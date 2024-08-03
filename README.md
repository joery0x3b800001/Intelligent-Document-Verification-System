# Intelligent Document Verification System

## Overview

The Intelligent Document Verification System is a web application that allows users to upload PDF documents, automatically summarizes their content, and then verifies the summary against information available on the web. The application uses state-of-the-art NLP models for summarization and various web scraping techniques to ensure the accuracy of the summaries.

## Features

- **PDF Upload**: Upload PDF documents for processing.
- **Text Extraction**: Extract text from PDF documents.
- **Summarization**: Generate a concise summary of the extracted text.
- **Fact-Checking**: Verify the accuracy of the summary by comparing it with content from relevant web sources.
- **Discrepancy Highlighting**: Identify and highlight discrepancies between the summary and web content.

## Technologies Used

- **Flask**: Web framework for building the web application.
- **PyMuPDF (fitz)**: Library for extracting text from PDF documents.
- **Transformers**: Hugging Face library for NLP tasks, used for summarization.
- **NLTK**: Library for natural language processing, used for sentence tokenization.
- **BeautifulSoup**: Library for web scraping and parsing HTML.
- **Google Search API**: For retrieving relevant web pages.
- **Difflib**: For comparing text and identifying differences.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/joery0x3b800001/Intelligent-Document-Verification-System.git
   cd intelligent-document-verification-system
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data:**
   ```python
   import nltk
   nltk.download('punkt')
   ```

5. **Flask Application Structure:**

   ```bash
      /docVerify
         /templates
            index.html
            result.html
      /static
      app.py
   ```

   - **`/docVerify/`**: The root directory of the Flask application.
   - **`/templates/`**: Contains HTML templates for the application.
      - **`index.html`**: Template for the file upload page.
      - **`result.html`**: Template for displaying results.
   - **`/static/`**: Directory for static files (e.g., CSS, JavaScript).
   - **`app.py`**: The main Flask application file.

6. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will start and be accessible at `http://127.0.0.1:5000`.

## Usage

1. **Upload a PDF Document:**
   - Go to the home page (`/`).
   - Use the file upload form to select and upload a PDF document.

2. **View Results:**
   - After uploading, you will be redirected to the results page (`/results/<filename>`).
   - The page will display the summarized text and discrepancies found by comparing the summary with web content.

## Example

Upload a PDF and the application will:
1. Extract text from the PDF.
2. Summarize the extracted text.
3. Search for web content related to the summary.
4. Highlight discrepancies between the summary and web content.

## Contributing

Contributions are welcome! Please submit issues and pull requests on the [GitHub repository](https://github.com/joery0x3b800001/Intelligent-Document-Verification-System.git).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.md) file for details.

## Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [NLTK](https://www.nltk.org/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Google Search API](https://pypi.org/project/googlesearch-python/)

---