from classes import Persona
from run_models_functions import *

personas = load_personas_from_json("personas.json")
data = load_json()


tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3-8B-Instruct", 
        torch_dtype=torch.bfloat16,
        load_in_8bit = True,
        device_map='auto')

#persona_nr = 0
#start_persona = 45
start_persona = 0
total_personas = len(personas)
for persona_nr in range(start_persona, len(personas)):    
    print(f"{persona_nr}/{total_personas}")

    p_prompt = personas[persona_nr].persona_str
    q_nr = 0
    answers = {}

    for id in QUESTION_IDS:
        print(f"\t{q_nr}/{NR_OF_QUESTIONS}")
        q_prompt = generate_question_prompt(id)
        prompt = combine_persona_question_prompt(p_prompt, q_prompt)
        template_messages = generate_messages(prompt, messages=[])

        return_string = run_question_llama(model, tokenizer, template_messages)
        #respond_string = return_string.split("<|im_start|> assistant")[-1]
        #clean_string = remove_instruct_prompt(respond_string)

        answers[id]=return_string

        q_nr += 1
    filename = f"results/llama3_2/{persona_nr}_llama3.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(answers, f,ensure_ascii=False)
    #persona_nr += 1