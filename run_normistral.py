from classes import Persona
from run_models_functions import *

personas = load_personas_from_json("personas.json")
data = load_json()


tokenizer = AutoTokenizer.from_pretrained("norallm/normistral-7b-warm-instruct")
model = AutoModelForCausalLM.from_pretrained(
        "norallm/normistral-7b-warm-instruct", 
        torch_dtype=torch.bfloat16,
        load_in_8bit = True,
        device_map='auto')
"""
test_persona = personas[0]
test_id = QUESTION_IDS[0]

p_prompt = test_persona.persona_str
q_prompt = generate_question_prompt(test_id, data)
prompt = combine_persona_question_prompt(p_prompt, q_prompt)
messages = generate_messages(prompt)
print(messages)
return_string = run_question_normistral(model, tokenizer, messages)
clean_string = remove_instruct_prompt(return_string)

print(clean_string)


"""
#persona_nr = 0
#start_persona = 45
start_persona = 115
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

        return_string = run_question_normistral(model, tokenizer, template_messages)
        respond_string = return_string.split("<|im_start|> assistant")[-1]
        clean_string = remove_instruct_prompt(respond_string)

        answers[id]=clean_string

        q_nr += 1
    filename = f"results/normistral/{persona_nr}_normistral.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(answers, f,ensure_ascii=False)
    #persona_nr += 1
