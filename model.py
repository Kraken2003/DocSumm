# Defining two functions for creating language model pipelines for document summarization and query generation.
# The create_summ function takes a model ID as input and returns a Hugging Face pipeline for generating summaries of documents.
# The create_query function takes a model ID as input and returns a Hugging Face pipeline for generating queries.

import torch
import transformers
from transformers import AutoTokenizer

def create_summ(model):
    model_id = model
    summ_pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    tokenizer=AutoTokenizer.from_pretrained(model_id),
    torch_dtype=torch.bfloat16,
    max_length=3000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id = AutoTokenizer.from_pretrained(model_id).eos_token_id
    
    )
    
    return summ_pipeline

def create_query(model):    

    model_id = model

    model_config = transformers.AutoConfig.from_pretrained(
        model_id,
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        config=model_config,
        device_map='auto')
    
    query_pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=AutoTokenizer.from_pretrained(model_id),
            torch_dtype=torch.float16)
    
    return query_pipeline
