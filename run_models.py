
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import gc
import re
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

def run_question_normistral(model, tokenizer, messages):
    torch.cuda.empty_cache()
    device = "cuda" # the device to load the model onto

    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16,
        device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

    print("Generating...")

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)

    model_inputs = encodeds.to(device)
    #model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=64, do_sample=True,  temperature = 0.3, repetition_penalty = 1.0, top_k = 64, top_p = 0.9)
    decoded = tokenizer.batch_decode(generated_ids)
    return (decoded[0])

def remove_instruct_prompt(string):
    clean_string = re.sub(r"\[INST\][\s\S]*?\[/INST\]", "", string, flags=re.DOTALL)
    clean_string = clean_string.replace("<s>", "")
    clean_string = clean_string.replace("</s>", "")
    return clean_string

def return_dict_json(dict_path=JSON_PATH):
    with open(dict_path, "r", encoding="utf-8") as d:
        data = json.load(d)

    return data

data = return_dict_json()

def get_question_object(question_id, dict=data):
    return data[question_id]

def get_question_from_object(question_object):
    return question_object["question"]

def get_options_from_object(question_object ):
    return question_object["alternatives"]

def get_question_object(question_id, dictionary=data):
    return data[question_id]

for id in QUESTION_IDS:
    print(get_question_from_object(get_question_object(id)))

def generate_question_prompt(question_id, question_dict=JSON_PATH):
    return None

test_messages = [
        #{
        #    "role": "system",
        #    "content": "Du er en kvinne som er 25 år, har ingen barn og er student som skal svare på en spørreundersøkelse. Svar bare ett alternativ."
        #},
        {
            "role": "user",
            "content": "Du er en kvinne som er 25 år, har ingen barn og er student som skal svare på en spørreundersøkelse. Svar bare ett alternativ.\
Du kan svare: 1 'helt enig', 2 'nokså enig', 3 'både og', 4 'nokså uenig, 5 'helt uenig'. EØS-avtalen bør sies opp"
        }
    ]
#return_string = run_question_normistral(model=None, tokenizer = None, messages=test_messages)
#clean_string = remove_instruct_prompt(return_string)
#print(clean_string)
