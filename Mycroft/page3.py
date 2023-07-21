import streamlit as st
import pathlib
import os
import glob
import requests
import pdfplumber

st.set_page_config(page_title="Null And Nill", page_icon=":double_curly_loop:", layout="wide")

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #1C97F1;
        text-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
	st.title("Index")
	st.header("1. SHERLOCK")
	st.header("2. WATSON")
	st.header("3. MYCROFT")


st.title("MYCROFT")
st.text("Upload legal documents skimp through important details.")
with st.form(key="Form :", clear_on_submit = True):
	File = st.file_uploader(label = "", type=["pdf"])
	Submit = st.form_submit_button(label='Submit')

if Submit :
	st.markdown("**The file is sucessfully Uploaded.**")
	save_folder = 'Uploaded_Data'
	save_path = pathlib.Path(save_folder, File.name)
	with open(save_path, mode='wb') as w:
		w.write(File.getvalue())
	if save_path.exists():
		st.success(f'File {File.name} is successfully saved!')
	st.text("Processing")
	os.system(f'ocrmypdf {File.name} output.pdf --force-ocr')
	data=[]
	with pdfplumber.open('output.pdf') as pdf:
    		for i in range(len(pdf.pages)):
        		data.append(pdf.pages[i].extract_text(x_tolerance=2))
	os.remove("output.pdf")
	st.markdown(''.join(data))