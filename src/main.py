import argparse
from src.load_extract_pdf import load_extract_all,load_extract_text

def run_pipeline(topic):
    articles_text = load_extract_text(topic)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', type=str,
                        help='name of the topic', default="AHAW VBD")

    args = parser.parse_args()
    run_pipeline(args.topic)