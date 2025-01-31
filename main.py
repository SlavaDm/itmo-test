import os
from dotenv import load_dotenv
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl
from schemas.request import PredictionRequest, PredictionResponse
from utils.get_text_content_from_url import get_text_content_from_url
from utils.google_search import google_search
from openai import OpenAI
import re


app = FastAPI()

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
G_API_KEY = os.getenv("G_API_KEY")
GSE_KEY = os.getenv("GSE_KEY")
PROXY_OPEN_AI_KEY = os.getenv("PROXY_OPEN_AI_KEY")

model = "gpt-4o-mini"

# client = OpenAI(api_key=OPEN_AI_KEY)

client = OpenAI(
    api_key=PROXY_OPEN_AI_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)


@app.post("/api/request", response_model=PredictionResponse)
async def predict(body: PredictionRequest):
    try:
        query = body.query
        lines = query.strip().split("\n")
        question = lines[0]
        variants = [line for line in lines[1:]]

        sources: List[HttpUrl] = [
            item["link"]
            for item in google_search(question, G_API_KEY, GSE_KEY)["items"]
        ]

        filtered_sources = [item for item in sources if ".pdf" not in item]

        text_contents = " ".join(
            [get_text_content_from_url(url) for url in filtered_sources]
        )[:103000]

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """Ты помощник, тебе на вход дают ****** question: '' ******, $$$$$$ variants: [] $$$$$$, |||||| texts: [] ||||||.
                    Тебе нужно сначала попытаться обработать question и variants, затем  тебе на основе texts и variants нужно подорбрать точный ответ из variants: [], если вариант подходит, выведи его число в формате 1-10. 
                    Обоснуй ответ, если нет верного ответа - выведи Ответ: answer=null, иначе Ответ: answer=n, где n число, если ты не уверен, тогда ответ неверный""",
                },
                {
                    "role": "user",
                    "content": f"""****** question: {question} ******, $$$$$$ variants: {variants} $$$$$$, |||||| texts: {text_contents} ||||||""",
                },
            ],
        )

        gpt_text = completion.choices[0].message.content

        pattern = r"Ответ: answer=(\d+|null)"
        match_gpt_answer = re.search(pattern, gpt_text)

        answer_value = None

        if match_gpt_answer:
            answer_value = match_gpt_answer.group(1)
            if answer_value.isdigit() and 1 <= int(answer_value) <= 10:
                answer_value = int(answer_value)
            elif answer_value == "null":
                answer_value = None

        response = PredictionResponse(
            id=body.id,
            answer=answer_value,
            reasoning=f"Ответ сформирован на основе модели {model}. {gpt_text}",
            sources=[] if answer_value == None else sources,
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
