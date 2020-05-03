from flask import Flask, request, jsonify, render_template
import mlflow.pyfunc
import pandas as pd
import json

# Name of the apps module package
app = Flask(__name__)

# Load in the model at app startup
model = mlflow.pyfunc.load_model('./model')


@app.route('/', methods=['GET', 'POST'])
def home():

	results = None
	if request.method == 'POST':
		text = request.form.get('text')
		if text:
			# Format the request data in a DataFrame
			inf_df = pd.DataFrame(data={'text':[text]})

			# Get model prediction - convert from np to list
			results = model.predict(inf_df).tolist()

			# Log the prediction
			print({'response': results})
		return jsonify(results)

	return render_template('home.html')

# Prediction endpoint
@app.route('/predict', methods=['GET'])
def predict():
	print(request)
	req = request.get_json()
	
	# Log the request
	print({'request': req})

	# Format the request data in a DataFrame
	inf_df = pd.DataFrame(data={'text':req['text']})

	# Get model prediction - convert from np to list
	pred = model.predict(inf_df).tolist()

	# Log the prediction
	print({'response': pred})

	# Return prediction as reponse
	return jsonify(pred)

app.run(host='0.0.0.0', port=5000)
