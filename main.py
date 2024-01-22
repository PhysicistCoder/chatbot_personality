import streamlit as st
from openai import OpenAI

# input template for Chatbot's personality and task
st.title("AI Chatbot - Instruct your own Custom Chatbot to do anything!")
st.image("https://res.cloudinary.com/preface/image/upload/w_1024,c_limit,f_auto/v1633826301/r2021/assets/images/preface_logo.png",use_column_width=True)

# input template for Chatbot's personality and task
input_template = st.text_area(label="Chatbot Instructions",value=
    """ You are a Chatbot for an EdTech company called Preface. The company is based in Hong Kong and teaches coding to students.
    The following courses are currently available:
    - Python
    - Data Science
    - Machine Learning
    - Web Development
    - App Development
    - Generative AI       
    Your goal is to respond to user queries about the courses and the company. 
    You can redirect users to the website or to the Preface team if you are unable to answer the question (preface.ai).
    Also feel free to ask the user questions to get more information about their query to recommend the best course for them.

    """)


# create text input for api key
api_key = st.text_input("Enter your OpenAI API key")


# create button to save input template
save_input_template = st.button("Save Chatbot Instructions")
if save_input_template:
    st.session_state["input_template"] = input_template

if st.session_state.get("input_template"):
    st.write("Chatbot Instructions Saved ✔️")

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Function for generating LLM response
    def generate_response(prompt_input):
        # append the template to the prompt
        template_with_prompt_input = input_template + "\n The users query is = " + prompt_input

        client = OpenAI(
            # This is the default and can be omitted
            api_key=api_key,
        )
        response = client.chat.completions.create(
            messages=[{
                    "role": "user",
                    "content": template_with_prompt_input,
                    }],
            model="gpt-3.5-turbo",
        )

        return response.choices[0].message.content



    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt) 
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)