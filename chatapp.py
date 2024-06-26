import streamlit as st
import requests
import json

# Initialize chat history and session ID
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "id" not in st.session_state:
    st.session_state["id"] = ''
if "mode" not in st.session_state:
    st.session_state["mode"] = 'group'  # Default mode

# Function to get a session ID from the server (create once per user)
def get_session_id():
    url = "http://127.0.0.1:8000/new_session"
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response to get the session ID
        data = json.loads(response.content.decode('utf-8'))
        session_id = data.get('session_id')
        return session_id
    else:
        # Print an error message if the request fails
        print(f"Error: {response.status_code}")
        return None

# Function to send a prompt and get the response using the session ID
def get_response(prompt, session_id, mode):
    url = "http://127.0.0.1:8000/user"
    data = {
    "input": {
        "text": prompt
    },
    "session_id": {
        "id": session_id
    },
    "mode":{
        "mode": mode
    }
}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response = response.json()
        print(response)
        if isinstance(response, list):
            for res in response:
                st.session_state.messages.append(res)
                message = res
                st.markdown(f"<span style='color: black; background-color: lightgray; padding: 5px; border-radius: 5px;'>**{message['from']}:** {message['content']}</span>", unsafe_allow_html=True)
        else:
            st.session_state.messages.append(response)
            message = response
            st.markdown(f"<span style='color: black; background-color: lightgray; padding: 5px; border-radius: 5px;'>**{message['from']}:** {message['content']}</span>", unsafe_allow_html=True)
    else:
        return {"error": f"Error: {response.status_code}"}
    
    

# Generate session ID when the app starts
if st.session_state["id"] == '':
    st.session_state["id"] = get_session_id()

st.title("Procurement Chatapp")
st.sidebar.title("Chat Configuration")

# Display session ID
st.sidebar.write(f"Your session ID is {st.session_state['id']}")

# Mode selection
st.sidebar.radio("Select Mode", ["group", "user"], key="mode")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(f"<span style='color: white; background-color: blue; padding: 5px; border-radius: 5px;'>**User:** {message['content']}</span>", unsafe_allow_html=True)
    else:
        with st.chat_message(message["role"]):
            st.markdown(f"<span style='color: black; background-color: lightgray; padding: 5px; border-radius: 5px;'>**{message['from']}:** {message['content']}</span>", unsafe_allow_html=True)


# Accept user input
if prompt := st.chat_input("Send a message"):
    with st.chat_message("user"):
        st.markdown(f"<span style='color: white; background-color: blue; padding: 5px; border-radius: 5px;'>**User:** {prompt}</span>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        get_response(prompt, st.session_state.id, st.session_state["mode"])


# if prompt:
#     st.session_state["messages"].append({"role": "user", "content": prompt})
#     response = get_response(prompt, st.session_state["id"], st.session_state["mode"])
#     print(response)
#     if st.session_state["mode"] == "user":
#         st.session_state["messages"].append(response[0])
#     else:
#         for msg in response:
#             st.session_state["messages"].append({"role": "assistant", "from": msg["from"], "content": msg["content"]})

#     st.experimental_rerun()  # Rerun the app to display the new messages


# # Display chat messages from history on app rerun
# for message in st.session_state["messages"]:
#     if message["role"] == "user":
#         st.markdown(f"<span style='color: white; background-color: blue; padding: 5px; border-radius: 5px;'>**User:** {message['content']}</span>", unsafe_allow_html=True)
#     else:
#         st.markdown(f"<span style='color: black; background-color: lightgray; padding: 5px; border-radius: 5px;'>**{message['from']}:** {message['content']}</span>", unsafe_allow_html=True)
