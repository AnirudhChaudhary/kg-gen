import os
import json
from openai import OpenAI
import subprocess
import re
import logging
logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, name="", sys_instruction="", llm_prompt="", model_name="gpt-4o"):
        self.name = name
        self.sys_instruction = sys_instruction
        self.prompt = llm_prompt  
        self.model_name = model_name
        self.model = OpenAI()

    def call(self, message, system_instruction="", llm_prompt="", tool_choice=False, tools={}):
        """
        Makes the actual call to gpt with the problem prompt and later, if we want tool_choice and tools.
        Input:
        - message : (str) - A message that you want to gpt to act on 
        - prompt : (str) - System defined prompt for gpt. This will be used as context for gpt.
        - instruction : (str) - This is the "prompt" in a traditional setting, it gives local context to your question / statement
        - tool_choice : (bool) - Determines whether or not you want gpt to consider function calls
        - tools : (Dict) - also known as `helper functions` that the LLM can use to answer the prompt

        Output:
        - ChatCompletion() [ Essentially a dictionary ]
        """
        assert type(message) == str, f"message should be a string, it is of type {type(message)}"
        if system_instruction == "":
            system_instruction = self.sys_instruction

        logger.info("-------- CALLING GPT ----------")
        logger.info("[SYSTEM]: ", system_instruction)
        logger.info("[USER]: ", llm_prompt + message)

        message_to_send =[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": llm_prompt + message}
        ]
        response = self.model.chat.completions.create(
            model=self.model_name,
            messages=message_to_send
        )

        # print("response looks like this now: ", response)

        self.log_meta_data_info(response)
        return response

    def log_meta_data_info(self, ChatCompletionResponse):
        """
        Keeps metadata information about the runs that are happening.
        """
        # Define the metadata folder path
        meta_folder = "metadata"

        # Create the metadata folder if it doesn't exist
        if not os.path.exists(meta_folder):
            os.makedirs(meta_folder)

        # Define the metadata file path
        meta_file = os.path.join(meta_folder, "meta.json")

        # Read the metadata file if it exists
        if os.path.exists(meta_file):
            with open(meta_file, "r") as f:
                meta_data = json.load(f)
        else:
            # otherwise just instantiate the info, and this will be added to later on
            meta_data = {}

        # Get the current agent's name
        agent_name = self.name

        # Get the completion tokens, prompt tokens, and total tokens from the ChatCompletionResponse
        completion_tokens = ChatCompletionResponse.usage.completion_tokens
        prompt_tokens = ChatCompletionResponse.usage.prompt_tokens
        total_tokens = ChatCompletionResponse.usage.total_tokens

        # Update the metadata for the current agent

        # instantiate if it is not in teh the meta information yet
        if agent_name not in meta_data:
            meta_data[agent_name] = {}
            meta_data[agent_name]["completion_tokens"] = 0
            meta_data[agent_name]["prompt_tokens"] = 0
            meta_data[agent_name]["total_tokens"] = 0
            meta_data[agent_name]["invocations"] = 0        # this is the number of times we have called this agent

        meta_data[agent_name]["completion_tokens"] += completion_tokens
        meta_data[agent_name]["prompt_tokens"] += prompt_tokens
        meta_data[agent_name]["total_tokens"] += total_tokens
        meta_data[agent_name]["invocations"] += 1

        # Write the updated metadata back to the file
        with open(meta_file, "w") as f:
            json.dump(meta_data, f)
        
        return

    def parse_output(response, content=True, function_call=False):
        """
        Parses the output
        """

        try:
            content = response["choices"][0]["message"]["content"]
        except:
            response = str(response)
            # print("response: ", response)
            content_start = response.index('content=')                   # get the start of the content
            response_first_half_stripped = response[content_start+9:]       # remove everything up until 'content'
            ending_quote_index = response_first_half_stripped.index("refusal=")  # this is the ending quote, but need to be careful that the index is relative to the content
            content = response_first_half_stripped[:ending_quote_index-2]    # 9 is the len(content=') and ending quote index comes from the previous part, with the new relative section

        return content