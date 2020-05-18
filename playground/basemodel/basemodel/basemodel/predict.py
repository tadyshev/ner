import spacy
import mlflow.spacy

# training data
PREDICT_DATA = [
    ("Who is Shaka Khan?", {"entities": [(7, 17, "PERSON")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
]

if __name__ == "__main__":
	# Load the model using mlflow and use it to predict data
	nlp2 = mlflow.spacy.load_model(model_uri=".")
	for text, _ in PREDICT_DATA:
		doc = nlp2(text)
		print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
		print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

