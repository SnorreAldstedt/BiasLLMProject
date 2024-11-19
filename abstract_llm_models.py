from abc import ABC, abstractmethod
from transformers import AutoModelForCausalLM, AutoTokenizer


class LanguageModel(ABC):
    '''An abstract class representing a language-model
    
    The class should be a base for the language models used in this project. 
    The class should be extended for each specific model, 
    and the methods should be overwritten if not compatible with the model

    Attributes:
        model_name (str): Name of the model (can be from huggingface)
        tokenizer: (optional) An tokenizer instance. If not provided, 
                    it will be loaded from huggingface using the model name.
        model: (optional) An model instance. If not provided, it will be loaded from the model name.
    '''
    # Should be overwritten if the model is not from huggingface
    def __init__(self, model_name: str, tokenizer=None, model=None):
        self.model_name = model_name

        if tokenizer == None:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        else:
            self.tokenizer = tokenizer

        if model == None:
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
        else:
            self.model = model

    def __str__(self):
        return self.model_name
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        pass

    def tokenize_input(self, text:str):
        return self.tokenizer(text, return_tensors="pt")

