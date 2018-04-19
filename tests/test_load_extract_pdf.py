import pytest
from src.load_extract_pdf import load_extract
import os


def test_load_extract():
    articles = load_extract("AHAW VBD")
    assert(len(articles)==len(os.listdir("data/AHAW VBD")))