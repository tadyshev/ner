from flask import Flask, request, jsonify, render_template, url_for
import mlflow.pyfunc
import pandas as pd
import requests

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
        return jsonify([add_html_tags(predictions)])

    return ''


categories = ['us', 'world', 'politics', 'business', 'opinion', 'health', 'entertainment', 'style', 'travel']

@app.route("/cnn")
def cnn():
    params = request.args.to_dict()

    if 'category' in params:
        url = f'https://search.api.cnn.io/content?size=5&q=*&type=article&sort=newest&from=0&category={params["category"]}'
    else:
        url = 'https://search.api.cnn.io/content?size=5&q=*&type=article&sort=newest&from=0'
    try:
        headlines = [r['headline'] for r in requests.get(url).json()['result']]

    except KeyError as e:
        print("KeyError", e)
        return ""
    except IndexError as e:
        print("IndexError", e)
        return ""

    print(headlines)
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
