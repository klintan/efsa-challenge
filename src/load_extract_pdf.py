import requests
import sys
import os
# from corvid.table_extraction.pdf_parser import TetmlPDFToXMLParser
from pdf2image import convert_from_path
from corvid.table_extraction import pdf_to_xml_parser
import json
import io


def load_extract_all(topic):
    articles_text = load_extract_text(topic)
    articles_figures = load_extract_figures(topic)
    articles_tables = load_extract_table_data(topic)


def load_extract_text(topic, save_json=False):
    raw_articles = []
    for article in os.listdir("data/" + topic):
        try:
            with open("data/" + topic + "/" + article, 'rb') as payload:
                headers = {"Content-type": "application/pdf"}
                url = "http://localhost:8080/v1"
                r = requests.post(url, headers=headers, data=payload)
            raw_articles.append(r.json())
        except Exception as e:
            print(e)
    if save_json:
        with open("data/" + topic + "/raw_json/articles.json") as f:
            f.write(json.dumps(raw_articles))
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
