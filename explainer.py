from functools import partial
from dataclasses import dataclass, asdict
from typing import Dict

from openai import OpenAI
from openai.types.chat import ChatCompletion

from utils import encode_image, get_system_prompt, get_user_prompt


@dataclass
class Models:
    GPT3_TURBO: str = "gpt-3.5-turbo"
    GPT4_TURBO: str = "gpt-4-turbo"
    GPT4O: str = "gpt-4o"

    def dict(self) -> Dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}


models = Models()

client = OpenAI()
system_prompt = get_system_prompt()


def send_text_request(
    user_content: str, system_content: str, model: str = models.GPT3_TURBO
) -> ChatCompletion:
    """
    Sends a text request to the OpenAI API.

    Args:
        user_content (str): The content provided by the user.
        system_content (str): The content provided by the system.
        model (str): The model to use for the request. Default is GPT3_TURBO.

    Returns:
        ChatCompletion: The response from the OpenAI API.
    """
    return client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
    )


def send_image_request(
    image_url: str, system_content: str, model: str = models.GPT4O, detail: str = "low"
) -> ChatCompletion:
    """
    Sends an image request to the OpenAI API.

    Args:
        image_url (str): The URL of the image to analyze.
        system_content (str): The content provided by the system.
        model (str): The model to use for the request. Default is GPT4O.
        detail (str): The detail level of the image. Default is "low".

    Returns:
        ChatCompletion: The response from the OpenAI API.
    """
    return client.chat.completions.create(
        model=model,
        messages=[
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
        ],
        max_tokens=300,
    )


def retrieve_ai_answer(response: ChatCompletion) -> str:
    """
    Retrieves the AI's answer from the response.

    Args:
        response (ChatCompletion): The response from the OpenAI API.

    Returns:
        str: The content of the AI's answer.
    """
    return response.choices[0].message.content


def get_image_url_from_path(image_path: str) -> str:
    """
    Encodes an image file to a base64 URL.

    Args:
        image_path (str): The file path of the image.

    Returns:
        str: The base64-encoded URL of the image.
    """
    return "data:image/jpeg;base64," + encode_image(image_path)


def get_image_explanation(image_path: str, model: str) -> str:
    """
    Gets an explanation for an image from the OpenAI API.

    Args:
        image_path (str): The file path of the image.

    Returns:
        str: The explanation for the image.
    """
    resp = send_image_request(
        image_url=get_image_url_from_path(image_path),
        system_content=system_prompt,
        model=model,
    )
    return retrieve_ai_answer(resp)


def get_text_explanation(prompt: str, model: str) -> str:
    """
    Gets an explanation for a text prompt from the OpenAI API.

    Args:
        prompt (str): The text prompt to explain.
        model (str): The model to use for the request.

    Returns:
        str: The explanation for the text prompt.
    """
    resp = send_text_request(
        user_content=get_user_prompt(prompt),
        system_content=system_prompt,
        model=model,
    )
    return retrieve_ai_answer(resp)


get_gpt3_explanation = partial(get_text_explanation, model=models.GPT3_TURBO)
get_gpt4_explanation = partial(get_text_explanation, model=models.GPT4_TURBO)
get_gpt4o_text_explanation = partial(get_text_explanation, model=models.GPT4O)
get_gpt4o_image_explanation = partial(get_image_explanation, model=models.GPT4O)


def __test_explainer():
    print("*" * 100)
    print("Testing for GPT-3.5-turbo")
    prompt = "Why did the Python programmer get cold during the winter? Because they didn't C# 😄🐍"
    print(get_gpt3_explanation(prompt))

    print("*" * 100)
    print("Testing for GPT-4o IMAGE")
    image_path = "examples/x_post.png"
    print(get_gpt4o_image_explanation(image_path))


if __name__ == "__main__":
    __test_explainer()
