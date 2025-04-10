import json 

JSON_PATH = "scraping/combined_questions.json"
QUESTION_IDS = ["Spm1", "Spm2", "Spm3", 
                "spm6_1","spm6_2","spm6_3","spm6_4","spm6_5","spm6_6","spm6_7","spm6_8","spm6_9","spm6_10","spm6_11",
                "spm17_1","spm17_2","spm17_3","spm17_4","spm17_5","spm17_6","spm17_7","spm17_8","spm17_9",
                "spm19_1","spm19_2","spm19_3","spm19_4","spm19_5","spm19_6","spm19_7","spm19_8","spm19_9",
                "Spm5a","Spm5b","Spm5c","Spm5d","Spm5e","Spm5f","Spm5g","Spm5h","Spm5i",
                "Spm7a","Spm7b","Spm7c","Spm7d","Spm7e","Spm7f","Spm7g",
                "Spm23a","Spm23b","Spm23c","Spm23d","Spm23e","Spm23f","Spm23h",
                "Spm31a","Spm31b","Spm31c","Spm48a","Spm48b","Spm48c","Spm48d","Spm48e","Spm48f","Spm48g",
                "Spm51a","Spm51b","Spm51c","Spm51d","Spm51e","Spm51f","Spm51g",
                ]

def load_json(dict_path=JSON_PATH):
    with open(dict_path, "r", encoding="utf-8") as d:
        data = json.load(d)

    return data

#Function that returns list of possible options, given a question ID
def get_question_options(question_id:str, data_dict) -> dict:
    alt = data_dict[question_id]["alternatives"]
    return alt

#Function that returns True if a string exist in the output
def exist_in_output(answer: str, output_str: str) -> bool:
    str_ind = output_str.find(answer)
    if str_ind != -1:
        return True
    else:
        return False

def check_response_against_alternatives(response: str, alternatives: dict) -> str | None:
    matched_keys = []
    for key, value in alternatives.items():
        if key in response or value in response:
            matched_keys.append(key)
    
    if not matched_keys:
        return None
    elif len(matched_keys) == 1:
        return matched_keys[0]
    else:
        return "UNKNOWN"

def persona_response(persona_response_dict, question_file_dict):
    #persona_response_dict = load_json()
    answer_dict = {}
    for key, value in persona_response_dict.items():
        answer_result = check_response_against_alternatives(value, get_question_options(key, question_file_dict))
        answer_dict[key] = answer_result
    return answer_dict

def save_responses(dict_list, q_file_dict, save_folder, save_name):
    for count, res_dict in enumerate(dict_list):
        ans_dict = persona_response(res_dict, q_file_dict)
        #print(ans_dict)
        filename = f"{save_folder}/{count}_{save_name}.json"
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(ans_dict, f,ensure_ascii=False)

if __name__ == "__main__":
    mistral_list = [load_json(f"results/mistral/{p_nr}_mistral.json") for p_nr in range(120)]
    mistral2_list = [load_json(f"results/mistral2/{p_nr}_mistral.json") for p_nr in range(120)]
    llama3_list = [load_json(f"results/llama3/{p_nr}_llama3.json") for p_nr in range(120)]
    llama3_2_list = [load_json(f"results/llama3_2/{p_nr}_llama3.json") for p_nr in range(120)]
    normistral_list = [load_json(f"results/normistral/{p_nr}_normistral.json") for p_nr in range(120)]
    normistral2_list = [load_json(f"results/normistral2/{p_nr}_normistral.json") for p_nr in range(120)]
    norwAI_mistral_list = [load_json(f"results/norwAI_mistral/{p_nr}_norwAI.json") for p_nr in range(120)]
    norwAI_mistral2_list = [load_json(f"results/norwAI_mistral2/{p_nr}_norwAI.json") for p_nr in range(120)]

    #print(mistral_list)
    questions_dict = load_json()
    save_responses(mistral_list, questions_dict, "results_processing/mistral", "mistral_processed")
    save_responses(mistral2_list, questions_dict, "results_processing/mistral2", "mistral2_processed")
    save_responses(normistral_list, questions_dict, "results_processing/normistral", "normistral_processed")
    save_responses(normistral2_list, questions_dict, "results_processing/normistral2", "normistral2_processed")
    save_responses(norwAI_mistral_list, questions_dict, "results_processing/norwAI_mistral", "norwAI_processed")
    save_responses(norwAI_mistral2_list, questions_dict, "results_processing/norwAI_mistral2", "norwAI2_processed")
    save_responses(llama3_list, questions_dict, "results_processing/llama3", "llama3_processed")
    save_responses(llama3_2_list, questions_dict, "results_processing/llama3_2", "llama3_2_processed")
#TODO: Add functions for: reading the results from the actual llms.
"""
test = load_json()
#print(test)
print(get_question_options("Spm1", test))

mistral_0 = load_json("results/mistral/0_mistral.json")
#print(mistral_0)

q_1 = mistral_0["Spm1"]
#print(q_1)
test_check = check_response_against_alternatives(q_1, get_question_options("Spm1", test))
#print(test_check)

for count, key_value in enumerate(mistral_0.items()):
    key, value = key_value
    print(f"Question {key}: {check_response_against_alternatives(value, get_question_options(key, test))}")
#check_response_against_alternatives(mistral_0)
"""