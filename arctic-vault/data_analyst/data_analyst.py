from typing import Dict, List, Tuple, Union

from arcticvault.data_analyst.config import (
    SYSTEM_PROMPT_DA,
    SYSTEM_PROMPT_GENERATION_REPORT,
)


class DataAnalystAssistant:
    """Data Analyst object to perform all action needed in Data Analyst page"""

    def __init__(self, history: List[Dict[str, str]]) -> None:
        self.history = history
        self.model_kwargs = {
            "top_p": 0.8,
            "temperature": 0.2,
            "max_new_tokens": 1024,
            "min_new_tokens": 256,
            "stop_sequences": "###, <|im_sep|>, <|im_end|>",
        }

    def get_chat_chain(
        self,
    ) -> Dict[str, Union[str, int]]:
        """
        Creates a conversational chain to chat with the user about the tables enter to create a data vault 2.0

        :return: The conversational chain
        """

        model_input = self.model_kwargs

        prompt = self._define_prompt_chat()

        model_input["prompt_template"] = prompt

        return model_input

    def get_generate_summary_chain(
        self,
    ) -> Dict[str, Union[str, int]]:
        """
        Creates a chain to be used to generate the report out of the conversation

        :return: the input argument to generate an swer with Replicate
        """

        model_input = self.model_kwargs

        conversation = self.__render_history(enable_generation=True)
        prompt = self._define_prompt_generation()

        model_input.update({
            "prompt_template": prompt,
            "prompt": f"Based on this conversation:\n {conversation}\n" +\
            "Generate the most complete report."
        })


        return model_input

    @staticmethod
    def _define_prompt_chat() -> str:
        """
        Define the prompt for a chat conversation.

        :return: the system prompt to be used to chat with the Data Analyst
        :rtype: str
        """
        prompt = (
            "<|im_start|>system\n"
            + SYSTEM_PROMPT_DA
            + "<|im_end|>\n"
            + "<|im_start|>user\n"
            + "{prompt}"
            + "<|im_end|>\n\n"
            + "<|im_start|>assistant\n"
        )

        return prompt

    @staticmethod
    def _define_prompt_generation() -> str:
        """
        Define the prompt for a chat conversation.

        :return: The system prompt to generate the Report of out the conversation with the Data Analyst
        :rtype: str
        """

        prompt = (
            "<|im_start|>system\n"
            + SYSTEM_PROMPT_GENERATION_REPORT
            + "<|im_end|>\n"
            + "<|im_start|>user\n"
            + "{prompt}"
            + "<|im_end|>\n\n"
            + "<|im_start|>assistant\n"
        )

        return prompt

    def __render_history(
        self, enable_generation: bool = False
    ) -> Union[List[Tuple[str, str]], str]:
        """
        Render the conversation history.

        :param enable_generation: If True, return the history as a single string.
                                If False, return the history as a list of tuples.
        :type enable_generation: bool
        :return: The conversation history, either as a string or a list of tuples.
        :rtype: Union[List[Tuple[str, str]], str]
        """
        if enable_generation:
            return "".join(
                f"{'|im_start|user' if msg['role'] == 'user' else '|im_start|assistant'}: {msg['content']} |im_end|\n"
                for msg in self.history
            )
        else:
            return [
                (
                    (
                        "<|im_start|>user"
                        if msg["role"] == "user"
                        else "<|im_start|>assistant"
                    ),
                    msg["content"] + "<|im_end|>",
                )
                for msg in self.history[:-1]
            ]
