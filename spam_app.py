import pickle
import streamlit as st
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import sys
if sys.platform == "win32":
    import win32api  # part of pywin32


nltk.download('punkt')
nltk.download('stopwords')
stopwords.words('english')

string.punctuation 

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y.copy()
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    
    text = y.copy()
    y.clear()
    
    for i in text:
        y.append(PorterStemmer().stem(i))
        
    return ' '.join(y)

# --- Streamlit Config ---
st.set_page_config(page_title="📧 Spam Email Classifier", layout="centered")
st.title("📧 Spam Email Classifier")
st.markdown("### Paste your email content below to classify it as Spam or Not Spam.")
# --- Load Model & Vectorizer ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))
    st.success("✅ Model and vectorizer loaded.")
except Exception as e:
    st.error(f"❌ Load Error: {e}")
    st.stop()
# --- User Input Widget ---
email_content = st.text_area("Email Content", height=300, placeholder="Paste your email content here...")

if st.button("🔍 Classify Email"):
    if not email_content.strip():
        st.error("❌ Please enter some email content.")
        st.stop()
    
    # Transform and vectorize the input

    transform_sms = transform_text(email_content)
    vector_input = vectorizer.transform([transform_sms])
    result = model.predict(vector_input)[0]
    if result == 1:
        st.success("✅ This email is classified as **Spam**.")

    else:
        st.success("✅ This email is classified as **Not Spam**.")