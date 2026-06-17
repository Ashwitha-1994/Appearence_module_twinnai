
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil
import uuid

from database import appearance_collection

app = FastAPI()
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)
# ----------------------------------
# Allowed File Types
# ----------------------------------

IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp"
]

VIDEO_TYPES = [
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo"
]

# ----------------------------------
# Create Upload Folders
# ----------------------------------

os.makedirs(
    "uploads/images",
    exist_ok=True
)

os.makedirs(
    "uploads/videos",
    exist_ok=True
)

# ----------------------------------
# Home Route
# ----------------------------------

@app.get("/")
def home():
    return {
        "message": "Appearance Upload API Running"
    }

# ----------------------------------
# Upload Route
# ----------------------------------

@app.post("/appearance/upload")
async def upload_file(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):

    try:

        print("\n========== NEW UPLOAD ==========")

        print("User ID:", user_id)
        print("Filename:", file.filename)
        print("Content Type:", file.content_type)

        # ----------------------------
        # Validate File Type
        # ----------------------------

        if (
            file.content_type not in IMAGE_TYPES
            and file.content_type not in VIDEO_TYPES
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type"
            )

        # ----------------------------
        # Generate Unique Filename
        # ----------------------------

        unique_name = (
            str(uuid.uuid4())
            + "_"
            + file.filename
        )

        # ----------------------------
        # Select Folder
        # ----------------------------

        if file.content_type in IMAGE_TYPES:
            folder = "uploads/images"
        else:
            folder = "uploads/videos"

        filepath = os.path.join(
            folder,
            unique_name
        )

        # ----------------------------
        # Save File
        # ----------------------------

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        print("File saved:", filepath)

        # ----------------------------
        # Metadata
        # ----------------------------

        metadata = {

            "user_id": user_id,

            "filename": unique_name,

            "original_filename": file.filename,

            "file_type": file.content_type,

            "file_path": filepath

        }

        print("Metadata Created")
        preview_url = (
        f"http://127.0.0.1:8000/uploads/images/{unique_name}"
        )

        # ----------------------------
        # MongoDB Insert
        # ----------------------------

        try:

            appearance_collection.insert_one(
                metadata
            )

            print(
                "MongoDB insert success"
            )

        except Exception as e:

            print(
                "Mongo Error:",
                str(e)
            )

        # ----------------------------
        # Response
        # ----------------------------

        return {

            "success": True,

            "filename": unique_name,

            "filepath": filepath,
            "preview_url": preview_url

        }

    except Exception as e:

        print(
            "UPLOAD ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )