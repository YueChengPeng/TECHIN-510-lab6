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
- `app.py`: the main streamlit application. Visit at https://techin510lab6leo.azurewebsites.net/. __Featuring__: 
    - Reading the PDF of the paper via URL, no need to download the PDF file locally. (examples include: https://dl.acm.org/doi/pdf/10.1145/3532106.3533551, https://dl.acm.org/doi/pdf/10.1145/3491101.3503579, https://dl.acm.org/doi/pdf/10.1145/3430524.3440642, https://dl.acm.org/doi/pdf/10.1145/3586183.3606724, etc.)
  
  > 🛑 Notice
  > 
  > Via the azure link, not all papers can be accessed because the request is sent from Azure server's IP address, which might not have access to this paper (e.g. https://dl.acm.org/doi/abs/10.1145/3084863.3084868).
  > 
  > One solution is to visit only Open Access papers only (refer to the example links above).
  > Alternative is to clone this repository and run locally. Make sure that your computer is connected via RVPN of your university or directly to the university's WiFi to get access.
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
