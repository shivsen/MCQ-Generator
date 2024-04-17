import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.MCQ_generator.logger import logging

# Importing Langchain packages
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from src.MCQ_generator.utils import read_file, get_table_data

# Importing pypdf2 for the pdf related data
from PyPDF2 import PdfReader

#load environment variable from the .env fiile
load_dotenv()

KEY = os.getenv("OPENAI_API_KEY") #Accessing the env from the env file

llm = ChatOpenAI(api_key=KEY, model="gpt-3.5-turbo") #creating object of OpenAI


template = '''   
{data}
from the above text generate {no_of_ques}
MCQ Question related to {ques_related_to}.
and give a output in {format}'''   # Designing template for the quic generation

generate_quiz_prompt = PromptTemplate(
    input_variables=["data", "no_of_ques", "ques_related_to", "format"],
    template=template
) # prompt for the quiz generation

quiz_gen_chain = LLMChain(llm=llm, prompt=generate_quiz_prompt, output_key="quiz") #1st chain (quix generation)


template2 = '''
{quiz}
from the above mention quizes
check if there is any grammatical mistakes.
if you find any, correct it''' # 2nd tempolate for mistakes and evaluation

quiz_eval_prompt = PromptTemplate(
    input_variables=["quiz"],
    template=template2
) # prompt for the evaluation with the orignal daata

eval_chain = LLMChain(llm=llm, prompt=quiz_eval_prompt, output_key="final_content") # evaluatiing chain

# combining both chains
main_chain = SequentialChain(chains=[quiz_gen_chain, eval_chain],
                             input_variables=["data", "no_of_ques", "ques_related_to", "format"],
                             output_variables=  ["quiz", "final_content"])


