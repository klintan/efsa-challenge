import argparse
from src.load_extract_pdf import load_extract_all, load_extract_text


def run_pipeline(topic, mode="train", pdf_dir=None, feat_desc_dir=None, attribute_train_dir=None, attribute_val_dir=None):
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
        raise("Define topic or pdf_dir")

    # 1. Extract data (text, figures and tables) from PDF in PDF folder (all modes)
    # probably create a "article"-class here which holds all info in one obj, for now only text
    articles = load_extract_text(topic)

    # 2. Format data to SQuAD format
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', type=str,
                        help='name of the topic', default="AHAW VBD")
    parser.add_argument('--mode', type=str,
                        help='name of the topic', default="train")

    args = parser.parse_args()
    run_pipeline(args.topic)
