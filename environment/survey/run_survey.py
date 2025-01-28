import os
from survey import Survey

def main():
    # Define the directory to save responses
    save_dir = "/Users/rgarzon/Documents/Stanford/genagents/outputs/responses"
    os.makedirs(save_dir, exist_ok=True)

    # Define the survey questions
    questions = {
        "What do you prefer for holidays?": ["Mountain", "Beach", "City"],
        "What is your favourite animal?": ["Elephant", "Dog", "Snake"]
    }

    # Define inclusion criteria (optional)
    inclusion_criteria = {
        "What do you prefer for holidays?": ["Mountain", "Beach"]
    }

    # Initialize the Survey environment
    survey_env = Survey(saved_dir=save_dir)

    # Load existing responses if any
    survey_env._load_responses(save_dir)

    # Administer the survey
    responses = survey_env.survey(questions, inclusion_criteria)

    # Package and save the responses
    packaged_responses = survey_env._package_responses()
    survey_env._save_responses(save_dir, packaged_responses)

    print("Survey completed and responses saved.")

if __name__ == "__main__":
    main()
