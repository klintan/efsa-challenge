import pytest
from efsa.load_extract_pdf import load_extract_text
import os


def test_load_extract_text():
    articles = load_extract_text("AHAW VBD")
    assert(len(articles)==len(os.listdir("data/AHAW VBD")))


def test_load_extract_text_save():
    articles = load_extract_text("AHAW VBD", save=True)
    assert(os.path.exists(data))