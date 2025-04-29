import os
import json

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def prompt_for_manual_input(persona_nr, question_key, original_value):
    print(f"\n[Persona {persona_nr}] Question: {question_key}")
    print(f"Original model answer: {original_value}")
    new_value = input("Enter a new value (or press Enter to skip): ").strip()
    return new_value if new_value else None

def edit_processed_files(original_folder, original_suffix,
                         processed_folder, processed_suffix,
                         start_persona = 0, persona_count=120):
    for persona_nr in range(start_persona,persona_count):
        original_path = os.path.join(original_folder, f"{persona_nr}_{original_suffix}.json")
        processed_path = os.path.join(processed_folder, f"{persona_nr}_{processed_suffix}.json")

        if not os.path.exists(original_path) or not os.path.exists(processed_path):
            print(f"Skipping persona {persona_nr}: File not found.")
            continue

        original_data = load_json_file(original_path)
        processed_data = load_json_file(processed_path)

        modified = False

        for q_key in processed_data:
            current_val = processed_data[q_key]
            if current_val == None or current_val == "UNKNOWN":
                original_val = original_data.get(q_key, "[No original answer found]")
                # Manual checking for strings repeated in norwAI which made manual processing harder
                # Comment out when not running norwAI
                """ 
                string_typical_1 = "1: Helt enig, 2: Nokså enig, 3: Både og, 4: Nokså uenig, 5: Helt uenig."
                string_typical_2 = "1: Helt enig 2: Nokså enig, 3: Både og, 4: Nokså uenig, 5: Helt uenig."
                string_typical_3 = "1: Helt enig, 2: Nokså enig, 3: Både og, 4: Nokså uenig, 5: Helt uenig"
                string_typical_4 = "1: Helt enig 2: Nokså enig, 3: Både og, 4: Nokså uenig, 5: Helt uenig"
                if string_typical_1.strip() == original_val.strip() or \
                    string_typical_2.strip() == original_val.strip() or \
                    string_typical_3.strip() == original_val.strip() or \
                    string_typical_4.strip() == original_val.strip():
                    continue
                """
                new_val = prompt_for_manual_input(persona_nr, q_key, original_val)
                if new_val != None:
                    processed_data[q_key] = new_val
                    modified = True

        if modified:
            save_json_file(processed_path, processed_data)
            print(f"Saved changes to {processed_path}")
        else:
            print(f"No changes for persona {persona_nr}")

def combine_dicts(list_of_dicts):
    new_dict = {}
    for i in range(len(list_of_dicts)):
        new_dict[i] = list_of_dicts[i]
    return new_dict

#test_dicts = [{"test1":1},{"test2":2}]
#print(combine_dicts(test_dicts))

def load_all_persona_json(processed_folder, processed_suffix, start_p = 0, end_p = 120):
    dict_list = []
    for i in range(start_p, end_p):
        processed_path = os.path.join(processed_folder, f"{i}_{processed_suffix}_processed.json")
        persona_dict = load_json_file(processed_path)
        dict_list.append(persona_dict)
    return dict_list

def load_and_combine_json(processed_folder, processed_suffix):
    combined_json = load_all_persona_json(processed_folder, processed_suffix)
    combine_name = os.path.join(processed_folder, f"combined_{processed_suffix}.json")
    combined = combine_dicts(combined_json)
    save_json_file(combine_name, combined)

# Example:
# edit_processed_files("results", "llama3", "results_manual_processing", "llama3_processed"), runs llama3 and checks the processed file, if Unknown or None, manually process the question
if __name__ == "__main__":
    #edit_processed_files("results/llama3/", "llama3", "results_manual_processing/llama3/", "llama3_processed")
    print("results_manual_processing/llama3/ FINISHED")
    #edit_processed_files("results/llama3_2/", "llama3", "results_manual_processing/llama3_2/", "llama3_2_processed")
    print("results_manual_processing/llama3_2/ FINISHED")
    #edit_processed_files("results/mistral", "mistral","results_manual_processing/mistral/", "mistral_processed")
    print("results_manual_processing/mistral/ FINISHED")
    #edit_processed_files("results/mistral2", "mistral","results_manual_processing/mistral2/", "mistral2_processed")
    print("results_manual_processing/mistral2/ FINISHED")
    #edit_processed_files("results/normistral", "normistral","results_manual_processing/normistral/", "normistral_processed")
    print("results_manual_processing/normistral/ FINISHED")
    #edit_processed_files("results/normistral2", "normistral","results_manual_processing/normistral2/", "normistral2_processed")
    print("results_manual_processing/normistral2/ FINISHED")
    #edit_processed_files("results/norwAI_mistral", "norwAI","results_manual_processing/norwAI_mistral/", "norwAI_processed")
    print("results_manual_processing/norwAI_mistral/ FINISHED")
    #edit_processed_files("results/norwAI_mistral2", "norwAI","results_manual_processing/norwAI_mistral2/", "norwAI2_processed")
    print("results_manual_processing/norwAI_mistral2/ FINISHED")
    load_and_combine_json("results_manual_processing/llama3/", "llama3")
    load_and_combine_json("results_manual_processing/llama3_2/", "llama3_2")
    load_and_combine_json("results_manual_processing/mistral/", "mistral")
    load_and_combine_json("results_manual_processing/mistral2/", "mistral2")
    load_and_combine_json("results_manual_processing/normistral/", "normistral")
    load_and_combine_json("results_manual_processing/normistral2/", "normistral2")
    load_and_combine_json("results_manual_processing/norwAI_mistral/", "norwAI")
    load_and_combine_json("results_manual_processing/norwAI_mistral2/", "norwAI2")
