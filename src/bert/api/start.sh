#!/bin/bash

source activate mlflow-env-bert

python -m pip install newsapi-python
python /root/app.py