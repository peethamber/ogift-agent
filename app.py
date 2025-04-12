import streamlit as st
import anthropic
import base64
import httpx
from PyPDF2 import PdfFileReader
import os as os

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
api_key = st.secrets["ANTHROPIC_API_KEY"]

# Text Input

# save the input text in the variable 'name'
# first argument shows the title of the text input box
# second argument displays a default text inside the text input area

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file from list below', filenames)
    # return os.path.join(folder_path, selected_filename)
    return selected_filename
            
def gen_response(query):
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
  
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": query,
                }
            ]
        }
    ],
    )

    return(message.content[0].text)
# directory = './'

# st.title("List of Lesson Books ")
# for filename in os.listdir(directory):
#     if filename.endswith('.pdf'):
#         st.write(f"PDF File: {filename}")

# st.title("Ask Hari, The Expert  ")

# pdf = st.text_input("Enter name of any pdf document with extension from list above ")


pdf = file_selector()
st.write(" You selected ",pdf)

if(pdf and pdf.endswith('.Pdf')):
    with open(pdf.title(), "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")
query = st.text_input("Ask me anything from this book ")

# display the name when the submit button is clicked
# .title() is used to get the input text string
if(st.button('Submit')):
    if(query):
       st.write(gen_response(query))
    else:
       st.write("Empty Query String")
   
