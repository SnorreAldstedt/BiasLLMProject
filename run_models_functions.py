
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import gc
import re
import json 
from classes import Persona
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
NR_OF_QUESTIONS = len(QUESTION_IDS)

def run_question_normistral(model, tokenizer, messages):
    torch.cuda.empty_cache()
    device = "cuda" # the device to load the model onto

    #model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16,
    #    device_map="auto")
    #tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

    print("Generating...")

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)

    model_inputs = encodeds.to(device)
    #model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=64, do_sample=True,  temperature = 0.1, repetition_penalty = 1.0, top_k = 64, top_p = 0.9)
    decoded = tokenizer.batch_decode(generated_ids)
    return (decoded[0])

def run_question_llama(model, tokenizer, messages):
    torch.cuda.empty_cache()
    device = "cuda" # the device to load the model onto

    terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")]

    print("Generating...")

    input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True).to(model.device)

    #model_inputs = encodeds.to(device)
    #model.to(device)

    generated_ids = model.generate(input_ids, max_new_tokens=128, do_sample=True,  temperature = 0.1, top_p = 0.9)
    response = generated_ids[0][input_ids.shape[-1]:]
    return (tokenizer.decode(response, skip_special_tokens=True))

def run_question_norwai_inst(model, tokenizer, prompt):
    torch.cuda.empty_cache()
    device = "cuda" # the device to load the model onto

    print("Generating...")

    #prompt = f"{instruction}\n\n{inst_input}\nSvar:" #Different prompt than the other models, reason is beacuse the documentation shows this as a pretrained prompt
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    generated_ids = model.generate(**inputs, 
                    max_new_tokens=100,
                    do_sample=True,
                    temperature=0.3)
    outputs = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return outputs


def remove_instruct_prompt(string):
    clean_string = re.sub(r"\[INST\][\s\S]*?\[/INST\]", "", string, flags=re.DOTALL)
    clean_string = clean_string.replace("<s>", "")
    clean_string = clean_string.replace("</s>", "")
    return clean_string

def load_json(dict_path=JSON_PATH):
    with open(dict_path, "r", encoding="utf-8") as d:
        data = json.load(d)

    return data

data = load_json()

def get_question_object(question_id, dictionary=data):
    return dictionary[question_id]

def get_question_from_object(question_object):
    return question_object["question"]

#Has to filter out values that ends with * (Because these were not shown to the participants, and values over 90.)
def get_options_from_object(question_object):
    options = question_object["alternatives"]
    filter_options = {}
    for k,v in options.items():
        v_str = v.strip()
        if v_str[-1] =="*":
            continue
        
        if int(k) >= 90:
            continue

        filter_options[k] = v

    options_str = ", ".join(f"{k}: {v}" for k,v in filter_options.items())
    
    return options_str


#for id in QUESTION_IDS:
#    print(get_question_from_object(get_question_object(id)))

def generate_question_prompt(question_id, question_dict=data):
    q_obj = get_question_object(question_id, question_dict)
    q = get_question_from_object(q_obj)
    o = get_options_from_object(q_obj)
    q_prompt = f"Du kan svare: '{o}'. {q}"
    return q_prompt

def combine_persona_question_prompt(persona_p, question_p):
    final_prompt = f"{persona_p}\n{question_p}"
    return final_prompt

def generate_messages(new_prompt, messages= []):
    user_dict = {
        "role": "user",
        "content": new_prompt
        }
    messages.append(user_dict) 
    return messages


def load_personas_from_json(json_path):
    personas_data = load_json(json_path)
    personas_list = []
    for persona_dict in personas_data:
        age = persona_dict["age"]
        gender = persona_dict["gender"]
        have_kids = persona_dict["kids"]
        occupation = persona_dict["occupation"]
        persona_str = persona_dict["persona_str"]

        persona = Persona(age, gender, have_kids, occupation, persona_str)
        personas_list.append(persona)

    return personas_list
