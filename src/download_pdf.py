import sys
import pandas as pd
import requests

def download_pdf(path):
    references = pd.read_csv(path)
    for idx, row in references.iterrows():
        try:
            r = requests.get(row['AlternativeLink'], timeout=5)
            with open(topic + '/' + str(idx) + '.pdf', 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print(e)
            print("Link download fail")


if __name__ == '__main__':
    topic = sys.argv[1]
    path = "dataset/" + topic + "/" + topic + " references for training set.csv"
    download_pdf(path)
