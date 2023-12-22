import json

submit = []

file_idx = [13, 12, 15, 16, 21]

for idx in file_idx:
    with open("../user_data/ner_b_" + str(idx) + ".json" , "r") as f:
        submit.append(json.load(f))

with open("../user_data/ner_b_12_13_15_16_21.json", "w") as write_f:

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
                entity = file[idx]["attribute"][0]
                if entity in tmp_set:
                    tmp_set[entity] += 1
                else:
                    tmp_set[entity] = 1
            
            tmp_set = sorted(tmp_set.items(),  key=lambda elem: elem[1], reverse=True)

            ans["attribute"] = []

            for item in tmp_set:
                if item[0] in ans["question"]:
                    ans["attribute"].append(item[0])
                    break

            if len(ans["attribute"]) == 0:
                ans["attribute"].append(tmp_set[0][0])
            print(tmp_set)

        ret.append(ans)

    json.dump(ret, write_f, indent=4, ensure_ascii=False)