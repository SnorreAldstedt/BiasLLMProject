from typing import Dict, List
import random

class Question:

    def __init__(self, code: str, question:str, options: Dict[int, str]):
        self.code = code
        self.question = question
        self.options = options

    def __str__(self):
        string = f"Code: {self.code},\nQuestion: {self.question},\nOptions: {self.options}"
        return string

    def return_code(self) -> str:
        return self.code
    
    def return_question(self) -> str:
        return self.question

    def return_options(self) -> Dict[int, str]:
        return self.options

    def return_option(self, key_value: int) -> str:
        return self.options[key_value]
    
    def set_category(self, category):
        self.category = category

    def return_category(self):
        return self.category
    
class Category:

    def __init__(self, category: str, questions: List[Question] = []):
        self.category = category
        self.questions = questions
    
    def __str__(self):
        category_str = self.category
        questions_str = ""
        for q in self.questions:
            questions_str += q.return_question()+'\n'+'\t'
        return f""" Category: {category_str} \n Questions: {questions_str}"""

    def return_category(self):
        return self.category
    
    def return_questions(self):
        return self.category
    
    def return_random_questions(self):
        copy_questions = self.questions[:]
        random.shuffle(copy_questions)
        return copy_questions
    
    def add_question(self, question):
        self.questions.append(question)

    def add_questions(self, questions):
        self.questions += questions
    
    def remove_question(self, question):
        self.questions.remove(question)

class Survey:

    def __init__(self, question_dict: Dict[str,Question] = {}):
        self.question_dict = question_dict

    def __str__(self):
        return_str = ""
        for q in self.question_dict.values():
            return_str+= q.__str__()+"\n"
        return return_str

    def return_question(self, code_key):
        self.question_dict[code_key].return_question()

    def return_options(self, code_key):
        self.question_dict[code_key].return_options()

    def add_question(self, question: Question):
        self.question_dict[question.return_code()] = question

    def remove_question(self, code_key):
        del self.question_dict[code_key]

class Persona:

    def __init__(self, age: int, gender:str, have_kids: bool, occupation: str):
        self.age = age
        self.gender = gender
        self.have_kids = have_kids
        self.occupation = occupation
    
    def create_persona_norwegian(self) -> str:
        alder = self.age
        kjonn = self.gender
        jobb = self.occupation
        barn = "barn" if self.have_kids else "ingen barn"
        persona_str = f"Du er en {kjonn} som er {alder} år, har {barn} og er {jobb}. \
Du skal svare på en spørreundersøkelse sånn som denne personen ville gjort. Svar bare ett alternativ."
        