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
    for persona_nr in range(persona_count):
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
                new_val = prompt_for_manual_input(persona_nr, q_key, original_val)
                if new_val != None:
                    processed_data[q_key] = new_val
                    modified = True

        if modified:
            save_json_file(processed_path, processed_data)
            print(f"Saved changes to {processed_path}")
        else:
            print(f"No changes for persona {persona_nr}")

# This function is ready to be used as described.
# Example:
# edit_processed_files("results", "llama3", "results_manual_processing", "llama3_processed")
if __name__ == "__main__":
    #edit_processed_files("results/llama3/", "llama3", "results_manual_processing/llama3/", "llama3_processed")
    print("results_manual_processing/llama3/ FINISHED")
    #edit_processed_files("results/llama3_2/", "llama3", "results_manual_processing/llama3_2/", "llama3_2_processed")
    print("results_manual_processing/llama3_2/ FINISHED")
    #edit_processed_files("results/mistral", "mistral","results_manual_processing/mistral/", "mistral_processed")
    print("results_manual_processing/mistral/ FINISHED")
    #edit_processed_files("results/mistral2", "mistral","results_manual_processing/mistral2/", "mistral2_processed")
    print("results_manual_processing/mistral2/ FINISHED")
    edit_processed_files("results/normistral", "normistral","results_manual_processing/normistral/", "normistral_processed", start_persona=97)
    print("results_manual_processing/normistral/ FINISHED")
    edit_processed_files("results/normistral2", "normistral","results_manual_processing/normistral2/", "normistral2_processed")
    print("results_manual_processing/normistral2/ FINISHED")
    edit_processed_files("results/norwAI_mistral", "norwAI","results_manual_processing/norwAI_mistral/", "norwAI_processed")
    print("results_manual_processing/norwAI_mistral/ FINISHED")
    edit_processed_files("results/norwAI_mistral2", "norwAI","results_manual_processing/norwAI_mistral2/", "norwAI2_processed")
    print("results_manual_processing/norwAI_mistral2/ FINISHED")
    
