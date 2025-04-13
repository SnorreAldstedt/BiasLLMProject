import re
from collections import Counter
import json

JSON_PATH = "scraping/combined_questions.json"

def extract_unique_rating(response: str) -> str:
    numbers = re.findall(r"\b(?:10|[0-9])\b", response)
    counts = Counter(numbers)

    if not numbers:
        return None
    elif len(counts) == 1:
        return list(counts.keys())[0]
    else:
        return "UNKNOWN"
    

def load_json(dict_path=JSON_PATH):
    with open(dict_path, "r", encoding="utf-8") as d:
        data = json.load(d)

    return data

def process_questions(original_dict_list, processed_dict_list, question_keys):
    new_processed = []
    for i in range(len(original_dict_list)):
        new_processed_results = {}
        persona_results = original_dict_list[i]
        processed_results = processed_dict_list[i]
        for q in question_keys:
            original_resp = persona_results[q]
            processed_resp = processed_results[q]
            if processed_resp == "UNKNOWN" or processed_resp == None:
                rating = extract_unique_rating(original_resp)
                #processed_results[q] = rating
                new_processed_results[q] = rating
            else:
                new_processed_results[q] = processed_resp
        new_processed.append(new_processed_results)
    return new_processed

def save_processed(original_dict_list, altered_dict_list, save_folder, save_name):
    for i in range(len(altered_dict_list)):
        result_altered_dict = altered_dict_list[i]
        for q_k, q_v in result_altered_dict.items():
            original_dict_list[i][q_k] = q_v

        filename = f"{save_folder}/{i}_{save_name}.json"
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(original_dict_list[i], f,ensure_ascii=False)

def process_and_save(original_dict_list, altered_dict_list, question_keys, save_folder, save_name):
    processed_altered = process_questions(original_dict_list, altered_dict_list, question_keys)
    save_processed(original_dict_list, processed_altered, save_folder, save_name)

if __name__ == "__main__":
    mistral_list = [load_json(f"results/mistral/{p_nr}_mistral.json") for p_nr in range(120)]
    mistral2_list = [load_json(f"results/mistral2/{p_nr}_mistral.json") for p_nr in range(120)]
    llama3_list = [load_json(f"results/llama3/{p_nr}_llama3.json") for p_nr in range(120)]
    llama3_2_list = [load_json(f"results/llama3_2/{p_nr}_llama3.json") for p_nr in range(120)]
    normistral_list = [load_json(f"results/normistral/{p_nr}_normistral.json") for p_nr in range(120)]
    normistral2_list = [load_json(f"results/normistral2/{p_nr}_normistral.json") for p_nr in range(120)]
    norwAI_mistral_list = [load_json(f"results/norwAI_mistral/{p_nr}_norwAI.json") for p_nr in range(120)]
    norwAI_mistral2_list = [load_json(f"results/norwAI_mistral2/{p_nr}_norwAI.json") for p_nr in range(120)]

    manual_mistral_list = [load_json(f"results_manual_processing/mistral/{p_nr}_mistral_processed.json") for p_nr in range(120)]
    manual_mistral2_list = [load_json(f"results_manual_processing/mistral2/{p_nr}_mistral2_processed.json") for p_nr in range(120)]
    manual_llama3_list = [load_json(f"results_manual_processing/llama3/{p_nr}_llama3_processed.json") for p_nr in range(120)]
    manual_llama3_2_list = [load_json(f"results_manual_processing/llama3_2/{p_nr}_llama3_2_processed.json") for p_nr in range(120)]
    manual_normistral_list = [load_json(f"results_manual_processing/normistral/{p_nr}_normistral_processed.json") for p_nr in range(120)]
    manual_normistral2_list = [load_json(f"results_manual_processing/normistral2/{p_nr}_normistral2_processed.json") for p_nr in range(120)]
    manual_norwAI_mistral_list = [load_json(f"results_manual_processing/norwAI_mistral/{p_nr}_norwAI_processed.json") for p_nr in range(120)]
    manual_norwAI_mistral2_list = [load_json(f"results_manual_processing/norwAI_mistral2/{p_nr}_norwAI2_processed.json") for p_nr in range(120)]

    #print(mistral_list)
    #questions_dict = load_json()
    relevant_questions = [
    "spm17_1","spm17_2","spm17_3","spm17_4","spm17_5","spm17_6","spm17_7","spm17_8","spm17_9",
    "spm19_1","spm19_2","spm19_3","spm19_4","spm19_5","spm19_6","spm19_7","spm19_8","spm19_9"]

    test_process = process_questions(llama3_list, manual_llama3_list, relevant_questions)
    print(len(test_process))

    """for i in range(len(test_process)):
        persona_result_dict = test_process[i]
        for question_key, question_value in persona_result_dict.items():
            manual_llama3_list[i][question_key] = question_value
        #save_processed(llama3_list[i], manual_llama3_list[i], "results_manual_processing/llama3","llama3_processed" )
    """

    print(manual_llama3_list)
    process_and_save(llama3_list, manual_llama3_list, relevant_questions, "results_manual_processing/llama3","llama3_processed" )
    process_and_save(llama3_2_list, manual_llama3_2_list, relevant_questions, "results_manual_processing/llama3_2","llama3_2_processed" )
    process_and_save(mistral_list, manual_mistral_list, relevant_questions, "results_manual_processing/mistral", "mistral_processed")
    process_and_save(mistral2_list, manual_mistral2_list, relevant_questions, "results_manual_processing/mistral2", "mistral2_processed")
    process_and_save(normistral_list, manual_normistral_list, relevant_questions, "results_manual_processing/normistral", "normistral_processed")
    process_and_save(normistral2_list, manual_normistral2_list, relevant_questions, "results_manual_processing/normistral2", "normistral2_processed")
    process_and_save(norwAI_mistral_list, manual_norwAI_mistral_list, relevant_questions, "results_manual_processing/norwAI_mistral", "norwAI_processed")
    process_and_save(norwAI_mistral2_list, manual_norwAI_mistral2_list, relevant_questions, "results_manual_processing/norwAI_mistral2", "norwAI2_processed")


"""
    test_p = llama3_list[2]
    test_p_pro = manual_llama3_list[2]
    for i in range(llama3_list):
        persona_results = llama3_list[i]
        for q in relevant_questions:
            resp = test_p_pro[q]
            resp_original = test_p[q]
            print(resp_original)
            if resp == "UNKNOWN" or resp == None:
                rating = extract_unique_rating(resp_original)
                print(q)
                print(rating)
"""