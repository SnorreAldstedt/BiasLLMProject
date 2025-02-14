from classes import Persona
from run_models_functions import *

personas = load_personas_from_json("personas.json")
data = load_json()


model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16,
        device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
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
persona_nr = 0
total_personas = len(personas)
for persona in personas:    
    print(f"{persona_nr}/{total_personas}")

    p_prompt = persona.persona_str
    q_nr = 0
    answers = {}

    for id in QUESTION_IDS:
        print(f"\t{q_nr}/{NR_OF_QUESTIONS}")
        q_prompt = generate_question_prompt(id)
        prompt = combine_persona_question_prompt(p_prompt, q_prompt)
        template_messages = generate_messages(prompt, messages=[])

        return_string = run_question_normistral(model, tokenizer, template_messages)
        clean_string = remove_instruct_prompt(return_string)

        answers[id]=clean_string

        q_nr += 1
    filename = f"{persona_nr}_mistral.json"
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(answers, f,ensure_ascii=False)
    persona_nr += 1
