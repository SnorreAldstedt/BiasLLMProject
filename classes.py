from typing import Dict, List
import random

class Question:

    def __init__(self, code: str, question:str, options: Dict[int, str]):
        self.code = code
        self.question = question
        self.options = options

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

    def __init__(self, category: str, questions: List[Question]):
        self.category = category
        self.questions = questions
    
    def return_category(self):
        return self.category
    
    def return_questions(self):
        return self.category
    
    def return_random_questions(self):
        copy_questions = self.questions[:]
        random.shuffle(copy_questions)
        return copy_questions
    

class Survey:

    def __init__(self, question_dict: Dict[str,Question] = {}):
        self.question_dict = question_dict

    def return_question(self, code_key):
        self.question_dict[code_key].return_question()

    def return_options(self, code_key):
        self.question_dict[code_key].return_options()

    def add_question(self, question: Question):
        self.question_dict[question.return_code()] = question
        