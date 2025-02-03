import torch
from abstract_llm_models import LanguageModel
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

#Need to install bitsandbytes and accelerate
class LLM_Class:

    def __init__(self, model_name: str, model: AutoModelForCausalLM, tokenizer: AutoTokenizer, gen_config: GenerationConfig = None):
        
        self.modelname = model_name
        self.model = model
        self.tokenizer = tokenizer
        self.gen_config = gen_config

    def set_generation_config(self, config):
        self.gen_config = config
    
    def generate_answer(self, input, gen_config: GenerationConfig):
        gen_input = self.tokenizer.apply_chat_template(input, add_generation_prompt=True, return_tensors="pt")
        outputs = self.model.generate(gen_input, gen_config)

        return self.tokenizer.decode(outputs[0])
