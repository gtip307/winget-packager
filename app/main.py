from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from app.script_generator import generate_script_package

app = FastAPI()

@app.post("/generate")
def generate_package(app_id: str = Form(...), app_name: str = Form(...)):
    package_path = generate_script_package(app_id, app_name)
    return FileResponse(package_path, filename="winget_package.zip", media_type="application/zip")
