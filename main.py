from fastapi import FastAPI, Response, status

from PIL import Image


app = FastAPI()


images = []


@app.get("/")
def root():
    return "Welcome in Thumbnail Generator"


@app.post('/images')
def save_image():
    image = Image.open('earth.jpg')

    images.append(image)
    print(images)

    return {"message": "Photo added to database."}


@app.get('/images/{dimensions}')
def get_thumbnail(dimensions: str, response: Response):
    try:
        width, height = [int(dimension) for dimension in dimensions.split('x')]
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Your URL '/images/{dimensions}' is invalid. Please try again."}

    return {"width": width, "height": height}
