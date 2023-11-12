import os
import openai
import streamlit as st

from PyPDF2 import PdfReader
from pptx import Presentation
import docx
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import glob
import time



def extract_text_from_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    raw_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text = raw_text + content

    return raw_text

def extract_text_from_pptx(pptx_file):

    raw_text = ""
    prs = Presentation(pptx_file)

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text=shape.text
                raw_text = raw_text + text
    
    return raw_text

def extract_text_from_docx(docx_file):

    doc = docx.Document(docx_file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def extract_text_from_JPG(JPG_file):

    image = Image.open(JPG_file)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    raw_text = image_to_string(image,lang='eng')
    return raw_text

session_state = st.session_state
if "api_key" not in session_state:
    session_state = None

def is_valid_openai_key(api_key):
    openai.api_key = api_key

    try:
        response = openai.Engine.list()
        if response and 'text' in response:
            return True
    except openai.error.OpenAIError as e:
        if "Authentication" in str(e):
            return False
    return False

@st.cache_data
def get_response(text):

    prompt = f"""
            You are an expert in summarizing Documents. You will be given a Document delimited by four backquotes, 
            make sure to capture the main points, key arguments, and many supporting evidence presented in the article.
            your summary should be informative and well-structured, ideally consisting of 3-5 sentences.

            text: ''''{text}''''
            """
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {
                "role" : "system",
                "content" : prompt,
            },
        ],

    )
    return response ["choices"][0]["message"]["content"]

def main():
    st.set_page_config(
        page_title = "Summarizer",
        page_icon = "📒",
         layout="wide",
    )

    st.title("📒Welcome to the AI-summarizer website.")
    st.subheader("This website uses :blue[OpenAI]'s GPT-3.5 turbo to summarize a given Document.")
    st.divider()
    st.markdown(":red[**Notice**] : **Do not** enter sensitive data. Data entered will be sent to OpenAI servers to be further processed.")
    st.divider()
    st.markdown("**First step**: Please enter OpenAI key.")
    st.markdown("**Hint**, the following link should help you in obtaining your key: https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt")
    api_key = st.text_input('OpenAI key', placeholder = 'Your key should be inserted here.',type="password")
    st.divider()
    st.markdown("**Second step**: Choose format and insert a file to summarize it.")
    option = st.radio("Select Input Type",("Text","Image","PDF", "Word","PowerPoint"))
    if is_valid_openai_key(api_key):
        if option == "Text":

            user_input = st.text_area("Enter Text", placeholder = "Enter some paragraphs to sammarize it.")

            if st.button("Submit") and user_input !="":

                progress_text = "In progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()

                response = get_response(user_input)
                st.success("done!")
                st.subheader("Summary")
                st.markdown(f"> {response}")
            else:
                st.error("Please enter some text.")

        elif option == "Image":
            uploaded_file = st.file_uploader("Choose a JPG file",type="jpg")

            st.divider()

            if st.button("Submit") and uploaded_file is not None:
                text = str(extract_text_from_JPG(uploaded_file))

                progress_text = "In progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()

                response = get_response(text=text)
                st.success("done!")
                st.subheader("Summary")
                st.markdown(f"> {response}")
            else:
                st.error("Please upload a JPG file.")

        elif option == "PDF":
            uploaded_file = st.file_uploader("Choose a PDF file",type="PDF")
        
            st.divider()

            if st.button("Submit") and uploaded_file is not None:
                text = extract_text_from_pdf(uploaded_file)

                progress_text = "In progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()

                response = get_response(text=text)
                st.success("done!")
                st.subheader("Summary")
                st.markdown(f"> {response}")
            else:
                st.error("Please upload a PDF file.")

        elif option == "Word":
            uploaded_file = st.file_uploader("Choose a Word file",type="docx")

            if st.button("Submit") and uploaded_file is not None:
                text = extract_text_from_docx(uploaded_file)

                progress_text = "In progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()

                response = get_response(text=text)
                st.success("done!")
                st.subheader("Summary")
                st.markdown(f"> {response}")
            else:
                st.error("Please upload a Word file.")

        elif option == "PowerPoint":
            uploaded_file = st.file_uploader("Choose a Powerpoint file",type="pptx")

            st.divider()

            if st.button("Submit") and uploaded_file is not None:
                text = extract_text_from_pptx(uploaded_file)

                progress_text = "In progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()

                response = get_response(text=text)
                st.success("done!")
                st.subheader("Summary")
                st.markdown(f"> {response}")
            else:
                st.error("Please upload a Powerpoint file.")
    else:
        st.error("Please provide a key.")

    st.divider()

    github_link = "https://github.com/MAlsultan1"
    twitter_link = "https://twitter.com/Mish3l809"
    github_logo = "https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Github-16.png"
    twitter_logo = "https://cdn4.iconfinder.com/data/icons/social-media-black-white-2/1227/X-16.png"

    html = f"""
    <ul style="list-style-type: none; padding-left: 0;">
        <li><a href="{github_link}" target="_blank"><img src="{github_logo}" width="20" height="20"/> GitHub</a></li>
        <li><a href="{twitter_link}" target="_blank"><img src="{twitter_logo}" width="20" height="20"/> X(Twitter)</a></li>
    </ul>
    """
    st.subheader("follow me on:")
    st.markdown(html, unsafe_allow_html=True)

    st.caption('Made by Meshal Alsultan')
    st.caption('v1.0')     

if __name__ == "__main__":
    main() 