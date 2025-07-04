import streamlit as st
from summarizer import TextSummarizer

# create TextSummarizer instance  
summarizer = TextSummarizer()


st.title("Text Summarization Tool")
st.write("Enter text or a URL to generate a summary. Choose the desired summary length.")


input_method = st.radio("Select input method:", ("Text", "URL"))
summary_length = st.selectbox("Select summary length:", ["Short", "Medium", "Long"])

# ensures session variables are available
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# show textarea for input 
if input_method == "Text":
    input_text = st.text_area("Enter text to summarize:", height=200)
else:
    input_text = st.text_input("Enter URL to summarize:", placeholder="https://example.com")


if st.button("Summarize"):
    if input_text:
        with st.spinner("Generating summary..."):
            if input_method == "URL":
                extracted_text = summarizer.extract_text_from_url(input_text) # extract text from provided URL 
                if "Error" in extracted_text:
                    st.error(extracted_text)
                else:
                    # store and summarize the extract text from URL
                    st.session_state.input_text = extracted_text
                    st.session_state.summary = summarizer.summarize_text(extracted_text, summary_length.lower())
            else:
                # store and summarize the extract text from given text input
                st.session_state.input_text = input_text
                st.session_state.summary = summarizer.summarize_text(input_text, summary_length.lower())
    else:
        st.error("Please provide text or a valid URL.")

# display input text and summary
if st.session_state.input_text:
    st.subheader("Input Text")
    st.write(st.session_state.input_text[:1000] + ("..." if len(st.session_state.input_text) > 1000 else ""))

if st.session_state.summary:
    st.subheader("Summary")
    st.write(st.session_state.summary)