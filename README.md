# Lab 6 - Chat with PDF
This is a research bot specialized in helping with analyzing research articles in HCI (human-computer-interaction) textile research (e.g. e-textiles, functional textiles, etc.). 

## Getting Started
Open the terminal and run the following commands:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## What's Included
- `app.py`: the main streamlit application. __Featuring__: 
    - Reading the PDF of the paper via URL, no need to download the PDF file locally. (examples include: https://dl.acm.org/doi/pdf/10.1145/3084863.3084868, https://dl.acm.org/doi/pdf/10.1145/3313831.3376841, https://dl.acm.org/doi/pdf/10.1145/2641248.2666717, etc.)
    - FAQs, including "paper overview", "conclude keywords/key methods", "brainstorm research ideas", and "advantages of this research".
    - Ask any other questions on the given PDF.

## Lessons learned
- Basics on LLM (applications and limitations).
    - Learned about many other LLM tools and platforms.
    - Learned about LlamaIndex (a data framework for LLM-based applications which benefit from context augmentation).
    - Concepts on Retrieval-Augmented Generation (RAG), which is used to obtain more accurate text generation relevant to users' specific data (e.g. pdfs, SQL databases, etc.). 
- Streamlit Session State (help variables survive when an interaction happens. e.g. when user push a button, streamlit will re-run the entire Python code, erasing variables. Putting variables in the Session State will help to keep variables between refreshes).
- How to use ChatGPT API in Python and embed AI chat functions in a Streamlit App.
    - How to upload the content pdf files to the context of LLM.

## Questions / Uncertainties
- For the FAQs section in my app, I tried various prompts to let the gpt organize its response in the form of a list `(e.g. 1. fabrication methods: xxx;\n material used: xxx;\n etc.)` but failed.