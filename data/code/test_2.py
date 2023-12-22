import json
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def torch_gc():
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

prompt_input = (
    "{instruction}\n### Response:\n"
)

def generate_prompt(instruction, input=None):
    if input:
        instruction = instruction + '\n' + input
    return prompt_input.format_map({'instruction': instruction})

model_name=sys.argv[1]
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, device_map='auto').half()
model.eval()

def query_LLM(query):

    input_text = generate_prompt(instruction=query)
    inputs = tokenizer(input_text, return_tensors="pt")
    generate_kwargs = dict(
        input_ids=inputs["input_ids"].to('cuda'),
        max_new_tokens=4096,
        temperature=0.3,
        do_sample=True,
        top_p=1.0,
        top_k=10,
        repetition_penalty=1.1,
    )
    generation_output = model.generate(
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        **generate_kwargs
    )
    s = generation_output[0]
    output = tokenizer.decode(s, skip_special_tokens=True)
    response = output.split("### Response:")[1].strip()
    torch_gc()
    return response

with open("../raw_data/test_data_B.json", "r", encoding="utf-8") as read_file:
    with open(sys.argv[2], "w", encoding="utf-8") as submit_file:

        data = json.load(read_file)
        ret = []

        for line in data:
            js = {}
            js["id"] = line["id"]
            js["question"] = line["question"]
            js["attribute"] = []
            if js["id"][2] == "C":
                js["attribute"] = [query_LLM(js["question"])]
            elif js["id"][2] == "D":
                js["attribute"] = [query_LLM("请你按照下列要求进行内容创作，注意满足字数要求。\n" + js["question"])]
            else:
                query = "给你一个问题，请找出这个问题中最重要的一个实体并直接输出，除此之外不要输出其他任何字符。\n" + js["question"]
                print("query1: ", query)

                entity = query_LLM(query)
                print("entity: ", entity)
                js["attribute"] = [entity]
                # if entity not in knowledgebaseDict:
                #     js["attribute"] = ["没有找到该问题对应的知识"]
                #     ret.append(js)
                #     continue

                # query = "现在给你一个问题并告诉你问题中的唯一关键实体，再给你该实体的所有属性列表，属性之间用|分隔，你必须从属性列表中找出提问的属性并保持原样将它们输出，输出的每个属性用|隔开，如果属性列表中的属性均不匹配请输出“没有找到该问题对应的知识”，否则不允许输出不存在属性列表中的属性，除此之外不要输出其他任何字符。" + "\n"\
                #         "问题：" + js["question"] + " " +\
                #         "实体：" + entity + " " +\
                #         "属性列表："

                # for att in knowledgebaseDict[entity]:
                #     query += att + "|"
                # query = query[:-1]
                # print("query2: ", query)

                # attributes = query_LLM('http://10.208.62.156:6666', query)
                # print("attributes: ", attributes)
                # attributes = attributes.split("|")
                # for att in attributes:
                #     if len(att) == 0:
                #         continue
                #     if att == "没有找到该问题对应的知识":
                #         js["attribute"].append("没有找到该问题对应的知识")
                #         break
                #     if att in knowledgebaseDict[entity]:
                #         js["attribute"].append(entity + " ||| " + att + " ||| " + knowledgebaseDict[entity][att])
                #     else:
                #         waiting_list = []
                #         for k_att in knowledgebaseDict[entity]:
                #             overlap = len(set(att).intersection(set(k_att))) / min(len(att), len(k_att))
                #             if overlap >= 0.5:
                #                 waiting_list.append((k_att, overlap))
                #         if len(waiting_list) > 0:
                #             waiting_list.sort(key=lambda elem: elem[1], reverse=True)
                #             js["attribute"].append(entity + " ||| " + waiting_list[0][0] + " ||| " + knowledgebaseDict[entity][waiting_list[0][0]])

                # if len(js["attribute"]) == 0:
                #     js["attribute"] = ["没有找到该问题对应的知识"]
                # print(js)
            ret.append(js)

        json.dump(ret, submit_file, indent=4, ensure_ascii=False)
