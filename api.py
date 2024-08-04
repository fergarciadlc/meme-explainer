import os
import logging
from typing import Dict
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from explainer import MemeExplainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SUPPORTED_LANGUAGES = ("en", "es")

app = FastAPI()
meme_explainer = MemeExplainer()
models = {
    "text": "gpt-4o-mini",
    "image": "gpt-4o",
}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class TextExplanationRequest(BaseModel):
    text: str


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def validate_language(
    lang: str = Query(default="en", description="Language for explanation")
):
    if lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}",
        )
    return lang


@app.post("/explain/text")
async def explain_text(
    request: TextExplanationRequest,
    language: str = Depends(validate_language),
) -> Dict[str, str]:
    try:
        explanation = meme_explainer.fetch_text_explanation(
            prompt=request.text,
            model=models["text"],
            language=language,
        )
        return {
            "explanation": explanation,
            "model": models["text"],
            "language": language,
        }
    except Exception as e:
        logger.error(f"Error explaining text: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text explanation")


@app.post("/explain/image")
async def explain_image(
    file: UploadFile = File(...),
    language: str = Depends(validate_language),
) -> Dict[str, str]:
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an image."
        )

    if file.size > 5 * 1024 * 1024:  # 5 MB limit
        raise HTTPException(
            status_code=400,
            detail="File too large. Please upload an image smaller than 5 MB.",
        )

    logger.info(f"Explaining image: {file.filename}")
    # Ensure the tmp directory exists
    tmp_dir = os.getenv("TMP_DIR", "tmp")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    # Create a temporary file path
    temp_file_path = os.path.join(tmp_dir, f"temp_{uuid.uuid4()}_{file.filename}")
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        explanation = meme_explainer.fetch_image_explanation(
            image_path=temp_file_path, model=models["image"], language=language
        )
        return {
            "explanation": explanation,
            "model": models["image"],
            "language": language,
        }
    except ValueError as ve:
        logger.error(f"Value error in image explanation: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error explaining image: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error processing image explanation"
        )
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
