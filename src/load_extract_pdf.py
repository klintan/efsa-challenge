import requests
import sys
import os
from corvid.table_extraction.pdf_parser import TetmlPDFToXMLParser

from corvid.table_extraction import pdf_to_xml_parser

def load_extract_all(topic):
    articles_text = load_extract_text(topic)
    articles_figures = load_extract_figures(topic)
    articles_tables = load_extract_table_data(topic)

def load_extract_text(topic):
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
    return raw_articles


def load_extract_textract(topic):
    pass


def load_extract_sp(topic):
    pass


def load_extract_figures(topic):
    pass


def load_extract_table_data(topic):
    #needs pdflib tet to be installed which is licensed, perhaps not allowed
    pdf_parser = TetmlPDFToXMLParser(tet_bin_path="",
                                     target_dir="")
    pass

if __name__ == '__main__':
    topic = sys.argv[1]
    load_extract(topic)
