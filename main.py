from fastapi import FastAPI, File, UploadFile, Response, status, Request
import uuid
from utils import validate_mime_type, upload_file_to_s3, get_file_from_s3, resize_image
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/images/")
async def create_upload_file(response: Response, file: UploadFile = File(...)):
    # opcja na plik z linku też?

    if validate_mime_type(file.content_type):
        file_extension = file.content_type.split('/')[1]
        file.filename = f"{uuid.uuid4()}.{file_extension}"
        contents = await file.read()
        upload_file_to_s3(contents, file.filename, file_extension)
        return {"filename": file.filename}

    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"message": f"Invalid file format."}


@app.get('/images/{dimensions}')
async def get_thumbnail(dimensions: str, response: Response):
    try:
        width, height = [int(dimension) for dimension in dimensions.split('x')]
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Your URL '/images/{dimensions}' is invalid. Please try again."}

    img = get_file_from_s3()
    if img:
        resized_image_url = resize_image(img, width, height)
        return resized_image_url

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": f"Please upload images in order to create a thumbnail."}
