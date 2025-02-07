import streamlit as st
import pandas as pd
import time
import random
import json
# Fix issue with the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # Add current folder to the python path
from genagents.genagents import GenerativeAgent
from simulation_engine.settings import LLM_VERS  # Import LLM_VERS
from simulation_engine.settings import STREAMLIT_USERNAME, STREAMLIT_PASSWORD  # Import USERNAME and PASSWORD

def load_placeholder(file_path):
    with open(file_path) as json_file:
        scratch = json.load(json_file)
    return scratch 

def generate_excel(type_of_question, query, demographics, response):
    # Simulate processing time
    time.sleep(random.uniform(2, 5))
    
    # Create DataFrame
    data = {
        'Type_of_Question': type_of_question,
        'Query': query,
        'Demographics': demographics,
        'Response': response
    }
        
    df = pd.DataFrame([data])
    
    # Generate Excel file
    filename = f"generated_data_{int(time.time())}.xlsx"
    df.to_excel(filename, index=False)
    return filename

def main():
    st.title("Run study with genagents")
    
    # Authentication
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if username != STREAMLIT_USERNAME or password != STREAMLIT_PASSWORD:
        st.error("Invalid username or password")
        return

    # Load placeholder information from JSON file
    current_path = os.path.dirname(os.path.abspath(__file__))
    placeholder_file_path = os.path.join(current_path, 'agent_bank/populations/gss_agents/0a1aa8c2-382a-4cd3-9d02-3a34e0592bbd/scratch.json')
    scratch_data = load_placeholder(placeholder_file_path)

    # Field 1: Select
    type_of_question_options = ['Categorical question', 'Numerical question']
    type_of_question = st.selectbox("Select type of question", type_of_question_options)
    
    # New Field: Model Selection
    model_options = ['gpt-4o-mini','gpt-4o']
    selected_model = st.selectbox("Select model", model_options)

    # Update LLM_VERS based on selected model
    LLM_VERS = selected_model

    # Field 3: Text Entry with dynamic placeholder
    if type_of_question == "Categorical question":
        placeholder = "{'Do you enjoy outdoor activities?': ['Yes', 'No', 'Sometimes']}"
    else:
        placeholder = "{'On a scale of 1 to 10, how much do you enjoy coding?': [1, 10]}"
    
    # Field 2: Text Entry
    query = st.text_input("Enter the question", value=placeholder)
    
    # Demographics: Large Text Area
    demographics = st.text_area("Enter demographics information", height=300, value=scratch_data)
    
    # Output field
    output_placeholder = st.empty()

    # Submit Button
    if st.button("Generate request"):
        # Progress window
        #progress_bar = st.progress(0)
        status_text = st.empty()
        
        #for percent_complete in range(0, 101, 20):
        #    time.sleep(0.5)
        #    progress_bar.progress(percent_complete)
         #   status_text.text(f"Processing: {percent_complete}% complete")
        status_text.text("Calling LLMs ...")
        agent = GenerativeAgent()  
        try:
            demographics_formatted = eval(demographics)
        except:
            print ("ERROR in json")
            output_placeholder.text("ERROR in formatting the demographics")
            demographics.value = scratch_data        
        
        agent.update_scratch(demographics_formatted)       

        if type_of_question == "Categorical question":
            response = agent.categorical_resp(eval(query))
        else:
            response = agent.numerical_resp(eval(query))
        status_text.text("Generating excel ...")
        # Generate and provide download
        filename = generate_excel(type_of_question,query, demographics, response)
        
        with open(filename, "rb") as file:
            st.download_button(
                label="Download Excel File",
                data=file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        status_text.text("File generation complete!")

        output_placeholder.text(response)
        # Optional restart
        if st.button("Start Over"):
            st.experimental_rerun()

if __name__ == "__main__":
    main()