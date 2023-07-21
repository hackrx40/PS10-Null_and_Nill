import streamlit as st

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

	# Save uploaded file to 'F:/tmp' folder.
	save_folder = 'F:/tmp'
	save_path = Path(save_folder, File.name)
	with open(save_path, mode='wb') as w:
		w.write(File.getvalue())

	if save_path.exists():
		st.success(f'File {File.name} is successfully saved!')

