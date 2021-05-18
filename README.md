# Thumbnail_Generator
FastAPI based thumbnail generator.

#### Live on AWS - [Click here for Semantic UI version](http://18.168.150.167/)
#### Live on AWS - [Click here for Bootstrap version](http://18.168.197.105/)  (Offline)

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/mateuszwwwrobel/Thumbnail_Generator.git
$ cd Thumbnail_Generator
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv <venv-name>
$ source <venv-name>/bin/activate
```

Then install the dependencies:

```sh
(<venv-name>)$ pip install -r requirements.txt
```
Note the `(venv-name)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:
```sh
(<venv-name>)$ uvicorn main:app --reload
```
And navigate to `http://127.0.0.1:8000/`

### List of environment variables needed
    os.environ["AWS_ACCESS_KEY_ID"] = ""
    os.environ["AWS_SECRET_ACCESS_KEY"] = ""
    os.environ["CLOUDFRONT_URL"] = ""
    os.environ["SOURCE_BUCKET"] = "
    os.environ["RESIZED_BUCKET"] = ""

### Dependencies

See requirements.txt file. 

### Running tests

In main directory run command:
```sh
(<venv-name>)$ pytest
```

## Acknowledgments

For help with every trouble:
* [Stackoverflow](https://stackoverflow.com/)
