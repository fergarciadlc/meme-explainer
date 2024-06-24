import base64
from typing import Any, Dict
from functools import partial

from jinja2 import Environment, FileSystemLoader, select_autoescape


def process_template(template_file: str, data: Dict[str, Any] | None) -> str:
    jinja_env = Environment(
        loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
    )
    template = jinja_env.get_template(template_file)
    if data is None:
        return template.render()
    return template.render(**data)


get_system_prompt = partial(
    process_template,
    template_file="prompts/system.jinja",
)


def get_user_prompt(question: str) -> str:
    return process_template(
        template_file="prompts/user.jinja",
        data={"prompt": question},
    )


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
