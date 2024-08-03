# Meme Explainer

## Run Locally

Set your `OPENAI_API_KEY` environment variable to your OpenAI API key.

- Linux/macOS: `export OPENAI_API_KEY=YOUR_API_KEY`
- Windows: `set OPENAI_API_KEY=YOUR_API_KEY`


### Quick Test
For a quick test, you can run the explainer.py script with the following command:
```bash
(venv) $ python explainer.py
```



## Backend
FastAPI Server (python 3.10+)
```bash
(venv) $ # set your OPENAI_API_KEY environment variable
(venv) $ pip install -r requirements.txt
(venv) $ fastapi dev api.py
```

## Frontend
React App:
```bash
# set your REACT_APP_API_URL environment variable
cd frontend
npm install
npm start
```

### .env file
If you want to use the `.env` file you can use the following command to set your environment variables:
```bash
$ export $(xargs < .env)
```