# genagents: Extensions

## Utils to run surveys

### Select population
Used to select among all the existing agents a sub-population to run a survey. Edit the file `select_population.py` and edit the variable name and the values (Ex. Age, [55,56,57,58,59])

```bash
python select_population.py
```

(It will create a folder including only the agents according to the variable values.)

### Run survey
Once the population of the survey has been selected, it will run a survey asking the specified questions to all the agents and store the answers in a file `answers.csv`.

The input needs to be a file with the following format:
```json
{
    "population_path": "/Users/rgarzon/Documents/Stanford/genagents/populations/repeat_20_times",
    "questions" : {
      "How much longer do you expect to live relative to others in your age?" 
  : ["I expect to live longer.", "I expect to live about the same time.", "I expect to die sooner."]
  }
}
```

```bash
python run_survey.py <path_to_input_json>

