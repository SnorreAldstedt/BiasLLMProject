import random
import json
from classes import Persona


def generate_personas_120():
    personas = []
    
    # Define three groups: (age_min, age_max, group_count)
    groups = [
        (18, 30, 40),
        (31, 50, 40),
        (51, 90, 40)  # Adjust the max age as needed
    ]
    
    for (age_min, age_max, group_count) in groups:
        
        # 10 male with kids, 10 male without kids
        male_with_kids = [("mann", True)] * 10
        male_without_kids = [("mann", False)] * 10
        
        # 10 female with kids, 10 female without kids
        female_with_kids = [("dame", True)] * 10
        female_without_kids = [("dame", False)] * 10
        
        gender_kids_pairs = (
            male_with_kids + male_without_kids +
            female_with_kids + female_without_kids
        )
        
        random.shuffle(gender_kids_pairs)
        
        # 2) Create a list of 40 occupations (4 categories, 25% each = 10 each)
        occupations_list = (
            ["I arbeid"] * 10 +
            ["student"] * 10 +
            ["arbeidsledig"] * 10 +
            ["pensjonert/uføretrygdet"] * 10
        )
        
        random.shuffle(occupations_list)
        
        # 3) Create 40 personas with the above distributions
        for i in range(group_count):
            gender, have_kids = gender_kids_pairs[i]
            occupation = occupations_list[i]
            age = random.randint(age_min, age_max)
            
            persona = Persona(
                age=age,
                gender=gender,
                have_kids=have_kids,
                occupation=occupation
            )
            personas.append(persona)
    
    return personas

#Generate personas and dump them into a json
personas = generate_personas_120()
personas_list=[]
for persona in personas:
    persona_dict = {
        "age": persona.age,
        "gender": persona.gender,
        "kids": persona.have_kids,
        "occupation": persona.occupation,
        "persona_str": persona.string_persona_norwegian()
    }
    personas_list.append(persona_dict)

with open('personas.json', 'w', encoding="utf-8") as f:
    json.dump(personas_list, f,ensure_ascii=False)