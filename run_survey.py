import os
import pandas as pd
from genagents.genagents import GenerativeAgent
import json

def ask_agents(path, questions):
    # List subfolders in the given path
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]

    # Initialize an empty DataFrame to store the answers
    df = pd.DataFrame(columns=['agent_id', 'answer'])

    # Iterate over each subfolder and create a GenerativeAgent object
    for subfolder in subfolders:
        print (subfolder)
        agent_id = os.path.basename(subfolder)
        agent = GenerativeAgent(subfolder)

        # Ask the agent the categorical question
        answer = agent.categorical_resp(questions)
        print (answer)
        scratch = agent.get_self_description()
        print (scratch)
        # Clean up the scratch string
        scratch = scratch.strip('{}').replace('"', '')

        # Create a new row with the agent_id and answer
        new_row = {'agent_id': agent_id, 'answer': answer , 'choice': answer["responses"]}

        # Parse the scratch string and add additional columns
        scratch_dict = {}
        for item in scratch.split(", "):
            if ": " in item:
                key, value = item.split(": ", 1)
                scratch_dict[key] = value
        for key, value in scratch_dict.items():
            print(key, value)
            new_row[key.replace('\'','')] = value
        # Convert the new_row dictionary to a DataFrame and concatenate it with df
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
    # Save the DataFrame to a CSV file named 'answers.csv' in the same path
    output_path = os.path.join(path, 'answers.csv')
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    # Example usage
    path = '/Users/rubengarzon/source/stanford/genagents/agent_bank/a_few_agents'
    # Interact with the agent
    questions = {
    "Do you enjoy outdoor activities?": ["Yes", "No", "Sometimes"]
    }
    
    df = ask_agents(path, questions)
    print(df)
    # Save to a file .csv
    df.to_csv('answers.csv', index=False)
