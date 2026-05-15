from core.llm import create_llm
from core.data_loader import load_metadata
from core.column_selector import select_columns
import streamlit as st
import json
from typing import Dict
from core.analysis import execute_analysis


metadata = load_metadata()
llm = create_llm()

def create_json(json_str: str) -> Dict:
    """ Clear text before and after the JSON string and then load it into a dictionary
    """

    # find the first { and last } using str.find method
    start_index = json_str.find("{")
    end_index = json_str.rfind("}")

    cleaned_json_str=json_str[start_index:end_index+1]

    print(cleaned_json_str) 

    return json.loads(cleaned_json_str)

st.set_page_config(page_title="CKT Analysis Assistant", layout="centered")
st.title("CKT Analysis Assistant")

# storing chat message history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"assistant", "content":"What would you like to do today?"}
    ]
    
# storing the analysis plan (session state) when a follow up question is required
if "pending_analysis" not in st.session_state:
    st.session_state["pending_analysis"] = None

with st.sidebar:
    st.subheader("Session")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.pop("message", None)
        st.rerun()
  
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a question")

if prompt:
        st.session_state["messages"].append({"role":"user", "content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            st.spinner("Retrieving answer")

            if st.session_state["pending_analysis"] is not None:
                clarification_prompt = f"""
                    The user is answering a clarification question for this pending analysis

                    The pending analysis plan:
                    {json.dumps(st.session_state.pending_analysis, indent=2)}

                    Update the pending analysis according to the user's clarification answer

                    User's clarification
                    {prompt}
                    
                    Rules:
                    - Keep the existing values in the pending analysis plan. 
                    - do not create a new analysis plan
                    - return only valid json using the required schema
                """
                results_text = select_columns(llm, clarification_prompt, metadata, st.session_state["messages"])
            
            else:
                results_text = select_columns(llm, prompt, metadata, st.session_state["messages"])
           
            #print(result)
            results = create_json(results_text)
            df = execute_analysis(results)
        
            with st.chat_message("assistant"):
                if results["clarification_required"]:
                    st.markdown(results["clarification_question"])
                    st.session_state["pending_analysis"] = results
                else: 
                    st.markdown(results)
                    st.dataframe(df)
                    # Clear the pending analysis plan
                    st.session_state.pop("pending_analysis", None)

                # if clarification needed
                # save it to pending state
                #sitll display the message to user
            
            st.session_state["messages"].append({"role":"assistant", "content":results})
        
        
        except Exception as e:
            st.error("Generating Response")
            st.exception(e)
      
          


       
        


        