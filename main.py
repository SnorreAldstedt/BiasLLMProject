import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import gc
#from llama_cpp import Llama
#IMPORTS

def test_llama_cpp_model():
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

def test_gen():
    tokenizer = AutoTokenizer.from_pretrained("norallm/normistral-7b-warm-instruct")
    model = AutoModelForCausalLM.from_pretrained("norallm/normistral-7b-warm-instruct", torch_dtype=torch.bfloat16)


    messages = [
        {"role": "user", "content": "Hva er hovedstaden i Norge?"},
        {"role": "assistant", "content": "Hovedstaden i Norge er Oslo. Denne byen ligger i den sørøstlige delen av landet, ved Oslofjorden. Oslo er en av de raskest voksende byene i Europa, og den er kjent for sin rike historie, kultur og moderne arkitektur. Noen populære turistattraksjoner i Oslo inkluderer Vigelandsparken, som viser mer enn 200 skulpturer laget av den berømte norske skulptøren Gustav Vigeland, og det kongelige slott, som er den offisielle residensen til Norges kongefamilie. Oslo er også hjemsted for mange museer, gallerier og teatre, samt mange restauranter og barer som tilbyr et bredt utvalg av kulinariske og kulturelle opplevelser."},
        {"role": "user", "content": "Gi meg en liste over de beste stedene å besøke i hovedstaden"}
    ]
    gen_input = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
    model.generate(
        gen_input,
        max_new_tokens=1024,
        top_k=64,  # top-k sampling
        top_p=0.9,  # nucleus sampling
        temperature=0.3,  # a low temparature to make the outputs less chaotic
        repetition_penalty=1.0,  # turn the repetition penalty off, having it on can lead to very bad outputs
        do_sample=True,  # randomly sample the outputs
        use_cache=True  # speed-up generation
    )

def test_model_norallm():
    torch.cuda.empty_cache()
    sentence  = 'Hello World!'
    device = "cuda:0"
    tokenizer = AutoTokenizer.from_pretrained("norallm/normistral-7b-warm-instruct")
    model = AutoModelForCausalLM.from_pretrained(
        "norallm/normistral-7b-warm-instruct", 
        torch_dtype=torch.bfloat16,
        load_in_8bit = True,
        device_map='auto')
    
    messages = [
        {"role": "user", "content": "Hva er hovedstaden i Norge?"},
        {"role": "assistant", "content": "Hovedstaden i Norge er Oslo."},
        {"role": "user", "content": "Gi meg en et eksempel på en av de beste stedene å besøke i hovedstaden"}
    ]
    gen_input = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
    gen_input = gen_input.to('cuda') 

    print("Generating...")
    start_timer = time.time()

    outputs =model.generate(
        gen_input,
        max_new_tokens=128,
        top_k=64,  # top-k sampling
        top_p=0.9,  # nucleus sampling
        temperature=0.3,  # a low temparature to make the outputs less chaotic
        repetition_penalty=1.0,  # turn the repetition penalty off, having it on can lead to very bad outputs
        do_sample=True,  # randomly sample the outputs
        use_cache=True  # speed-up generation
    )

    #print(outputs)
    #okenizer.decode(outputs[0])
    print(tokenizer.decode(outputs[0]))
    end_timer = time.time()
    print(end_timer-start_timer,"s to run the code")


def test_viking():
    device= "cuda:0"
    model = AutoModelForCausalLM.from_pretrained("PrunaAI/LumiOpen-Viking-7B-QUANTO-int4bit-smashed", trust_remote_code=True, device_map='auto')
    tokenizer = AutoTokenizer.from_pretrained("LumiOpen/Viking-7B")
    model = model.to(device)


    input_ids = tokenizer("What is the color of prunes?,", return_tensors='pt').to(model.device)["input_ids"]
    outputs = model.generate(input_ids, max_new_tokens=216)
    tokenizer.decode(outputs[0])
    print(tokenizer.decode(outputs[0]))

def test_llama():
    model_id ="meta-llama/Meta-Llama-3-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto")

    tokenizer.pad_token = tokenizer.eos_token

    #Manually defined chat template because the tokenizer doesnt have it
    tokenizer.chat_template = """<s>[INST]  {messages} [/INST]</s>"""


    messages = [
        {"role": "user", "content": "Hva er hovedstaden i Norge?"},
        {"role": "assistant", "content": "Hovedstaden i Norge er Oslo."},
        {"role": "user", "content": "Gi meg en et eksempel på en av de beste stedene å besøke i hovedstaden"}
    ]
    gen_input = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
    gen_input = gen_input.to('cuda') 

    print("Generating...")
    start_timer = time.time()

    #model.input_ids.to('cuda')

    outputs =model.generate(
        gen_input,
        max_new_tokens=128,
        top_k=64,  # top-k sampling
        top_p=0.9,  # nucleus sampling
        temperature=0.3,  # a low temparature to make the outputs less chaotic
        repetition_penalty=1.0,  # turn the repetition penalty off, having it on can lead to very bad outputs
        do_sample=True,  # randomly sample the outputs
        use_cache=True,  # speed-up generation
        pad_token_id = tokenizer.pad_token_id,
        attention_mask = torch.ones_like(gen_input)
    )

    #print(outputs)
    #okenizer.decode(outputs[0])
    print(tokenizer.decode(outputs[0]))
    end_timer = time.time()
    print(end_timer-start_timer,"s to run the code")    

def test_llama_pipe():
    model_id = "meta-llama/Meta-Llama-3-8B"
    pipe = pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")

    context = "Du er en hjelpsom assistent som svarer på spørsmål"
    question = "Hva er hovedstaden i Oslo"
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"

    newline_token_id = pipe.tokenizer("\n", add_special_tokens=False)["input_ids"][0]

    print("Generating...")
    start_timer = time.time()
    response = pipe(prompt, do_sample=True, pad_token_id=pipe.tokenizer.eos_token_id, eos_token_id = newline_token_id, max_new_tokens = 50)
    print(response)

    end_timer = time.time()
    print(end_timer-start_timer,"s to run the code")

def test_mistral_pipe():
    model_id = "mistralai/Mistral-7B-v0.1"
    pipe = pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")

    context = "Du er en hjelpsom assistent som svarer på spørsmål"
    question = "Hva er hovedstaden i Oslo"
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"

    newline_token_id = pipe.tokenizer("\n", add_special_tokens=False)["input_ids"][0]

    print("Generating...")
    start_timer = time.time()
    response = pipe(prompt, do_sample=True, pad_token_id=pipe.tokenizer.eos_token_id, eos_token_id = newline_token_id, max_new_tokens = 50)
    print(response)

    end_timer = time.time()
    print(end_timer-start_timer,"s to run the code")

if __name__ == "__main__":
    #Empty cache, RAM, memomry etc.
    torch.cuda.empty_cache()
    gc.collect()
    torch.cuda.ipc_collect()


    print("Running main.py")
    test_mistral_pipe()
    #test_gen()
    #test_llama_cpp_model()
    #repo_test_input = input("1 for normistral-7b-warm-instruct, 2 for normistral-7b-warm: ")