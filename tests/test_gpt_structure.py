import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from simulation_engine.gpt_structure import gpt_request
from simulation_engine.gpt_structure import generate_prompt

from simulation_engine.settings import *

def create_prompt_input(agent_desc, questions):
    str_questions = ""
    for key, val in questions.items(): 
        str_questions += f"Q: {key}\n"
        str_questions += f"Option: {val}\n\n"
        str_questions = str_questions.strip()
    return [agent_desc, str_questions]

class TestGptRequest(unittest.TestCase):
    def test_gpt_request_success(self):
        # Mock a successful response
#        mock_post.return_value.status_code = 200
#        mock_post.return_value.json.return_value = {'responses': ["Yes", "No", "Sometimes"]}
        agent_desc = "Name is John Doe, 30 year old, very sportive person."
        agent_desc += f"Other observations about the subject:\n\n"
        questions = {
            "Do you enjoy outdoor activities?": ["Yes", "No", "Sometimes"]
        }
        prompt_lib_file = f"{LLM_PROMPT_DIR}/generative_agent/interaction/categorical_resp/singular_v1.txt" 
        prompt_input = create_prompt_input(agent_desc, questions)
        prompt = generate_prompt(prompt_input, prompt_lib_file)
        print (prompt)
        gpt_version = "gpt-4o-mini"
        response = gpt_request(prompt, gpt_version)
        print (response)
        print (response["Response"])
        self.assertIn("Yes", response["Response"]) or self.assertIn("No", response["Response"]) or self.assertIn("Sometimes", response["Response"])

if __name__ == '__main__':
    unittest.main()
