# NER for AISC ML Ops 

A deployable Named Entity Recognition tool. 

```bash
cd src/bert
make build
make run
```

### Model
- spaCy as base model
- LSTMs/BERT as advanced model

### Packaging
- MLFlow with pyfunc

### Cloud platform
- Azure App Service for containers

### Dataset
- Wikigold

### Devops
- [![Build Status](https://dev.azure.com/ditadi/ner/_apis/build/status/ditadi.ner?branchName=master)](https://dev.azure.com/ditadi/ner/_build/latest?definitionId=1&branchName=master)
