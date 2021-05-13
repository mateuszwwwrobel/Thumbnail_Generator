import os
import uuid
from fastapi import FastAPI, File, UploadFile, Response, status, Request
from utils import validate_mime_type, upload_file_to_s3, resize_image
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cache.cache import CacheMemory
from S3Resource.S3Resource import S3Resource

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
cache = CacheMemory()


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/images/")
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    if validate_mime_type(file.content_type):
        file_extension = file.content_type.split('/')[1]
        file.filename = f"{uuid.uuid4()}.{file_extension}"
        contents = await file.read()

        upload_file_to_s3(contents, file.filename, file_extension)
        return templates.TemplateResponse(
            "upload.html", {
                "request": request,
                "filename": file.filename,
                "message": "Image has been uploaded.",
                "status": "success"
            })

    return templates.TemplateResponse(
        "upload.html", {
            "request": request,
            "message": "Invalid file format. Please try again.",
            "status": "fail"
        })


@app.get('/images/{dimensions}')
async def get_thumbnail(dimensions: str, response: Response):
    cached_url = cache.check_cache(dimensions, 1)
    if cached_url:
        return {
            'img_url': cached_url,
            "message": "Thumbnail has been created within last hour."}

    try:
        width, height = [int(dimension) for dimension in dimensions.split('x')]
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Your dimensions are invalid. Please try again."}

    if width <= 0 or height <= 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Height and width must be greater then 0."}

    s3_resource = S3Resource()
    img = s3_resource.get_random_file(os.getenv('SOURCE_BUCKET'))
    if img:
        resized_image_url = resize_image(img, width, height)
        cache.add_cache(dimensions, resized_image_url)
        return {'message': f"Thumbnail {dimensions} successfully created",
                'img_url': resized_image_url}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Please upload images in order to create a thumbnail."}
