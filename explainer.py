import logging
from typing import Dict
from dataclasses import dataclass, asdict
from utils import encode_image, get_system_prompt, get_user_prompt

from openai import OpenAI
from openai.types.chat import ChatCompletion


@dataclass
class Models:
    GPT3_TURBO: str = "gpt-3.5-turbo"
    GPT4_TURBO: str = "gpt-4-turbo"
    GPT4O: str = "gpt-4o"

    def dict(self) -> Dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}


class MemeExplainer:
    def __init__(self, openai_api_key: str = None):
        self.models = Models()
        self.client = OpenAI(api_key=openai_api_key)
        self.system_prompt = get_system_prompt()
        self.logger = logging.getLogger(__name__)

    def send_request_to_api(
        self, messages: list, model: str, max_tokens: int = None
    ) -> ChatCompletion:
        """Sends a request to the OpenAI API."""
        try:
            self.logger.info(f"Sending request to model: {model}")
            return self.client.chat.completions.create(
                model=model, messages=messages, max_tokens=max_tokens
            )
        except Exception as e:
            self.logger.error(f"API request failed: {e}")
            return None

    def send_text_request_to_api(
        self,
        user_content: str,
        system_content: str,
        model: str = None,
        max_tokens: int = None,
    ) -> ChatCompletion:
        """Sends a text request to the OpenAI API."""
        if model is None:
            model = self.models.GPT3_TURBO
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        return self.send_request_to_api(messages, model, max_tokens)

    def send_image_request_to_api(
        self,
        image_url: str,
        system_content: str,
        model: str = None,
        detail: str = "low",
        max_tokens: int = 300,
    ) -> ChatCompletion:
        """Sends an image request to the OpenAI API."""
        if model is None:
            model = self.models.GPT4O
        messages = [
            {"role": "system", "content": system_content},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Why is this funny?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": detail,
                        },
                    },
                ],
            },
        ]
        return self.send_request_to_api(messages, model, max_tokens)

    @staticmethod
    def parse_model_response(resp: ChatCompletion) -> str:
        """Parses the response from the OpenAI API."""
        if resp and resp.choices:
            return resp.choices[0].message.content
        return "No response received from the model."

    def get_image_url_from_path(self, image_path: str) -> str:
        """Encodes an image file to a base64 URL."""
        return "data:image/jpeg;base64," + encode_image(image_path)

    def fetch_image_explanation(self, image_path: str, model: str = None) -> str:
        """Gets an explanation for an image from the OpenAI API."""
        resp = self.send_image_request_to_api(
            image_url=self.get_image_url_from_path(image_path),
            system_content=self.system_prompt,
            model=model,
        )
        return self.parse_model_response(resp)

    def fetch_text_explanation(self, prompt: str, model: str = None) -> str:
        """Gets an explanation for a text prompt from the OpenAI API."""
        resp = self.send_text_request_to_api(
            user_content=get_user_prompt(prompt),
            system_content=self.system_prompt,
            model=model,
        )
        return self.parse_model_response(resp)

    def get_gpt3_explanation(self, prompt: str) -> str:
        return self.fetch_text_explanation(prompt, model=self.models.GPT3_TURBO)

    def get_gpt4_explanation(self, prompt: str) -> str:
        return self.fetch_text_explanation(prompt, model=self.models.GPT4_TURBO)

    def get_gpt4o_text_explanation(self, prompt: str) -> str:
        return self.fetch_text_explanation(prompt, model=self.models.GPT4O)

    def get_gpt4o_image_explanation(self, image_path: str) -> str:
        return self.fetch_image_explanation(image_path, model=self.models.GPT4O)


def __test_explainer() -> None:
    import logging

    logging.basicConfig(level=logging.INFO)
    explainer = MemeExplainer()
    print("*" * 100)
    print("Testing for GPT-3.5-turbo")
    prompt = "Why did the Python programmer get cold during the winter? Because they didn't C# 😄🐍"
    print(explainer.get_gpt3_explanation(prompt))

    print("*" * 100)
    print("Testing for GPT-4o IMAGE")
    image_path = "examples/x_post.png"
    print(explainer.get_gpt4o_image_explanation(image_path))


if __name__ == "__main__":
    __test_explainer()
