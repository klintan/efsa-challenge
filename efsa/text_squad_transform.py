import pandas as pd
import json
from nltk.tokenize import sent_tokenize
import re
import uuid

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
    return groundtruth_data.loc[groundtruth_data['topic'] == topic][list(attributes['feature']) + ['RefId']]


def get_context_question_answer_triples(topic, groundtruth_data, articles, attributes):
    topic_attributes = load_topic_attribute_data(topic, attributes)
    attribute_description_mapping = get_attribute_description_mapping(topic_attributes)
    topic_groundtruth_data = get_topic_training_data(topic=topic, groundtruth_data=groundtruth_data,
                                                     attributes=topic_attributes)
    squad_template = {"data": []}



    for idx, sample in enumerate(articles):
        squad_template['data'].append({'title': sample['Bibliography'], "paragraphs": []})
        sentences = sent_tokenize(sample['raw_text'])
        for sent_id, sentence in enumerate(sentences):
            qas = []
            context = create_sentence_context(sentence, sent_id, sentences)
            for idy, attrib in enumerate(attribute_description_mapping):
                # find exact match
                if re.search(r'\b' + sample[attrib].lower() + r'\b', sentence.lower()) and len(sample[attrib]) > 0:
                    # get index of exact match
                    # start_index = re.search(r'\b'+sample[attrib].lower()+r'\b', sentence.lower()).start()
                    start_index = re.search(r'\b' + sample[attrib].lower() + r'\b', context.lower()).start()
                    # start_index = sentence.lower().index(sample[attrib].lower())
                    q = attribute_description_mapping[attrib]
                    a = sample[attrib]
                    qas.append(add_qas_obj(q, a, start_index))
            if len(qas) >= 1:
                squad_template['data'][idx]['paragraphs'].append(create_paragraph_obj(context, qas))


def add_qas_obj(q, a, index):
    '''
    Creates SQuAD qas object with answers and question, and create a unique idea for each question.
    :param q: question, the description of the attribute to extract
    :param a: answer, the attribute that is extracted
    :param index: start index of answer in the context
    :return:
    '''
    q_id = uuid.uuid4()
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
            context = [sentence] + [sentences[index + 1]] + [all_sentences[index + 2]]
        elif index == len(all_sentences) - 1:
            context = [all_sentences[index - 2]] + [all_sentences[index - 1]] + [sentence]
        else:
            context = [all_sentences[index - 1]] + [sentence] + [all_sentences[index + 1]]
        return " ".join(context)
    return ""


def create_paragraph_obj(context, qas):
    return {"context": context, "qas": qas}
