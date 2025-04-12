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
    manual_mistral2_list = [load_json(f"results_manual_processing/mistral2/{p_nr}_mistral_processed.json") for p_nr in range(120)]
    manual_llama3_list = [load_json(f"results_manual_processing/llama3/{p_nr}_llama3_processed.json") for p_nr in range(120)]
    manual_llama3_2_list = [load_json(f"results_manual_processing/llama3_2/{p_nr}_llama3_processed.json") for p_nr in range(120)]
    manual_normistral_list = [load_json(f"results_manual_processing/normistral/{p_nr}_normistral_processed.json") for p_nr in range(120)]
    manual_normistral2_list = [load_json(f"results_manual_processing/normistral2/{p_nr}_normistral_processed.json") for p_nr in range(120)]
    manual_norwAI_mistral_list = [load_json(f"results_manual_processing/norwAI_mistral/{p_nr}_norwAI_processed.json") for p_nr in range(120)]
    manual_norwAI_mistral2_list = [load_json(f"results_manual_processing/norwAI_mistral2/{p_nr}_norwAI_processed.json") for p_nr in range(120)]

    #print(mistral_list)
    #questions_dict = load_json()
    relevant_questions = [
    "spm17_1","spm17_2","spm17_3","spm17_4","spm17_5","spm17_6","spm17_7","spm17_8","spm17_9",
    "spm19_1","spm19_2","spm19_3","spm19_4","spm19_5","spm19_6","spm19_7","spm19_8","spm19_9"]

    test_p = llama3_list[2]
    for q in relevant_questions:
        resp = test_p[q]
        print(resp)
        rating = extract_unique_rating(resp)
        print(rating)