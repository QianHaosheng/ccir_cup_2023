#!/bin/sh

# train
eval "$(conda shell.bash hook)"
conda activate stanford_alpaca
cd ../data/code
bash train.sh ../user_data/Qwen-7B ../user_data/data1 ../user_data/ccir_model_17
bash train.sh ../user_data/Qwen-7B ../user_data/data2 ../user_data/ccir_model_20
bash train.sh ../user_data/Qwen-7B ../user_data/data3 ../user_data/ccir_model_19
bash train.sh ../user_data/Baichuan2-7B-Base ../user_data/data1 ../user_data/ccir_model_16
conda deactivate

conda activate llama_factory
cd LLaMA-Factory
bash train.sh ../../user_data/Qwen-14B ccir_small ../../user_data/ccir_model_21
python evaluate.py
python ner_convert.py
python evaluate_2.py
conda deactivate



# predict
conda activate stanford_alpaca
cd ..
python test.py ../user_data/ccir_model_16 ../prediction_result/submit_b_12.json
python test.py ../user_data/ccir_model_17 ../prediction_result/submit_b_13.json
python test.py ../user_data/ccir_model_19 ../prediction_result/submit_b_15.json
python test.py ../user_data/ccir_model_20 ../prediction_result/submit_b_21.json

python test_2.py ../user_data/ccir_model_16 ../user_data/ner_b_12.json
python test_2.py ../user_data/ccir_model_17 ../user_data/ner_b_13.json
python test_2.py ../user_data/ccir_model_19 ../user_data/ner_b_15.json
python test_2.py ../user_data/ccir_model_20 ../user_data/ner_b_21.json

python merge_ner.py

conda deactivate
conda activate llama_factory
cd LLaMA-Factory
python ner_convert_2.py
python evaluate_3.py
cd ..
conda deactivate

conda activate stanford_alpaca
python test_3.py ../user_data/ccir_model_16 ../prediction_result/submit_b_12_2.json
python test_3.py ../user_data/ccir_model_17 ../prediction_result/submit_b_13_2.json
python test_3.py ../user_data/ccir_model_19 ../prediction_result/submit_b_15_2.json
python test_3.py ../user_data/ccir_model_20 ../prediction_result/submit_b_21_2.json

python merge.py
conda deactivate