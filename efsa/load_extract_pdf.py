import requests
import sys
import os
# from corvid.table_extraction.pdf_parser import TetmlPDFToXMLParser
from pdf2image import convert_from_path
from corvid.table_extraction import pdf_to_xml_parser
import json
import io

import yaml
import logging
#from logging.config import fileConfig

#fileConfig('logging_config.ini')
log = logging.getLogger()

from efsa.exceptions import DirectoryEmptyError

# load config
with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

PDF_PARSER_URL = config['pdf-parser']['url']

def load_extract_all(topic):
    articles_text = load_extract_text(topic)
    articles_figures = load_extract_figures(topic)
    articles_tables = load_extract_table_data(topic)


def load_extract_text(pdf_path, topic, save_json=False):
    if len(os.listdir(pdf_path)) == 0:
        raise DirectoryEmptyError("Article PDF folder empty: %s " % pdf_path)

    raw_articles = []
    for article in os.listdir(pdf_path):
        try:
            with open(pdf_path + "/" + article, 'rb') as payload:
                headers = {"Content-type": "application/pdf"}
                r = requests.post(PDF_PARSER_URL, headers=headers, data=payload)

            article_data = r.json()
            article_data['refId'] = os.path.splitext(article)[0]
            raw_articles.append(article_data)
        except Exception as e:
            print(e)
    if save_json:
        save_path = "data/" + topic + "/raw_json/articles.json"
        if not os.path.isfile(save_path):
            with open(save_path, 'w') as f:
                f.write(json.dumps(raw_articles))
        log.warning("Article json already exists, remove before overwriting")
    return raw_articles


def get_json_text_template():
    sections = {
        "heading": "",
        "text": "",
    }
    authors = {
        "name": "",
        "affiliations": []
    }
    template = {
        "sections": [],
        "id": "",
        "authors": [],
        "abstractText": ""
    }
    return (template, authors, sections)


def load_extract_textract(topic):
    raise NotImplementedError


def load_extract_ocr(path):
    '''
    Failed PDFs, last resort is using TesseractOCR to extract the text.
    :param topic:
    :return:
    '''

    template, authors, sections = get_json_text_template()

    url = "http://localhost:1688/upload"
    images = convert_from_path(path)
    articles = []

    for image in images:
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format='PNG')
        image_byte_array = image_byte_array.getvalue()
        r = requests.post(url, files=image_byte_array)
        sections['text'] = r.json()
        template['sections'].append(sections)

    return template


def load_extract_sp(topic):
    raise NotImplementedError


def load_extract_figures(topic):
    raise NotImplementedError


def load_extract_table_data(topic):
    # needs pdflib tet to be installed which is licensed, perhaps not allowed
    # pdf_parser = TetmlPDFToXMLParser(tet_bin_path="", target_dir = "")
    raise NotImplementedError


if __name__ == '__main__':
    topic = sys.argv[1]
    load_extract_text(topic)
