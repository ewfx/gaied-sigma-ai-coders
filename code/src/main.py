from fastapi import FastAPI, File, UploadFile
import shutil

app = FastAPI()
UPLOAD_FOLDER = "emails"
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Save file to the upload directory
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "file_location": file_location}