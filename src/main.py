# Import the Pipeline and Agent classes
# from agent import Pipeline, Agent

# Set up the Azure OpenAI service
import os
import json
from openai import OpenAI
import subprocess
import re
import logging
logger = logging.getLogger(__name__)
from agent import Agent

def main():
    count = 1
    output_path = f'logging/log_{count}.txt'
    while os.path.exists(output_path):
        count += 1
        output_path = f'logging/log_{count}.txt'

    f = open(output_path, "w+")
    f.close()
    logging.basicConfig(filename=output_path, level=logging.INFO)
    print("Logging to: ", output_path)

    ##### DEFINE AGENTS #####
    text_analyzer_agent = Agent(name="Text Analyzer", model_name="gpt-4o")


    ##### PULL INPUT TEXT #####
    input_directory = "textbooks/LeeSeshia"
    input_file = "ch13.txt"
    output_file = "outputs/" + input_file.strip(".txt") + ".json"

    full_path = input_directory + "/" + input_file

    with open(full_path, "r") as f:
        input_text = f.read()


    # system_instruction = "You will be given text from a chapter on EmbeddedSystems. I need you to generate a list of topics and subtopics that are related to the text. The output should be in a json format with the following fields: topic: <string>, descr: <string>, related_topics: List[<string>]. "
    # prompt = "Text: " + input_text

    # response = text_analyzer_agent.call(message=prompt, system_instruction=system_instruction)
    # response = Agent.parse_output(response)
    response = """```json\n[\n    {\n        "topic": "System Requirements and Specifications",\n        "descr": "Embedded systems must be designed to meet specific requirements, often detailed in specifications which help prevent ambiguity during design.",\n        "related_topics": ["Formal Specifications", "System Properties", "SpaceWire Protocol"]\n    },\n    {\n        "topic": "Formal Specifications",\n        "descr": "A mathematical method for specifying system properties precisely, avoiding ambiguities in natural language descriptions.",\n        "related_topics": ["Temporal Logic", "System Requirements and Specifications", "Mathematical Notations"]\n    },\n    {\n        "topic": "Temporal Logic",\n        "descr": "A mathematical notation used for representing and reasoning about timing-related properties in system specifications.",\n        "related_topics": ["Formal Specifications", "Linear Temporal Logic", "System Properties"]\n    },\n    {\n        "topic": "Invariants",\n        "descr": "Properties that hold true for a system at every point during its operation, a fundamental concept in temporal logic.",\n        "related_topics": ["Temporal Logic", "System Properties", "SpaceWire Protocol"]\n    },\n    {\n        "topic": "Linear Temporal Logic (LTL)",\n        "descr": "A type of temporal logic used to specify system behavior across single executions, capable of expressing occurrence, dependency, and order properties.",\n        "related_topics": ["Temporal Logic", "Propositional Logic Formulas", "Temporal Operators"]\n    },\n    {\n        "topic": "Propositional Logic Formulas",\n        "descr": "Combining atomic propositions using logical connectives to express conditions in a system\'s reactions.",\n        "related_topics": ["Linear Temporal Logic (LTL)", "Temporal Logic", "Logical Connectives"]\n    },\n    {\n        "topic": "LTL Temporal Operators",\n        "descr": "Operators such as G (Globally), F (Eventually), X (Next), and U (Until) used within LTL to reason about system traces.",\n        "related_topics": ["Linear Temporal Logic (LTL)", "Temporal Logic", "Propositional Logic Formulas"]\n    },\n    {\n        "topic": "Safety and Liveness Properties",\n        "descr": "Key types of properties expressible with temporal logic focusing on a system\'s dependability and continuous operation.",\n        "related_topics": ["Temporal Logic", "Linear Temporal Logic (LTL)", "Formal Specifications"]\n    }\n]\n```'"""
    response_split_by_line = response.split("\n")
    response = json.dumps(response_split_by_line, indent=2)
    print(response)

    with open(output_file, "w") as f:
        for line in response_split_by_line:
            f.write(line + "\n")



if __name__ == '__main__':
    main()