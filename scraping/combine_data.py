import copy
import json

# method for combining two dicts with the structure of questions_data.json and questions.json
def combine_questions_dict(dict1, dict2, key) -> dict:
    new_dict = copy.deepcopy(dict2)
    # Key is a category, values is a list of keys of dict2
    for key1, values1 in dict1.items():
        for value in values1:
            #value = value.strip()

            # Had to include try, except because SVU_vekt1 and refnr doesnt exist
            try:
                new_dict[value][key] = key1
            except Exception as e:
                print(e)
    return new_dict


with open('questions.json', encoding="utf-8") as f:
    category_dict = json.load(f)

with open('questions_data.json', encoding="utf-8") as f:
    question_dict = json.load(f)

new_question_dict = combine_questions_dict(category_dict, question_dict, "category")

print(new_question_dict)
with open('combined_questions.json', 'w', encoding="utf-8") as f:
    json.dump(new_question_dict, f, ensure_ascii=False) 

