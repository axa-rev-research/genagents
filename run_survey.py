import os
import pandas as pd
from genagents.genagents import GenerativeAgent
import json
import sys
# import mlflow
from datetime import datetime
from simulation_engine.settings import *

def ask_agents(path, questions):
    # End any existing run
    # if mlflow.active_run():
    #     mlflow.end_run()

    # Generate a unique experiment name using the current date and time
    # experiment_name = f"survey_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # experiment_id = mlflow.set_experiment(experiment_name).experiment_id
    
    # Start an mlflow run
    # with mlflow.start_run(experiment_id=experiment_id):
    # List subfolders in the given path
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]

    # Check if 'answers.csv' exists and load it into the DataFrame if it does
    output_path = os.path.join(path, 'answers.csv')
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
    else:
        df = pd.DataFrame(columns=['agent_id', 'answer'])

    # Iterate over each subfolder and create a GenerativeAgent object
    for subfolder in subfolders:
        agent_id = os.path.basename(subfolder)
        
        # Check if the agent_id is already in the DataFrame
        if agent_id in df['agent_id'].values:
            print(f"Skipping agent {agent_id} as it is already in the dataframe.")
            continue
        
        print(f"Processing agent {agent_id} in subfolder {subfolder}")
        agent = GenerativeAgent(subfolder)

        # Ask the agent the categorical question
        answer = agent.categorical_resp(questions)
        print(f"Answer from agent {agent_id}: {answer}")
        scratch = agent.get_self_description()
        print(f"Self description from agent {agent_id}: {scratch}")
        # Clean up the scratch string
        scratch = scratch.strip('{}').replace('"', '')

        # Create a new row with the agent_id and answer
        new_row = {'agent_id': agent_id, 'answer': answer, 'choice': answer[0]["responses"], 'logprobs':answer[2]}

        # Parse the scratch string and add additional columns
        scratch_dict = {}
        for item in scratch.split(", "):
            if ": " in item:
                key, value = item.split(": ", 1)
                scratch_dict[key] = value
        for key, value in scratch_dict.items():
            print(f"{key}: {value}")
            new_row[key.replace('\'', '')] = value
        # Convert the new_row dictionary to a DataFrame and concatenate it with df
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
    
    # Save the DataFrame to a CSV file named 'answers.csv' in the same path
    df.to_csv(output_path, index=False)
    # mlflow.log_artifact(output_path)
    
    # Save the path and questions to a JSON file named 'survey_metadata.json' in the same path
    metadata = {
        'path': path,
        'questions': questions,
        'model_params': MODEL_PARAMS,
        'LLM_VERS':LLM_VERS,
        'AZURE_MODEL_API_VERSION':AZURE_MODEL_API_VERSION
    }
    metadata_path = os.path.join(path, 'survey_metadata.json')
    with open(metadata_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    # mlflow.log_artifact(metadata_path)
    
    # Log the content of all subfolders
    # for subfolder in subfolders:
    #     for root, _, files in os.walk(subfolder):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             mlflow.log_artifact(file_path, artifact_path=os.path.relpath(root, path))
    
    return df

if __name__ == "__main__":
    # End any existing run
    # if mlflow.active_run():
    #     mlflow.end_run()

    if len(sys.argv) < 2:
        print("Usage: python run_survey.py <path_to_input_json>")
        sys.exit(1)
    
    input_path = sys.argv[1]

    # Load input data from the JSON file
    with open(input_path, 'r') as f:
        input_data = json.load(f)
    
    path = input_data['population_path']
    questions = input_data['questions']
    
    # Log the input JSON file
    # mlflow.log_artifact(input_path)
    
    # Generate a unique experiment name using the current date and time
    # experiment_name = f"survey_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # experiment_id = mlflow.set_experiment(experiment_name).experiment_id
    
    # Example usage
    # input_data = {
    #     "population_path": "/Users/rubengarzon/source/stanford/genagents/agent_bank/a_few_agents",
    #     "questions": {
    #         "Do you enjoy outdoor activities?": ["Yes", "No", "Sometimes"]
    #     }
    # }
    
    df = ask_agents(path, questions)

