from fastapi import FastAPI, Query

app = FastAPI()

import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ.get('api_key')


def send_message(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=3800,
        stop=None,
        temperature=0.7,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content


@app.get("/get_assessment/")
async def get_assessment(x: str = Query(..., title="User Input")):
    user_input = f"""
        Please, do mention the ICD-10 and CPT codes from your medical knowledge even it is not mentioned in the conversation. Answer it in given format. The conversation between doctor and patient.:{x}

        Plan:
        Treatment:
        Procedural Codes (CPT) for tests:
    """
    subjective = send_message(user_input)

    return {"plan": subjective}


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
