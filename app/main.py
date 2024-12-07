import uvicorn
from fastapi import FastAPI
from models import FormData
from utils import response_fields

app = FastAPI()

@app.post("/get_form")
async def get_form(form_data: FormData):
    response = response_fields(form_data)
    print(response)
    if isinstance(response, dict):
        return response
    return {"Template name": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
