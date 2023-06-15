import streamlit as st
from PyPDF2 import PdfReader
from example_context import exContext
import pyautogui
from transformers import pipeline

def main():
    st.set_page_config(page_title='Chatbot | A .pmWEB creation.', layout='wide')
    st.header('Welcome to your personal chatbot 🗣️')
    st.caption('Sourced at heylightning/chatpy-huggingface on GitHub.')
    st.caption('A .pmWEB creation.')
    st.subheader("Choose your context mode:")
    pdfTab, textTab, exampleTab = st.tabs(["Use PDF", "Use Text", "Example"])

    # For pdfTab
    pdf = pdfTab.file_uploader("Upload your PDF file here:", type='pdf')
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        pdfContext = ""
        for page in pdf_reader.pages:
            pdfContext += page.extract_text()
        pdfTab.caption("Here is the content of your file: (Only the first 2500 characters)")

        if(len(pdfContext) >= 2500):
            pdfContext = pdfContext[: 2501]
        pdfTab.write(pdfContext)

        pdfTab.divider()
 
        pdfContextQuestion = pdfTab.text_input("Ask a question❔", key=f'pdfCQ', placeholder='Ask me anything (as long as it is in your context 😉)')
        if pdfTab.button('Compute', key='textBTN'):
            question_answer = pipeline('question-answering', model='deepset/roberta-base-squad2')
            res = question_answer(
                question = pdfContextQuestion,
                context = pdfContext
            )
            pdfTab.write("Answer: " + res['answer'])
            pdfTab.write("Accuracy score: " + str(res['score']*100) + " %")
        if pdfTab.button('Another Context', key='textTabAC'):       
            pyautogui.hotkey('ctrl', 'r')

    # For textTab
    textContext = textTab.text_area("Write / Paste your context here:", placeholder='Check out the Example tab!')

    if len(textContext) > 2:
        textTab.caption("Here is the content of your file: (Only the first 2500 characters)")
        if(len(textContext) >= 2500):
            textContext = textContext[: 2501]
        textTab.write(textContext)

        textTab.divider()

        textContextQuestion = textTab.text_input("Ask a question❔", key='textCQ', placeholder='Ask me anything (as long as it is in your context 😉)')
        if textTab.button('Compute', key='textBTN'):
            question_answer = pipeline('question-answering', model='deepset/roberta-base-squad2')
            res = question_answer(
                question = textContextQuestion,
                context = textContext
            )
            textTab.write("Answer: " + res['answer'])
            textTab.write("Accuracy score: " + str(res['score']*100) + "%")
        if textTab.button('Another Context', key='textTabAC'):
            pyautogui.hotkey('ctrl', 'r')

    # For exampleTab
    exampleTab.subheader("Use the following text as an example to text context 💬")
    exampleTab.write(exContext)

if __name__ == '__main__':
    main()