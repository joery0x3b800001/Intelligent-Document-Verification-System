from flask import Flask, request, render_template, redirect, url_for
import fitz  # PyMuPDF
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import difflib
import os
from transformers import pipeline
import nltk
import torch

nltk.download('punkt')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the summarization model
summarizer = pipeline('summarization', model="sshleifer/distilbart-cnn-12-6")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def google_search(query, num_results=5):
    return [url for url in search(query, num_results=num_results)]

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join([p.text for p in soup.find_all('p')])

def find_discrepancies(summary_text, web_text):
    d = difflib.SequenceMatcher(None, summary_text, web_text)
    differences = d.get_opcodes()
    return differences

def split_text_with_context(text, max_length=512, overlap=50):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(nltk.word_tokenize(sentence))
        if current_length + sentence_length > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = current_chunk[-overlap:]  # Retain overlap sentences
            current_length = sum(len(nltk.word_tokenize(sent)) for sent in current_chunk)
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def summarize_text(text):
    chunks = split_text_with_context(text)
    summaries = []
    
    for chunk in chunks:
        if len(chunk) > 0:  # Ensure the chunk is not empty
            summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
            summaries.append(summary)
    
    return ' '.join(summaries)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('show_results', filename=file.filename))
    return render_template('index.html')

@app.route('/results/<filename>')
def show_results(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_text = extract_text_from_pdf(file_path)
    
    # Summarize the extracted text
    summary = summarize_text(pdf_text)
    
    # Fact-check the summary
    urls = google_search(summary)
    discrepancies = []
    colors = ['#FFCCCC', '#CCFFCC', '#CCCCFF', '#FFFF99', '#FF99CC']  # Different colors for each source
    color_index = 0

    for url in urls:
        web_text = get_text_from_url(url)
        diffs = find_discrepancies(summary, web_text)
        for tag, i1, i2, j1, j2 in diffs:
            if tag == 'replace' or tag == 'delete' or tag == 'insert':
                discrepancies.append({
                    'source': url,
                    'summary_text': summary[i1:i2],
                    'web_text': web_text[j1:j2],
                    'color': colors[color_index % len(colors)]
                })
        color_index += 1

    return render_template('result.html', summary=summary, discrepancies=discrepancies)

if __name__ == '__main__':
    app.run(debug=True)
