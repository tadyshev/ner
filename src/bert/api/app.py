from flask import Flask, request, jsonify, render_template, url_for
import mlflow.pyfunc
import pandas as pd
import requests
from newsapi import NewsApiClient

import json
import time
import string


app = Flask(__name__)

# Load in the model at app startup
model = mlflow.pyfunc.load_model('./model')


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/predict")
def predict():

    params = request.args.to_dict()

    text = pd.DataFrame(data={'text': [params['text']]})

    predictions = model.predict(text)

    print(predictions)

    if request.method == 'GET':
        return add_html_tags(predictions)

    if request.method == 'POST':
        return jsonify([predictions])

    return ''


@app.route("/news")
def news():
    params = request.args.to_dict()

    api_client = NewsApiClient(api_key='1e0334ac55a24c4d937ccfcccb183e20')

    if 'category' in params:
        results = api_client.get_top_headlines(country='us',
                                               category=params['category'],
                                               page_size=5,
                                               )
    else:
        return "No category specified"

    try:
        headlines = [a['title'] for a in results['articles']]
    except KeyError:
        print("Key error")

    tagged = []
    for h in headlines:
        text = pd.DataFrame(data={'text': [h]})
        tagged.append(add_html_tags(model.predict(text)))
    
    return jsonify(tagged)

@app.route("/headlines")
def headlines():
    return render_template("headlines.html")


def add_html_tags(predictions):
    html_text = ''
    for i, (token, label) in enumerate(zip(*predictions)):
        if token in ['[CLS]', '[SEP]']:
            continue
        if token[:2] == '##':
            token = token[2:]
        elif token in string.punctuation:
            pass
        else:
            token = f" {token}"
        if label != 'O':
            html_text += f"<span class='{label.lower()}'>{token}</span>"
        else:
            html_text += f"{token}"

    return html_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
