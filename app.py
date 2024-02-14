import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv
import requests
import os
from tempfile import NamedTemporaryFile

load_dotenv()

st.set_page_config(
    page_title="Chat with the PDF",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

if "if_pdf_none" not in st.session_state.keys():
    st.session_state.if_pdf_none = True

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "I'm your HCI textile research assistant. Start with entering the PDF URL in the sidebar. Let's chat!"}
    ]

st.sidebar.header("Start with loading the PDF")
pdf_url = st.sidebar.text_input("Enter the PDF URL", key="pdf_url") # PDF URL input (fixed position)
st.sidebar.header("FAQs")
overview_button = st.sidebar.button("🔭 Paper Overview")
conclude_keywords_button = st.sidebar.button("🔑 Conclude Keywords/Key Methods")
brainstorm_button = st.sidebar.button("🧠 Brainstorm Research Ideas") # Brainstorm button (fixed position)
advantage_button = st.sidebar.button("🌟 Advantages of this Research") # Brainstorm button (fixed position)


if pdf_url:
    response = requests.get(pdf_url)
    if response.status_code == 200:
        bytes_data = response.content
        with NamedTemporaryFile(delete=False) as tmp:  # open a named temporary file
            tmp.write(bytes_data)  # write data from the PDF URL into it
            with st.spinner(
                text="Loading and indexing the PDF – hang tight! This should take 1-2 minutes."
            ):
                reader = PDFReader()
                docs = reader.load_data(tmp.name)
                llm = OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    base_url=os.getenv("OPENAI_API_BASE"),
                    model="gpt-3.5-turbo",
                    temperature=0.0,
                    system_prompt="You are an expert on HCI textile research. Provide detailed answers to the questions using the document. Use the document to support your answers."
                )
                index = VectorStoreIndex.from_documents(docs)
                os.remove(tmp.name)  # remove temp file

                if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
                    st.session_state.chat_engine = index.as_chat_engine(
                        chat_mode="condense_question", verbose=False, llm=llm
                    )
                    print(st.session_state.chat_engine.stream_chat("tell me about this article").response_gen)
                    if st.session_state.if_pdf_none:
                        st.session_state.messages = [
                            {"role": "assistant", "content": "The PDF has been loaded and indexed. You can now ask questions!"}
                        ]
                        st.session_state.if_pdf_none = False

# Chat input and message handling remains the same
if not st.session_state.if_pdf_none:
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Conclude Keywords/Key Methods
    if conclude_keywords_button:
        prompt = """
        Based on the this paper, extract keywords.
        Notice, I will extract a lot of similar papers all about textiles, so I need to extract the most specific keywords possible. For example, I am interested in how they made the smart textiles (embroidered) and what they did with the smart textiles (sensing, actuating, and connecting components, etc.), not something like “textiles” or “smart textile”. The ones he extracted are meaningless because all the articles I collected are about textiles. I want more specific keywords with a specific purpose.
    dimensions include: 
    1. method that they used to fabricate textiles (embroidery, knitting, weaving, etc.) 
    2. fabrication tools/machines used (e.g. embroidery machine, knitting machine, looms, Jacquard machine, punch needle, etc.) 
    3. materials used (conductive thread, carbon ink, PPy, etc.) 
    4. what they did with the textiles (use textiles to do what? sensing? displaying? output, actuating?, applications) 
    5. tools they use/develop (e.g. Visual programming tool, design space, design templates, online tools, parametric design tools (e.g. grasshopper), design tool, simulation tool, etc.) 
    6. if they conduct any workshop or user study (if yes, return "yes") 
    7. special techniques used (e.g. self-powered, TENG, etc.)
    return a ordered list, including phrases for each dimensions (and the name of the dimension). Create a new line for each list number. if the outlines are not applicable, e.g. in the abstract they did not describe how they made the textiles, return NA for that dimension.
    please be concise on your response, for each question, provide phrases separated by commas. For each phrases, use no more than 4 words. Don't repeat the name of the paper (e.g. the name they give for their projects).
    """
        st.session_state.messages.append({"role": "user", "content": "Conclude Keywords/Key Methods"})
    
    if brainstorm_button:
        prompt = """
        based on this paper's main content and its "future work" part (if applicable), brainstorm 5 possible future research ideas on textiles in HCI domain.
        """
        st.session_state.messages.append({"role": "user", "content": "Brainstorm research ideas based on this paper"})

    if overview_button:
        prompt = """
        Provide an overview of this paper.
        """
        st.session_state.messages.append({"role": "user", "content": "Overview of the paper"})
    
    if advantage_button:
        prompt = """
        Based on this paper, provide the advantages of this research.
        """
        st.session_state.messages.append({"role": "user", "content": "Advantages of this research"})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)