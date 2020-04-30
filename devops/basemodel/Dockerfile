FROM continuumio/miniconda3
WORKDIR /app

COPY ./basemodel .
RUN ls .

RUN conda env create --name basemodel -f conda.yml

# Make RUN commands use the new environment:
# https://pythonspeed.com/articles/activate-conda-dockerfile/
SHELL ["conda", "run", "-n", "basemodel", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure spacy is installed:"
RUN python -c "import spacy"

ENTRYPOINT ["conda", "run", "-n", "basemodel", "mlflow", "models", "serve", "-m", "/app"]

