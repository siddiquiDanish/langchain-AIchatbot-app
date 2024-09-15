import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from streamlit_chat import message
from langchain.schema import (HumanMessage, SystemMessage, AIMessage)

load_dotenv(find_dotenv(), override=True)

llm_model = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.5)
st.set_page_config(
    page_title='AI Chatbox',
    page_icon='🤖'
)

st.subheader('Custom AI Chatbox')
if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_message = st.text_input(label='System role :')
    user_prompt = st.text_input(label='Send a message :')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(SystemMessage(content=system_message))
            # st.write(st.session_state.messages)

    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))

        with st.spinner('Generating response...'):
            response = llm_model(st.session_state.messages)

        st.session_state.messages.append(AIMessage(content=response.content))

if len( st.session_state.messages)>=1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant'))

for i, msg in enumerate(st.session_state.messages[1:]): #starting with index 1, no need to show first system message
    if i%2 == 0:
        message(msg.content, is_user=True, key=f'{i} 🧔🏻‍♂️')
    else:
        message(msg.content, is_user=True, key=f'{i}  🤖')



