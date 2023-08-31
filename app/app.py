import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tiktoken
import tempfile
import openai
from instruction import instructions
from eda import visualize
import pandas as pd
from classification import automl
st.set_page_config(
   page_title="Data-Talker",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

def main():
    try:
        title = st.empty()
        title.title("Hello 👋, Lets Talk about your Data")
        wip = st.empty()
        wip.text("Feel free to ask any question on your Data, \nWait! first Upload it from the sidebar")
        
        st.sidebar.title("🧊 Data-Talker")
        st.sidebar.markdown("---")
        user_api_key = st.sidebar.text_input(
            label="## Put Your Api Key, Don't worry its safe 😇",
            placeholder="Paste your OpenAI API key...",
            type="password")

        uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

        if uploaded_file:
            # Use tempfile because CSVLoader only accepts a file_path
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ','})
            data = loader.load()

            csv = st.empty()
            csv.write("CSV Data:")
            wait = st.empty()
            wait.write("Wait for some time it may take some time to load the data.....")

            options = st.sidebar.radio("What do you want to do?", ("Talk to your Data", "Visualize Data", "AutoML"))

            if options == "Visualize Data":
                wip.empty()
                title.empty()
                csv.empty()
                wait.empty()
                visualize(uploaded_file)

            if options == "AutoML":
                wip.empty()
                title.empty()
                csv.empty()
                wait.empty()
                if type(uploaded_file) is not str:
                    uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
                st.title("AutoML")
                st.subheader("Glimpse of dataset")
                st.write(df)
                label = None 
                label = st.selectbox("Select the target column",df.columns)
                usecase = None
                with st.header('2. Set Parameters'):
                    usecase = st.selectbox('Select dataset type (Regression/Classification)', ['regression','classification'])
                button = st.button('Train Models')
                if label is not None:
                    if usecase is not None:
                        if button:
                            automl(df, label, usecase)
                    elif button:
                        st.write("Please select the dataset type")
                elif button:
                    st.write("Please select the target column")
            
            if options == "Talk to your Data":
                wip.empty()
                if user_api_key:
                    openai.api_key = user_api_key  # Set the API key
                    embeddings = OpenAIEmbeddings(openai_api_key=user_api_key)
                    vectorstore = FAISS.from_documents(data, embeddings)

                    chain = ConversationalRetrievalChain.from_llm(
                        llm=ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo', openai_api_key=user_api_key),
                        retriever=vectorstore.as_retriever())
                                # Container for the chat history
                response_container = st.container()
                # Container for the user's text input
                container = st.container()

                if 'history' not in st.session_state:
                    st.session_state['history'] = []

                if 'generated' not in st.session_state:
                    st.session_state['generated'] = ["Hello! Ask me anything about " + uploaded_file.name + " 🤗"]

                if 'past' not in st.session_state:
                    st.session_state['past'] = ["Hey! 👋"]

                with container:
                    with st.form(key='my_form', clear_on_submit=True):
                        user_input = st.text_input("Query:", placeholder="Talk about your csv data here (:", key='input')
                        submit_button = st.form_submit_button(label='Send')

                    if submit_button and user_input:
                        output = conversational_chat(user_input, chain)
                        st.session_state['past'].append(user_input)
                        st.session_state['generated'].append(output)

                if st.session_state['generated']:
                    with response_container:
                        for i in range(len(st.session_state['generated'])):
                            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
                else:
                    st.write("No data uploaded yet")

        # Show Instructions
        instructions()

    except openai.error.AuthenticationError:
        st.error("Invalid API key. Please check your OpenAI API key and try again.")
    except openai.error.RateLimitError:
        st.error("API quota exceeded. Please check your API quota or try again later.")
    except Exception as e:
        st.error("An error occurred: {}".format(e))

def conversational_chat(query, chain):
    try:
        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]
    except openai.error.RateLimitError:
        st.error("API quota exceeded. Please check your API quota or try again later.")
    except Exception as e:
        st.error("An error occurred during the conversation: {}".format(e))



if __name__ == "__main__":
    main()