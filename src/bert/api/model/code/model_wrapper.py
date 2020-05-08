import torch
import json


class ModelWrapper():
  def __init__(self, model, tokenizer, label_dict):
    self._model = model
    self._tokenizer = tokenizer
    self._label_dict = label_dict

  def predict(self, data):

    input_ids = torch.tensor([self._tokenizer.encode(data.iloc[0]['text'], add_special_tokens=True)])

    outputs = self._model(input_ids)[0].squeeze()
    output_ids = torch.argmax(outputs, dim=1)

    token_list = self._tokenizer.convert_ids_to_tokens(input_ids.squeeze())
    

    return token_list, [self._label_dict[str(oid.item())] for oid in output_ids]


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