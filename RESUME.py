import streamlit as st 
import pandas as pd
import base64, random 
import time, datetime 

import spacy
import nltk
nltk.data.path.append("C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python38\\nltk_data")
from nltk.corpus import stopwords
nltk.download('stopwords')

# Load the default English language model (small version)
nlp = spacy.load('en_core_web_sm')


#libraries to parse the resume pdf files
from pyresparser import ResumeParser   #esumeParser class from the pyresparser module.
from pdfminer3.layout import LAParams, LTTextBox 
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io, random 
from streamlit_tags import st_tags
from PIL import Image
import pymysql 
# import pafy
import plotly.express as px


st.set_page_config(
    page_title="AI CV Job Recommendation"
)

# connecting to database 
def pdf_reader(file):
    res_manager = PDFResourceManager()
    file_handler = io.StringIO()
    converter = TextConverter(res_manager, file_handler, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(res_manager, converter)
    fh = open(file, 'rb')
    for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
        page_interpreter.process_page(page)
        print(page)
    text = file_handler.getvalue()
    converter.close()
    file_handler.close()
    return text

def start():
    logo = Image.open('jpg.jpg')
    logo = logo.resize((500,400))
    st.image(logo)

    st.title("UPLOAD YOUR CV TO GET JOB RECOMMENDATION")

    pdf_file = st.file_uploader("choose your CV", type=["pdf"])
    if pdf_file is not None:
        with st.spinner("Uploading your CV ..."):
            time.sleep(4)
    save_image_path = "./Resume/Uploaded_Resume/" + pdf_file.name
    if hasattr(pdf_file, 'name'):
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
    else:
        st.error("Uploaded file has no name attribute.")
else:
    st.error("No file was uploaded.")
        
            #getting data from cv
        cv_data= ResumeParser(save_image_path).get_extracted_data()
        if cv_data:
            cv_content = pdf_reader(save_image_path)

            st.header("CV Analysis")
            st.success("Hello" + cv_data["name"])
            
            try:
                # st.success("Hello "+ cv_data["name"])
                st.text(cv_data["mobile_number"])
                # st.text(cv_data["degree"])
                # st.text(cv_data["experience"])
                st.text(cv_data["skills"])
                # st.text(cv_data["total_experience"])
                # st.text(cv_data["no_of_pages"])
            except:
                pass

            experience_level = 0 # initialization
            if cv_data["no_of_pages"] == 1:
                experience_level = "Fresher"
            elif cv_data["no_of_pages"] == 2:
                experience_level = "Intermediate"
            elif cv_data["no_of_pages"] >= 3:
                experience_level = "Experienced"
            else:
                experience_level = "Yet to start"
            
            st.text("You fall under category of someone who is " + experience_level)

        # recommend career
        #keywords = st_tags(label = "You current skills are")
        for i in cv_data["skills"]:
            if i.lower() in ["Coding", "Python", "mySQL", "Programming", "html", "css", "Javascript", "Software"]:
                st.text(i.lower())
                st.text("Recommended job: Data Science, Software development, Frontend development, backend")

            elif i.lower() in ["Engineering", "Construction", "Architect", "Architecture", "Building"]:
                print(i.lower())
                st.text("Recommended job: Architecture, Civil Engineering")

            elif i.lower() in ["Care giving", "Health", "Bioinformatics", "Caring"]:
                print(i.lower())
                st.text("Recommended job: Medicine, Nursing, Microbiology")

            elif i.lower() in ["Law, Justice, Freedom"]:
                print(i.lower())
                st.text("Recommended job: Law, Political science")

            elif i.lower() in ["Traveling", "Hospitality", "scheduling"]:
                print(i.lower())
                st.text("Recommended job: Hotel management, Aviation")
            elif i.lower() in ["Meeting people", "Sales", "warehouse", "Marketing"]:
                print(i.lower())
                st.text("Recommended job: sales, marketing, entreprenuer, business")
            elif i.lower() in ["Entertainment", "Music", "Sport", "Art"]:
                print(i.lower())
                st.text("Recommended job: Music, sport analyst, coaching, comedy, acting")
            elif i.lower() in ["Finance", "Numbers", "Data", "Yrchnical", ""]:
                print(i.lower())
                st.text("Recommended job: Accounting, data analyst, financial analyst")
                


start()

