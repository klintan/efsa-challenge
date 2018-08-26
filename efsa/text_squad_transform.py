import pandas as pd
import json
from nltk.tokenize import sent_tokenize
import re
import uuid
from itertools import groupby


def load_topic_attribute_data(topic, attributes):
    if topic:
        return attributes.loc[attributes['topic'] == topic]
    return attributes


def get_attribute_description_mapping(attributes):
    '''
    Attribute descriptions, what we also use as "questions" for the sake of training SQuAD and QA systems
    :return:
    '''
    return {row["feature"]: row['description'] for _, row in attributes.iterrows()}


def get_context_question_pair(articles_text, attributes, topic=None):
    '''
    Create context question pair for each sentence to get attributes
    :param articles_text:
    :return:
    '''

    attributes = load_topic_attribute_data(topic)
    attribute_description_mapping = get_attribute_description_mapping(attributes)
    template = {"data": []}
    for article in articles_text:
        print(article)
    pass


def get_topic_training_data(topic, groundtruth_data, attributes):
    '''
    Get dataframe with all attribute columns and article RefId, rows are attributes extracted from articles
    :param topic:
    :param groundtruth_data:
    :param attributes:
    :return:
    '''
    return groundtruth_data.loc[groundtruth_data['topic'] == topic][
        list(attributes['feature']) + ['Refid', 'Bibliography']]


def clean_article(article):
    '''
    Remove all sections in the article which does not contain any text
    :param article:
    :return:
    '''
    if not 'sections' in article:
        article['sections'] = []
        return article

    article['sections'] = [text for text in article['sections'] if len(text['text']) != 0]
    return article


def get_body_text(article):
    '''
    Get all body text from an article (also implemented in the article class)
    :param article:
    :return:
    '''
    body_text = []
    if 'abstractText' in article:
        body_text.append(article['abstractText'])

    for section in article['sections']:
        if 'heading' in section:
            body_text.append(section['heading'])
        if 'text' in section:
            body_text.append(section['text'])
    return ' '.join(body_text)


def get_article_by_id(articles):
    article_by_id = {}
    for key, group in groupby(articles, lambda x: x['refId']):
        article_by_id[key] = list(group)[0]

    return article_by_id


def get_context_question_answer_triples(topic, groundtruth_data, articles, attributes, save_article=False):
    topic_attributes = load_topic_attribute_data(topic, attributes)
    attribute_description_mapping = get_attribute_description_mapping(topic_attributes)
    topic_groundtruth_data = get_topic_training_data(topic=topic, groundtruth_data=groundtruth_data,
                                                     attributes=topic_attributes)
    squad_template = {"data": []}
    article_by_id = get_article_by_id(articles)

    # a counter is needed for now since if we continue in the loop it will not be the correct array index
    count = 0
    for idx, data_sample in topic_groundtruth_data.iterrows():
        if not str(data_sample['Refid']) in article_by_id:
            continue

        article = clean_article(article_by_id[str(data_sample['Refid'])])

        if len(article['sections']) == 0:
            # temporary measure, it should never be empty, that means we have errors in parsing
            continue
        bibliography = \
            topic_groundtruth_data.loc[topic_groundtruth_data['Refid'] == article['refId']]['Bibliography'].values[0]
        squad_template['data'].append({'title': bibliography, "paragraphs": []})
        body_text = get_body_text(article)
        sentences = sent_tokenize(body_text)

        if save_article:
            with open("data/" + topic + "/raw_txt/" + article['refId'] + ".txt", 'w') as article_file:
                article_file.write(json.dumps({"text": body_text}))

        for sent_id, sentence in enumerate(sentences):
            qas = []
            context = create_sentence_context(sentence, sent_id, sentences)
            for idy, attrib in enumerate(attribute_description_mapping):
                # find exact match
                if re.search(r'\b' + str(data_sample[attrib]).lower() + r'\b', sentence.lower()) and len(
                        data_sample[attrib]) > 0:
                    # get index of exact match
                    start_index = re.search(r'\b' + str(data_sample[attrib]).lower() + r'\b', context.lower()).start()
                    q = attribute_description_mapping[attrib]
                    a = data_sample[attrib]
                    qas.append(add_qas_obj(q, a, start_index))
            if len(qas) >= 1:
                squad_template['data'][count]['paragraphs'].append(create_paragraph_obj(context, qas))
        count += 1
    return squad_template


def add_qas_obj(q, a, index):
    '''
    Creates SQuAD qas object with answers and question, and create a unique idea for each question.
    :param q: question, the description of the attribute to extract
    :param a: answer, the attribute that is extracted
    :param index: start index of answer in the context
    :return:
    '''
    q_id = str(uuid.uuid4())
    qas = {}
    qas['question'] = q
    qas['id'] = q_id
    qas['answers'] = [{
        "answer_start": index,
        "text": a
    }, {
        "answer_start": index,
        "text": a
    }, {
        "answer_start": index,
        "text": a
    }]
    return qas


def create_sentence_context(sentence, index, all_sentences):
    if len(all_sentences) > 2:
        if index == 0:
            context = [sentence] + [all_sentences[index + 1]] + [all_sentences[index + 2]]
        elif index == len(all_sentences) - 1:
            context = [all_sentences[index - 2]] + [all_sentences[index - 1]] + [sentence]
        else:
            context = [all_sentences[index - 1]] + [sentence] + [all_sentences[index + 1]]
        return " ".join(context)
    return ""


def create_paragraph_obj(context, qas):
    return {"context": context, "qas": qas}
