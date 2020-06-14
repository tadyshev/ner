# Create common environment for training and serving BERT
FROM ubuntu:18.04 AS conda-env

# Set character encoding environment variables
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

# Allow apt-get install without interaction from console
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory to /root
WORKDIR /root

# System updates and configurations
RUN apt-get update && apt-get -y --no-install-recommends install \
		ca-certificates \
		git \
		ssh \
		wget && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
	bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda && \
	rm Miniconda3-latest-Linux-x86_64.sh

# Set the path env to include miniconda
ENV PATH /root/miniconda/bin:$PATH

# Serving environment
FROM conda-env 

# Copy over dependency file to cache (hopefully) core packages
COPY ./api/model/mlflow_env.yml /root/mlflow_env.yml 


# Create a conda environment from the specified conda.yaml
RUN conda env create --file /root/mlflow_env.yml

# Add to .bashrc
RUN echo "source activate mlflow-env-bert" >> .bashrc


COPY ./api/requirements.txt /root/requirements.txt

# Pip install api requirements into the conda env
RUN /bin/bash -c "source activate mlflow-env-bert" && \
	pip install --upgrade pip setuptools && \
	pip install -r /root/requirements.txt --no-cache-dir


# Download trained BERT pytorch model
RUN wget 'https://aisc-mlops-bert.s3.amazonaws.com/model.pt' -O /root/model.pt -nc

RUN pip install newsapi-python

# Copy over everything else into the container
COPY ./api /root

RUN ln -s /root/model.pt ./model/data/pyfunc_data/model.pt


# Make our start script executable
RUN ["chmod", "+x", "/root/start.sh"]

EXPOSE 80 5000

# Start the API
ENTRYPOINT [ "/root/start.sh" ]
