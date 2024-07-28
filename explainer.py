import logging
from typing import List, Dict, Any, Tuple, Optional
from utils import encode_image, get_system_prompt, get_user_prompt

from openai import OpenAI
from openai.types.chat import ChatCompletion


class MemeExplainer:
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_MAX_TOKENS = 300
    DEFAULT_IMAGE_DETAIL = "low"

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        default_model: str = DEFAULT_MODEL,
        language: str = "en",
    ):
        self.logger = logging.getLogger(__name__)
        self.client = OpenAI(api_key=openai_api_key)
        self.set_default_model(default_model)
        self.language = language

    # Configuration methods
    def set_default_model(self, model: str) -> None:
        """Sets the default model for Meme Explainer Class."""
        available_models = self.get_available_models()
        if model not in available_models:
            logging.debug(f"Available models: {available_models}")
            raise ValueError(f"Model {model} is not supported.")
        self.logger.info(f"Setting default model to {model}")
        self.default_model = model

    def set_language(self, language: str) -> None:
        """Sets the language."""
        self.language = language

    # API interaction methods
    def send_request_to_api(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        max_tokens: Optional[int] = None,
    ) -> ChatCompletion:
        """Sends a request to the OpenAI API."""
        max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS
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
        model = model or self.default_model
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
        detail: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> ChatCompletion:
        """Sends an image request to the OpenAI API."""
        model = model or self.default_model
        max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS
        detail = detail or self.DEFAULT_IMAGE_DETAIL
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

    # Explanation methods
    def fetch_image_explanation(
        self, image_path: str, model: str = None, language: Optional[str] = None
    ) -> str:
        lang = language or self.language
        resp = self.send_image_request_to_api(
            image_url=self.get_image_url_from_path(image_path),
            system_content=get_system_prompt(lang=lang),
            model=model,
        )
        return self.parse_model_response(resp)

    def fetch_text_explanation(
        self, prompt: str, model: str = None, language: Optional[str] = None
    ) -> str:
        lang = language or self.language
        resp = self.send_text_request_to_api(
            user_content=get_user_prompt(prompt, lang=lang),
            system_content=get_system_prompt(lang=lang),
            model=model,
        )
        return self.parse_model_response(resp)

    # Utility methods
    @staticmethod
    def parse_model_response(resp: ChatCompletion) -> str:
        """Parses the response from the OpenAI API."""
        if resp and resp.choices:
            return resp.choices[0].message.content
        return "No response received from the model."

    @staticmethod
    def get_image_url_from_path(image_path: str) -> str:
        """Encodes an image file to a base64 URL."""
        return "data:image/jpeg;base64," + encode_image(image_path)

    def get_available_models(self) -> Tuple[str]:
        """Gets the list of available models from the OpenAI API."""
        models = self.client.models.list()
        return tuple([model.id for model in models.data])


def __test_explainer() -> None:
    import logging

    logging.basicConfig(level=logging.INFO)
    explainer = MemeExplainer()
    print("*" * 100)
    print("Testing for Text")
    prompt = "Why did the Python programmer get cold during the winter? Because they didn't C# 😄🐍"
    print("English")
    print(explainer.fetch_text_explanation(prompt))
    print("Spanish")
    print(explainer.fetch_text_explanation(prompt, language="es"))

    print("*" * 100)
    print("Testing for IMAGE")
    image_path = "examples/x_post.png"
    print(explainer.fetch_image_explanation(image_path=image_path, model="gpt-4o"))


if __name__ == "__main__":
    __test_explainer()
