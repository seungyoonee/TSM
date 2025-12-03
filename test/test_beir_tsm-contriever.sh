#!/bin/bash

MODEL_NAME_OR_PATH="seungyoonee/tsm-contriever"
BEIR_DIR="../dataset/test"
DATASETS="nobel_prize timeqa nq msmarco"

for dataset in $DATASETS; do
    echo "Evaluating on BEIR dataset: $dataset"
    
    python ../contriever/eval_beir.py \
        --model_name_or_path $MODEL_NAME_OR_PATH \
        --beir_dir $BEIR_DIR \
        --dataset $dataset \
        --output_dir ./eval_output_beir/$MODEL_NAME_OR_PATH/$dataset \
        --per_gpu_batch_size 256
        
done

echo "BEIR evaluation complete."
