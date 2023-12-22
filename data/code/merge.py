import json

submit = []

file_idx = [12, 13, 15, 16, 21]

for idx in file_idx:
    with open("../prediction_result/submit_b_" + str(idx) + ".json" , "r") as f:
        submit.append(json.load(f))

for idx in file_idx:
    with open("../prediction_result/submit_b_" + str(idx) + "_2" + ".json" , "r") as f:
        submit.append(json.load(f))
        

with open("../prediction_result/submit_b_12_13_15_16_21_all.json", "w") as write_f:

    ret = []
    for idx, data in enumerate(submit[0]):
        
        if data["id"][2] == "C" or data["id"][2] == "D":
            ans = data
        else:
            ans = {}
            ans["id"] = data["id"]
            ans["question"] = data["question"]

            tmp_set = {}

            for file in submit:
                if file[idx]["attribute"][0] == "没有找到该问题对应的知识":
                    continue
                for att in file[idx]["attribute"]:
                    part = att.split(" ||| ")
                    att = part[0] + " ||| " + part[1].replace(" ", "") + " ||| " + part[2]
                    if att in tmp_set:
                        tmp_set[att] += 1
                    else:
                        tmp_set[att] = 1
            tmp_set = sorted(tmp_set.items(),  key=lambda elem: elem[1], reverse=True)

            ans["attribute"] = []
            for item in tmp_set:
                ans["attribute"].append(item[0])

            if len(ans["attribute"]) == 0:
                ans["attribute"].append("没有找到该问题对应的知识")
            print(tmp_set)

        ret.append(ans)

    json.dump(ret, write_f, indent=4, ensure_ascii=False)