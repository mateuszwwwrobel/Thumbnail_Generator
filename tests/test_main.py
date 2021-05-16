
# endpoint: '/'
def test_homepage_route(test_app):
    response = test_app.get('/')
    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "request" in response.context


# endpoint: '/images/{dimensions}'
def test_thumbnail_successfully_created(s3_file_created, test_app):
    response = test_app.get('/images/400x400/')
    assert response.status_code == 200
    assert response.json()['message'] == 'Thumbnail 400x400 successfully created'


def test_thumbnail_dimensions_0x0(s3_file_created, test_app):
    response = test_app.get('/images/0x0/')
    assert response.status_code == 400
    assert response.json()['message'] == 'Height and width must be greater then 0.'


def test_thumbnail_dimensions_minus_pixels(s3_file_created, test_app):
    response = test_app.get('/images/-100x-50/')
    assert response.status_code == 400
    assert response.json()['message'] == 'Height and width must be greater then 0.'


def test_thumbnail_dimensions_not_correct(s3_file_created, test_app):
    response = test_app.get('/images/string_intead_of_integers/')
    assert response.status_code == 400
    assert response.json()['message'] == 'Your dimensions are invalid. Please try again.'


def test_thumbnail_no_images_in_db_404(s3_test, test_app):
    response = test_app.get('/images/500x500/')
    assert response.status_code == 404
    assert response.json()['message'] == 'Please upload images in order to create a thumbnail.'


def test_thumbnail_created_within_last_hour(s3_file_created, test_app):
    # route called twice
    test_app.get('/images/500x500/')
    response = test_app.get('/images/500x500/')
    assert response.status_code == 200
    assert response.json()['message'] == 'Thumbnail has been created within last hour.'


# endpoint /images/

def test_upload_image_to_db_invalid(test_app, test_file):
    response = test_app.post('/images/',
                             files={'file': test_file})
    assert response.status_code == 200
    assert response.template.name == 'upload.html'
    assert "request" in response.context
    assert response.context['message'] == "Invalid file format. Please try again."
