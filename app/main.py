from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.script_generator import generate_script_package
from pathlib import Path
import os
import threading
import time

app = FastAPI()

origins = [
    "https://winget.gareth.tips",
    "https://intune.gareth.tips",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # ← This is the critical line
)

def schedule_cleanup(file_path: str, delay: int = 30):
    """Delete the .zip and its associated output folder after a delay"""
    def cleanup():
        try:
            time.sleep(delay)
            # Delete ZIP file
            os.remove(file_path)

            # Delete associated output folder
            output_folder_name = Path(file_path).stem.replace("_package_", "-")
            output_folder = Path("./output") / output_folder_name
            if output_folder.exists():
                for file in output_folder.glob("*"):
                    file.unlink()
                output_folder.rmdir()

            print(f"🧹 Cleaned up: {file_path} and {output_folder}")
        except Exception as e:
            print(f"⚠️ Cleanup failed: {e}")
    threading.Thread(target=cleanup, daemon=True).start()

@app.post("/generate")
def generate_package(app_id: str = Form(...), app_name: str = Form(...)):
    package_path = generate_script_package(app_id, app_name)
    filename = Path(package_path).name
    schedule_cleanup(package_path)  # 🧼 Schedule file deletion in background
    return FileResponse(package_path, filename=filename, media_type="application/zip")