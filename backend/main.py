from fastapi import FastAPI
from pydantic import BaseModel
from conversation import handle_message

app = FastAPI()

class Message(BaseModel):
    user_id: str
    text: str

@app.post("/chat")
def chat(msg: Message):
    reply = handle_message(msg.user_id, msg.text)
    return {"reply": reply}
