import pathlib
import uuid
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests as rq
from fastapi.middleware.cors import CORSMiddleware
import pathlib
app = FastAPI()

# We want to be flexible in our localhost demo so we'll set
# very open CORS policies.
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Text(BaseModel):
    text: str


# This endpoint returns our HTML page.
@app.get("/", response_class=HTMLResponse)
def index():
    html=pathlib.Path("index1.html").read_text()
    return HTMLResponse(content=html,status_code=200)


# This endpoint will receive texts, proxy to Rasa and return parsed results.
@app.post("/api/")
def post_attempt(text: Text):
    body = {
      "text": text.text,
      "message_id": str(uuid.uuid4())
    }
    url = "http://localhost:5005/model/parse"
    return rq.post(url, json=body).json()


@app.get("/status/")
def get_attempt():
    return {"status": "alive"}