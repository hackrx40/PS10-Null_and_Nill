import streamlit as st
import pathlib
import os
import glob
import requests
import pdfplumber
import sys
from streamlit_extras.switch_page_button import switch_page
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma


st.set_page_config(page_title="Null And Nill", page_icon=":double_curly_loop:", layout="wide")

os.environ["OPENAI_API_KEY"] = "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"

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  loader = DirectoryLoader("/home/pranav/Desktop/data/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

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
	st.header("2. MYCROFT")


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
	st.text("Processing...")
	os.system(f'ocrmypdf {File.name} output.pdf --force-ocr')
	data=[]
	with pdfplumber.open('output.pdf') as pdf:
    		for i in range(len(pdf.pages)):
        		data.append(pdf.pages[i].extract_text(x_tolerance=2))
	os.remove("output.pdf")
	#st.markdown(''.join(data))
	
	file1 = open("Uploaded_Data/Database.txt","a")
	file1.writelines(data)
	file1.close()
	result = chain({"question": "What is the context of the document", "chat_history": chat_history})
	st.markdown("The context of the document is-")
	st.markdown(result['answer'])
if st.button('Upload More Docs'):
	pass

#askme = st.button("Ask Me Anything")
#if askme:
    #switch_page("Contribute")
