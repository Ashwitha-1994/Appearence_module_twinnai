# Appearence_module_twinnai
Demo of image/video upload file picker
# Architecture
Backend flow
User clicks Upload
        ↓
Select Image / Video
        ↓
Frontend sends file to FastAPI
        ↓
FastAPI validates file type
        ↓
Unique filename generated
        ↓
File saved in uploads/
        ↓
Metadata stored in MongoDB
        ↓
Preview URL returned
        ↓
Frontend displays preview
