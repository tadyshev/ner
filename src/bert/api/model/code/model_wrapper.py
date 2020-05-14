import torch
import json


class ModelWrapper():
  def __init__(self, model, tokenizer, label_dict):
    self._model = model
    self._tokenizer = tokenizer
    self._label_dict = label_dict

  def predict(self, data):

    splits = data.iloc[0]['text'].split(" ")[:250]

    token_list, tags = [], []

    chunk_size = 75

    for i in range(0, len(splits), chunk_size):

      input_ids = torch.tensor([self._tokenizer.encode(" ".join(splits[i:i+chunk_size]), add_special_tokens=True)])

      outputs = self._model(input_ids)[0].squeeze()
      output_ids = torch.argmax(outputs, dim=1)

      token_list.extend(self._tokenizer.convert_ids_to_tokens(input_ids.squeeze()))
      tags.extend([self._label_dict[str(oid.item())] for oid in output_ids])
    

    return token_list, tags


def _load_pyfunc(path):

  # Load the model object
  model = torch.load(f'{path}/model.pt')

  # Load in the tokenizer
  tokenizer = torch.load(f'{path}/tokenizer.pt')

  # Load in the config file for label mapping
  with open(f'{path}/config.json', 'r') as f:
    label_dict = json.load(f)['id2label']


  return ModelWrapper(
      model=model,
      tokenizer=tokenizer,
      label_dict=label_dict
  )