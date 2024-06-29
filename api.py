from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from explainer import MemeExplainer
import os
from typing import Dict
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize MemeExplainer
meme_explainer = MemeExplainer()


class TextExplanationRequest(BaseModel):
    text: str


@app.post("/explain/text")
async def explain_text(request: TextExplanationRequest) -> Dict[str, str]:
    try:
        explanation = meme_explainer.get_gpt3_explanation(request.text)
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"Error explaining text: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text explanation")


@app.post("/explain/image")
async def explain_image(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an image."
        )

    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        explanation = meme_explainer.get_gpt4o_image_explanation(temp_file_path)
        return {"explanation": explanation}
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
