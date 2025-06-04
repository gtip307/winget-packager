# Winget Packager (FastAPI) - Mac Setup

## Setup Instructions:

1. Open Terminal and navigate into the extracted folder.

2. Create a virtual environment:
   python3 -m venv venv

3. Activate it:
   source venv/bin/activate

4. Install requirements:
   pip install -r requirements.txt

5. Run the server:
   uvicorn app.main:app --reload

6. Open your browser to:
   http://127.0.0.1:8000/docs

That's it! 🎉
