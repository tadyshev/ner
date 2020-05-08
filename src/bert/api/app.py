from flask import Flask, request, jsonify, render_template, url_for
import mlflow.pyfunc
import pandas as pd
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
