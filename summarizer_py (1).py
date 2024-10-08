# -*- coding: utf-8 -*-
"""summarizer.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YZxLzaR4o9gnBPdICtJkN8sBz0uAqtP0

Installing the Dependencies
"""

from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk import sent_tokenize
nltk.download('punkt')
!pip install transformers
from transformers import pipeline

!pip install Streamlit

import streamlit as st

st.title("Wikipedia Summary Generator")

title = st.text_input("Wikipedia page link", "Life of Brian")
st.write("Your wiki summary is here...")

headers = {"User_Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}

web = requests.get(title, headers=headers)
web

wiki_content = BeautifulSoup(web.content, "html.parser")
wiki_content.get_text(strip=True)

paras = wiki_content.find_all("p")

for p in paras:
  p.get_text()

text = str(paras)

tokens = sent_tokenize(text)
type(tokens)

tokens[0]

def remove_html_tags(text):
    # clean = re.compile("""<.*?>\[\\\""")
    clean = re.compile(r'<.*?>|\[.*?\]|\[.*?$|^.*?\]$|\n')
    return re.sub(clean, '', text)

# Remove HTML tags from each string in the list
clean_texts = [remove_html_tags(text) for text in tokens]

print(clean_texts)

Content = str(clean_texts)

print(f"total number of sentences is {len(clean_texts)}")

"""Text Summarization"""

# Load the summarization pipeline
model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization", model=model_name)

chunk_size = 500
overlap = 30

# Initialize chunk indices
start = 0
end = chunk_size

# List to store summaries
summaries = []

while start < len(Content):
    # Extract chunk from the content
    chunk = Content[start:end]

    # Ensure the chunk is within the length of the content
    if end > len(Content):
        chunk = Content[start:]

    # Summarize the chunk
    summary = summarizer(chunk, max_length=500, min_length=30, do_sample=False)
    summaries.append(summary[0]['summary_text'])

    # Update chunk indices
    start += chunk_size - overlap
    end = start + chunk_size

# Combine all summaries into a final summary
final_summary = " ".join(summaries)
print(final_summary)

final_summary

print(f"Word count is {len(final_summary)}")

"""Deployment"""

