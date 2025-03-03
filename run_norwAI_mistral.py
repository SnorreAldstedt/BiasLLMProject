from classes import Persona
from run_models_functions import *

personas = load_personas_from_json("personas.json")
data = load_json()


tokenizer = AutoTokenizer.from_pretrained("NorwAI/NorwAI-Mistral-7B-instruct")
model = AutoModelForCausalLM.from_pretrained(
        "NorwAI/NorwAI-Mistral-7B-instruct", 
        torch_dtype=torch.bfloat16,
        load_in_8bit = True,
        device_map='balanced')

#persona_nr = 0
#start_persona = 45
start_persona = 4
total_personas = len(personas)
for persona_nr in range(start_persona, len(personas)):    
    print(f"{persona_nr}/{total_personas}")

    p_prompt = personas[persona_nr].persona_str
    q_nr = 0
    answers = {}

    for id in QUESTION_IDS:
        print(f"\t{q_nr}/{NR_OF_QUESTIONS}")
        q_prompt = generate_question_prompt(id)
        instruction=p_prompt
        inst_input=q_prompt
        prompt = f"{instruction}\n\n{inst_input}\nSvar:"

        return_string = run_question_norwai_inst(model, tokenizer, prompt)
        # Clean the string, remove the prompt from the returning string
        clean_string = return_string.replace(prompt, "")
        answers[id]=clean_string

        q_nr += 1
    filename = f"results/norwAI_mistral/{persona_nr}_norwAI.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(answers, f,ensure_ascii=False)
    #persona_nr += 1