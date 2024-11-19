import torch
from abstract_llm_models import LanguageModel
from transformers import AutoModelForCausalLM, AutoTokenizer

#Need to install bitsandbytes and accelerate
class NoraLLM(LanguageModel):

    def __init__(self, model_name):
        # model variable can be changed depending on how much vram is available
        # this setup is taken from the documentation for normistral-7b-warm and needs ~8gb vram
        tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        # load_in_8bit=False -> 15gb VRAM
        # torch.float32 and load_in_8bit=False -> 21gb VRAM
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map = "auto",
            load_in_8bit = True,
            torch_dtype=torch.bfloat16

        )
        super().__init__(model_name, tokenizer, model)
    
