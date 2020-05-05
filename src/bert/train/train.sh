#!/bin/bash

mkdir $HOME/tmp
export TMPDIR=$HOME/tmp

source activate mlflow-env-bert

# Install transformers from source NOTE: it installs tensorflow-board and it may fail ingore it
echo "Install transformers from source"
git clone https://github.com/huggingface/transformers
cd transformers
pip install .
cd ..
pip install -r ./transformers/examples/requirements.txt

# Download training data 
echo "Download training data"
# TODO: create a loop 
# TODO: downloading files can be another docker multi-stage build s.t. they can be cached by docker
train='https://raw.githubusercontent.com/davidsbatista/NER-datasets/master/CONLL2003/train.txt'
dev='https://raw.githubusercontent.com/davidsbatista/NER-datasets/master/CONLL2003/valid.txt'
test='https://raw.githubusercontent.com/davidsbatista/NER-datasets/master/CONLL2003/test.txt'
wget $train -O raw-train.txt -nc
wget $dev -O raw-dev.txt -nc
wget $test -O raw-test.txt -nc
	
# Download HuggingFace utility files
echo "Download HuggingFace utility files"
run_ner_url='https://raw.githubusercontent.com/huggingface/transformers/master/examples/ner/run_ner.py'
ner_utils_url='https://raw.githubusercontent.com/huggingface/transformers/master/examples/ner/utils_ner.py'
preprocess_url='https://raw.githubusercontent.com/stefan-it/fine-tuned-berts-seq/master/scripts/preprocess.py'
wget $run_ner_url -nc
wget $ner_utils_url -nc
wget $preprocess_url -nc


# Preprocess train/dev/test files
echo "Preprocess train/dev/test files"
python preprocess.py raw-train.txt bert-base-cased 128 > train.txt
python preprocess.py raw-dev.txt bert-base-cased 128 > dev.txt
python preprocess.py raw-test.txt bert-base-cased 128 > test.txt

# Check for train.txt/dev.txt/test.txt files are there
echo "Check for train.txt/dev.txt/test.txt files are there"
ls .

# Create labels file
echo "Create labels file"
labels_file='labels.txt'
cat train.txt dev.txt test.txt | cut -d " " -f 4 | grep -v "^$"| sort | uniq > $labels_file


# Setup training environment variables
echo "Setup training environment variables"
output_dir='bert-ner-model'
mkdir $output_dir

export MAX_LENGTH='128'
export BERT_MODEL='bert-base-cased'

export OUTPUT_DIR=output_dir
export BATCH_SIZE='32'
export NUM_EPOCHS='3'
export SAVE_STEPS='750'
export SEED='1'
export LABELS='labels.txt'

# Train
echo "Train BERT model"
python run_ner.py --data_dir ./ \
--labels $LABELS \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--max_seq_length $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_train \
--do_eval \
--do_predict
echo "Training BERT model complete"

echo "Working Directory"
ls
echo "Output Directory"
ls $output_dir
