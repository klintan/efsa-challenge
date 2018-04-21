import argparse
from efsa.load_extract_pdf import load_extract_all, load_extract_text
from efsa import text_squad_transform

import pandas as pd
import json


def get_topics_paths(topic):
    '''
    Helper function to get paths for a specific topic
    :param topic:
    :return:
    '''
    feat_desc_dir = "data/feature_descriptors.csv"
    attribute_train_dir = "data/training_set_attributes.csv"
    pdf_dir = "data/" + topic + "/pdf"
    return (pdf_dir, feat_desc_dir, attribute_train_dir)


def run_pipeline(topic, parse=True, mode="train", pdf_dir=None, feat_desc_dir=None, attribute_train_dir=None,
                 attribute_val_dir=None):
    '''
    Main pipeline for attribute extraction
    3 modes:
        - Train mode
        - Test mode
        - Predict/Extract mode

    Train Mode:
    For training 3 types of input files are needed and a new model is produced as an output.
    1. Path to folder of training PDF files (providing topic will assume default path)
    2. Path to feature description csv, containing attributes and attribute description of training set.
    3. Path to training set attributes csv files, containing pdf references and ref ids as well as extracted attributes from articles.

    Test Mode:
    For test 3 types of input files are needed and a F1 score is produced as output.
    1. Path to folder of validation PDF files (providing topic will assume default path of validation data).
    2. Path to feature description csv, containing attributes and attribute description of validation set.
    3. Path to validation set attributes csv files, containing pdf references and ref ids as well as extracted attributes from articles.

    Predict/Extract mode
    For predict/extract 3 types of input files are needed and a CSV output table with attribute columns from feature description csv
    is produced.
    1. Path to folder of new PDF files (providing topic will assume default path of PDFs).
    2. Path to feature description csv, containing attributes and attribute description of the attributes to be extracted.

    :param topic:
    :return:
    '''

    # Validate arguments
    if not topic and not pdf_dir:
        raise ("Define topic or pdf_dir")

    # Get all paths for topic
    if topic:
        pdf_dir, feat_desc_dir, attribute_train_dir = get_topics_paths(topic)

    # Load auxiliary data
    if mode == "train":
        groundtruth_data = pd.read_csv(attribute_train_dir)

    attributes = pd.read_csv(feat_desc_dir, dtype=str, encoding="utf-8")

    # 1. Extract data (text, figures and tables) from PDF in PDF folder (all modes)
    # probably create a "article"-class here which holds all info in one obj, for now only text
    if not parse:
        articles = load_extract_text(pdf_dir, topic, save_json=True)
    else:
        with open("data/" + topic + "/raw_json/articles.json") as art_f:
            articles = json.loads(art_f.read())

    # 2. Format data to SQuAD format
    if mode == "train":
        squad = text_squad_transform.get_context_question_answer_triples(topic, groundtruth_data, articles, attributes)
    else:
        squad = text_squad_transform.get_context_question_pair(articles, attributes, topic=None)

    # 3. (optional) train
    if mode == "train":
        pass

    # 4. extract attributes

    # 5. build csv output file and post-processing of data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', type=str,
                        help='name of the topic', default="AHAW VBD")
    parser.add_argument('--mode', type=str,
                        help='name of the topic', default="train")
    parser.add_argument('--parse', type=bool,
                        help='parse pdfs or used already extracted data', default="true")

    args = parser.parse_args()
    run_pipeline(args.topic, parse=args.parse)
