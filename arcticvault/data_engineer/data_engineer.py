from typing import Dict, Union
from arcticvault.data_engineer.prompts import (
    SYSTEM_PROMPT_SQL_GENERATION_HUBS, 
    SYSTEM_PROMPT_SQL_GENERATION_LINKS, 
    SYSTEM_PROMPT_SQL_GENERATION_SATELLITES
)


class DataEngineerAssistant:
    """Data Engineer object to perform all action needed in Data Analyst page"""

    def __init__(self, table_type: str, input_report: str) -> None:
        self.model_kwargs = {    
            "top_p": 0.99,
            "temperature": 0.0,
            "max_new_tokens": 1024,
            "stop_sequences": "###, <|im_sep|>, Note",
           
        }
        self.input_report = input_report
        if table_type == "hubs":
            self.prompt = SYSTEM_PROMPT_SQL_GENERATION_HUBS
            self.start_message = "Hubs Tables:"
            self.min_new_tokens = 64
        elif table_type == "links":
            self.prompt = SYSTEM_PROMPT_SQL_GENERATION_LINKS
            self.start_message = "Links Tables:"
            self.min_new_tokens = 64
        elif table_type == "satellites":
            self.prompt = SYSTEM_PROMPT_SQL_GENERATION_SATELLITES
            self.start_message = "Satellites Tables:"
            self.min_new_tokens = 512

    def get_model_input_sql_generation(
        self,
    ) -> Dict[str, Union[str, int]]:
        """
        Creates a conversational chain to chat with the user about the tables enter to create a data vault 2.0

        :return: The conversational chain
        """

        prompt = self._define_prompt_sql_generation(
            prompt=self.prompt, start_message=self.start_message
        )
        
        model_inputs = self.model_kwargs
        model_inputs.update({
            "min_new_tokens": self.min_new_tokens,
            "prompt_template": prompt,
            "prompt": self.input_report

        })
        
        return model_inputs

    @staticmethod
    def _define_prompt_sql_generation(prompt: str, start_message: str) -> str:
        """
        Define the prompt for a chat conversation.

        :return: A ChatPromptTemplate instance representing the prompt.
        :rtype: ChatPromptTemplate
        """

        prompt = "<|im_start|>user\n" +\
            prompt +\
            "\n" +\
            "{prompt}" +\
            "<|im_end|>\n\n" +\
            "<|im_start|>assistant\n: Here are the SQL queries to create" +\
            f" the {start_message} tables based on the Data Vault 2.0 model you provided:\n"

        return prompt



