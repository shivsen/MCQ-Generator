import os
import traceback
import PyPDF2
import json

# function for read pdf and text file

def read_file (file):
    if file.name.endswith(".pdf"):
        try:
            pages = PyPDF2.PdfReader(file)
            text=""
            for i in range(len(pages.pages)):
                text+= pages.pages[i].extract_text()
            return text
        except Exception as e:
            raise Exception("pdf file not readed")
        
    elif  file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        
    else:
        raise Exception("Unsupported Format")


def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " | ".join([
                    f"{option} -> {option_value}" for option, option_value in value["options"].items()
               ])

            correct=value["correct"]
            quiz_table_data.append({"MCQ" : mcq, "Choices" : options, "Correct" : correct})
            
        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
     