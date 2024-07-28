import logging
import base64
import os
from typing import Any, Dict, Optional
from functools import partial
from jinja2 import Environment, FileSystemLoader, select_autoescape

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jinja_env = Environment(
    loader=FileSystemLoader(searchpath=os.path.dirname(os.path.abspath(__file__))),
    autoescape=select_autoescape(),
)


def process_template(template_file: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Renders a Jinja2 template with optional data."""
    try:
        template = jinja_env.get_template(template_file)
        if data is None:
            rendered_template = template.render()
            logger.debug(
                f"Rendering template {template_file} without data:\n{rendered_template}"
            )
        else:
            rendered_template = template.render(**data)
            logger.debug(
                f"Rendering template {template_file} with data {data}:\n{rendered_template}"
            )
        return rendered_template
    except Exception as e:
        logger.error(f"Error processing template {template_file}: {str(e)}")
        raise


get_system_prompt = partial(process_template, template_file="prompts/system.jinja")
get_system_prompt.__doc__ = "Renders the system prompt template."


def get_user_prompt(question: str) -> str:
    """Renders the user prompt template with the provided question."""
    return process_template(
        template_file="prompts/user.jinja",
        data={"prompt": question},
    )


def encode_image(image_path: str) -> str:
    """Encodes an image file to a base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {str(e)}")
        raise
