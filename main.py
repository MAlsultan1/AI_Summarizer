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

st.set_page_config(
    page_title="Summarizer",
    page_icon="📒",
    layout="wide",
)


session_state = st.session_state


if "api_key" not in session_state:
    session_state.api_key = None


# ? Check if the provided OpenAI API key is valid
def is_valid_openai_key(api_key):
    """Check if the provided OpenAI API key is valid."""
    openai.api_key = api_key
    try:
        # ! Make a test call. Here we'll list available engines, which is a lightweight call.
        response = openai.Engine.list()
        if response and 'data' in response:
            return True
    except openai.error.OpenAIError as e:
        # ! Handle specific authentication error
        if "Authentication" in str(e):
            return False
    return False


# ? If API key has not been set, show the input
if not session_state.api_key:
    st.title("📒Welcome to AI summarizer website.")
    st.write("Please enter your OpenAI API key to begin:")
    temp_key = st.text_input("OpenAI API Key:", type="password")
    api_key_url = "https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt"
    html_code = f"""
    <ul style="list-style-type: none; padding-left: 0;">
    <li>Need an API key? <a href="{api_key_url}" target="_blank">Learn how to obtain one here.</a></li>
    </ul>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    if st.button("Submit"):
        if len(temp_key) < 20:
            st.error("The API key seems too short. Please recheck.")
        else:
            if is_valid_openai_key(temp_key):
                session_state.api_key = temp_key
                st.experimental_rerun()
            else:
                st.error("The provided API key is invalid. Please recheck.")


if session_state.api_key:
    @st.cache_data
    def get_response(text):

        prompt = f"""
            You are an expert in summarizing Documents. You will be given a Document delimited by four backquotes, 
            make sure to capture the main points, key arguments, and many supporting evidence presented in the article.
            your summary should be informative and well-structured, ideally consisting of 3-5 sentences.

            text: ''''{text}''''
            """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],

        )
        return response["choices"][0]["message"]["content"]

else:
    st.error("Please provide a valid API key.")


def main():

    st.divider()
    st.markdown(
        "**Second step**: Choose format and insert a file to summarize it.")
    option = st.radio("Select Input Type",
                      ("Text", "Image", "PDF", "Word", "PowerPoint"))

    if option == "Text":

        user_input = st.text_area(
            "Enter Text", placeholder="Enter some paragraphs to sammarize it.")

        if st.button("Submit", key=12) and user_input != "":

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
        uploaded_file = st.file_uploader("Choose a JPG file", type="jpg")

        st.divider()

        if st.button("Submit") and uploaded_file is not None:
            text = extract_text_from_JPG(uploaded_file)

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
        uploaded_file = st.file_uploader("Choose a PDF file", type="PDF")

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
        uploaded_file = st.file_uploader("Choose a Word file", type="docx")

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
        uploaded_file = st.file_uploader(
            "Choose a Powerpoint file", type="pptx")

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
                text = shape.text
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
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'
    raw_text = image_to_string(image, lang='eng')
    return raw_text


if __name__ == "__main__":
    main()