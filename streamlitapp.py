import json, os, traceback
import pandas as pd
from dotenv import load_dotenv
from src.MCQ_generator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.MCQ_generator.Mcq_generator import main_chain
from src.MCQ_generator.logger import logging


with open ("G:/Projetcs/Github/MCQ Generator with langchain and OpenAI/response.json", "r") as file:
    RESPONSE_JSON = json.load(file)  # load json file


st.title("MCQ Generator (Using OPEN AI )")

with st.form("user_inputs"):

    uploaded_file = st.file_uploader("Upload file (Only single pdf file or text file will be accepted")

    mcq_count = st.number_input("Number of questions required.", min_value=3, max_value=10)

    Subject = st.text_input("Subject of the MCQ's")

    button = st.form_submit_button("Create")

    if button and uploaded_file is not None and mcq_count and Subject:
        with st.spinner("loading"):

            try:
                text = read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response=main_chain(
                        {
                            "data": text,
                            "no_of_ques": mcq_count,
                            "ques_related_to": Subject,
                            "format": json.dumps(RESPONSE_JSON)
                        }
                        )
                
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("error")

            else:
                print(f'Total Token Used {cb.total_tokens}')
                print(f'Total Cost Involved : {cb.total_cost}')
                

                if isinstance(response, dict):

                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)


                            st.text_area(label = "final_content", value=response["final_content"])
                        else:
                            st.error("Error in the table data")
                
                else:
                    st.write(response)


                     

