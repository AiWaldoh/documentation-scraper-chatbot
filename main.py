from typing import Set

from retrieval import run_llm
import streamlit as st
from streamlit_chat import message

st.sidebar.title("Configuration")

def model_callback():
    st.session_state["model"] = st.session_state["model_selected"]

def node_callback():
    print(st.session_state.node)
    st.session_state["node"] = st.session_state["node_selected"]

if "model" not in st.session_state:
    st.session_state["model"] = "gpt-3.5-turbo-16k"

if "node" not in st.session_state:
    st.session_state["node"] = "cosmos"

# not implemented yet
st.session_state.model = st.sidebar.radio(
    "Select OpenAI Model",
    ("gpt-3.5-turbo-16k", "gpt-4"),
    index=0 if st.session_state["model"] == "gpt-3.5-turbo-16k" else 1,
    on_change=model_callback,
    key="model_selected",
)

st.session_state.node = st.sidebar.radio(
    "Select Documentation",
    ("streamlit-26", "langchain-1", "cosmos-047", "osmosis-18", "kubernetes-128", "elys-1", "nextjs-13"),
    on_change=node_callback,
    key="node_selected",
)

st.header("AiWaldoh's AI Documentation Whisperer!🤖")

prompt = st.chat_input("Enter your prompt here..")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"], node=st.session_state.node
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)
