import logging
import base64
from typing import Any, Dict, Optional
from functools import partial
from jinja2 import Environment, FileSystemLoader, select_autoescape


def process_template(template_file: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Renders a Jinja2 template with optional data."""
    jinja_env = Environment(
        loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
    )
    template = jinja_env.get_template(template_file)
    if data is None:
        rendered_template = template.render()
        logging.debug(
            f"Rendering template {template_file} without data:\n{rendered_template}"
        )
        return rendered_template
    rendered_template = template.render(**data)
    logging.debug(
        f"Rendering template {template_file} with data {data}:\n{rendered_template}"
    )
    return rendered_template


get_system_prompt = partial(
    process_template,
    template_file="prompts/system.jinja",
)


def get_user_prompt(question: str) -> str:
    """Renders the user prompt template with the provided question."""
    return process_template(
        template_file="prompts/user.jinja",
        data={"prompt": question},
    )


def encode_image(image_path: str) -> str:
    """Encodes an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
