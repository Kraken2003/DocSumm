from model import create_summ
from  langchain import LLMChain, HuggingFacePipeline, PromptTemplate

def docsumm(model_id):

    
    pipeline = create_summ(model_id)

    llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})

    prompt_template = """
                Write a summary of the following text delimited by triple backticks.
                Return your response which covers the key points of the text.
                ```{text}```
                SUMMARY:
            """

    prompt = PromptTemplate(template=prompt_template, 
                            input_variables=["text"])
    
    summ_chain = LLMChain(prompt=prompt, llm=llm)

    return summ_chain
