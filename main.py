import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_cpp import Llama

if __name__ == "__main__":
    #repo_test_input = input("1 for normistral-7b-warm-instruct, 2 for normistral-7b-warm: ")
    print("Running main.py")
    #if repo_test_input == "1":
    #    repo_id_name="norallm/normistral-7b-warm-instruct",  # HuggingFace repository containing the GGUF files.
    #else:
    #    repo_id_name="norallm/normistral-7b-warm",
    llm = Llama.from_pretrained(
          # HuggingFace repository containing the GGUF files.
        repo_id="norallm/normistral-7b-warm-instruct",  # HuggingFace repository containing the GGUF files.
        filename="*Q4_K_M.gguf", # suffix of the filename containing the level of quantization. 
        n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
        n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
        n_gpu_layers=35         # The number of layers to offload to GPU, if you have GPU acceleration available
    )

    # Simple inference example
    output = llm(
  """<s><|im_start|> user
Hva kan jeg bruke einstape til?<|im_end|>
<|im_start|> assistant
""", # Prompt
        max_tokens=512,  # Generate up to 512 tokens
        stop=["<|im_end|>"],   # Example stop token
        echo=True,       # Whether to echo the prompt
        temperature=0.3  # Temperature to set, for Q3_K_M, Q4_K_M, Q5_K_M, and Q6_0 it is recommended to set it relatively low.
    )

    # Chat Completion API

    llm.create_chat_completion(
        messages = [
            {
                "role": "user",
                "content": "Hva kan jeg bruke einstape til?"
            }
        ]
    )



