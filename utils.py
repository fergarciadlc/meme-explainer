import logging
import base64
import os
import yaml
from typing import Any, Dict, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load YAML file
yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.yaml")
with open(yaml_path, "r", encoding="utf-8") as file:
    prompts = yaml.safe_load(file)

# Set up Jinja environment
jinja_env = Environment(
    loader=FileSystemLoader(searchpath=os.path.dirname(os.path.abspath(__file__))),
    autoescape=select_autoescape(),
)


def get_system_prompt(lang: str = "en") -> str:
    """Returns the system prompt for the specified language."""
    try:
        prompt = prompts[lang]["system"]
        logger.debug(f"Retrieved system prompt for language '{lang}'")
        return prompt
    except KeyError:
        logger.error(f"Language '{lang}' not found in prompts file")
        raise ValueError(f"Unsupported language: '{lang}'")


def get_user_prompt(question: str, lang: str = "en") -> str:
    """Renders the user prompt template with the provided question for the specified language."""
    # fmt: off
    try:
        template = Template(prompts[lang]["user"])
        rendered_prompt = template.render(prompt=question)
        logger.debug(f"Rendered user prompt for language '{lang}' with question: {question}")
        return rendered_prompt
    except KeyError:
        logger.error(f"Language '{lang}' not found in prompts file")
        raise ValueError(f"Unsupported language: '{lang}'")
    except Exception as e:
        logger.error(f"Error rendering user prompt: {str(e)}")
        raise
    # fmt: on


def encode_image(image_path: str) -> str:
    """Encodes an image file to a base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
        logger.debug(f"Successfully encoded image: {image_path}")
        return encoded
    except Exception as e:
        logger.error(f"Error encoding image {image_path}: {str(e)}")
        raise


# TODO: currently unused, remove later...
def process_template(template_file: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Renders a Jinja2 template with optional data."""
    # fmt: off
    try:
        template = jinja_env.get_template(template_file)
        if data is None:
            rendered_template = template.render()
            logger.debug(f"Rendering template {template_file} without data:\n{rendered_template}")
        else:
            rendered_template = template.render(**data)
            logger.debug(f"Rendering template {template_file} with data {data}:\n{rendered_template}")
        return rendered_template
    except Exception as e:
        logger.error(f"Error processing template {template_file}: {str(e)}")
        raise
    # fmt: on
