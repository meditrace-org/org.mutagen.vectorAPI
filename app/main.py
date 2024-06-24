import numpy as np
import torch
import time
from transformers import AutoModel, pipeline
from fastapi import FastAPI, BackgroundTasks
from .index import update_index, get_top

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
clip = AutoModel.from_pretrained("jinaai/jina-clip-v1", trust_remote_code=True).to(
    device
)
opus = pipeline("translation", model="Helsinki-NLP/opus-mt-ru-en", device=device)


app = FastAPI()


@app.get("/")
async def default():
    return "Ok"


@app.get("/get")
async def read_item(input: str):
    print(input)
    if len(input) > 0:
        start = time.time()
        text_en = opus(input)[0]["translation_text"]
        emb = clip.encode_text(text_en).astype(np.float16)

        return {"time": round(time.time() - start, 2), "result": emb.tolist()}

    else:
        return "Empty String"


@app.get("/get_index")
async def read_item(input: str, top: int = 100):
    print(input)
    if len(input) > 0:
        start = time.time()
        text_en = opus(input)[0]["translation_text"]
        emb = clip.encode_text(text_en).astype(np.float16)
        send = get_top(emb, top)
        return {"time": round(time.time() - start, 2), "result": send}

    else:
        return "Empty String"


@app.get("/rebuild_index")
async def read_item(background_tasks: BackgroundTasks):

    background_tasks.add_task(update_index)
    return {"status": "In Progress"}
