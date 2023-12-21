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
        The conversation between doctor and patient. Please, mention the ICD-10 and CPT codes from your medical knowledge even though it is not in the conversation and extract the information from the conversation and . Answer it in given format. :{x}

        Subjective:
        State all the complains and symptoms faced by the patient, with history of present illness. 

        Objective:
        Vital Signs:
        Physical Examination:
        Diagnostic Tests:

        Assessment:
        Diagnosis: [Primary and secondary diagnoses] (ICD codes: [ICD-10 codes])

        Plan:
        Treatment: [Medications]
        Patient Education: [Information provided to the patient]
        Follow-up: [Return date, monitoring details]
        Procedural Codes (CPT): [CPT codes]"""
    
    subjective = send_message(user_input)

    return {subjective}


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
