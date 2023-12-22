环境说明
操作系统：centos 7
NVIDIA驱动版本: 535.104.05

一键运行需要切换两个conda环境

stanford_alpaca环境安装：
conda create -n stanford_alpaca python=3.10
conda activate stanford_alpaca
cd ../data/code
pip install -r requirements.txt


llama_factory环境安装：
conda create -n llama_factory python=3.10
conda activate llama_factory
cd ../data/code/LLaMA-Factory
pip install -r requirements.txt

run.sh说明：
```
bash train.sh ../user_data/Qwen-7B ../user_data/data1 ../user_data/ccir_model_17
bash train.sh ../user_data/Qwen-7B ../user_data/data2 ../user_data/ccir_model_20
bash train.sh ../user_data/Qwen-7B ../user_data/data3 ../user_data/ccir_model_19
bash train.sh ../user_data/Baichuan2-7B-Base ../user_data/data1 ../user_data/ccir_model_16
```
训练baichuan2-7b（编号为16）、qwen-7b（编号为17，19，20）

```
bash train.sh ../../user_data/Qwen-14B ccir_small ../../user_data/ccir_model_21
```
训练qwen-14b（编号为21）

```
python test.py ../user_data/ccir_model_16 ../prediction_result/submit_b_12.json
python test.py ../user_data/ccir_model_17 ../prediction_result/submit_b_13.json
python test.py ../user_data/ccir_model_19 ../prediction_result/submit_b_15.json
python test.py ../user_data/ccir_model_20 ../prediction_result/submit_b_21.json
```
16、17、19、20号模型进行推理，输出文件编号为12、13、15、21

```
python evaluate.py
```
21号模型进行实体识别任务推理


```
python evaluate_2.py
```
21号模型进行属性选择任务推理，输出文件编号为16

```
python test_2.py ../user_data/ccir_model_16 ../user_data/ner_b_12.json
python test_2.py ../user_data/ccir_model_17 ../user_data/ner_b_13.json
python test_2.py ../user_data/ccir_model_19 ../user_data/ner_b_15.json
python test_2.py ../user_data/ccir_model_20 ../user_data/ner_b_21.json
```
分阶段推理，16、17、19、20号模型进行实体识别任务推理

```
python merge_ner.py
```
融合实体结果

```
python evaluate_3.py
```
分阶段推理，21号模型使用融合后的实体进行属性选择任务推理

```
python test_3.py ../user_data/ccir_model_16 ../prediction_result/submit_b_12_2.json
python test_3.py ../user_data/ccir_model_17 ../prediction_result/submit_b_13_2.json
python test_3.py ../user_data/ccir_model_19 ../prediction_result/submit_b_15_2.json
python test_3.py ../user_data/ccir_model_20 ../prediction_result/submit_b_21_2.json
```
分阶段推理，16、17、19、20号模型使用融合后的实体进行属性选择任务推理

```
python merge.py
```
融合最终结果，生成submit_b_12_13_15_16_21_all.json