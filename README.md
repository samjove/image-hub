# Image Processing Service
A Django-based image processing service that allows users to upload images, apply various transformations, and retrieve images. The service supports user registration, login, and transformation operations. It uses AWS S3 for image storage and handles transformations with PIL.


## Copy code
`git clone https://github.com/samjove/image-processing-service.git`

`cd image-processing-service`

## Create and Activate a Virtual Environment

`python -m venv venv`

`source venv/bin/activate`  

On Windows use 

`venv\Scripts\activate`

## Install Dependencies

`pip install -r requirements.txt`

## Create a .env File

Create a .env file in the root directory of the project with the following content:

`AWS_ACCESS_KEY_ID=your-access-key-id`

`AWS_SECRET_ACCESS_KEY=your-secret-access-key`

`AWS_S3_BUCKET_NAME=your-bucket-name`

Along with information for your postgres DB instance, which you'll later spin up with Docker and Docker Compose.

`DB_ENGINE=django.db.backends.postgresql`

`DB_NAME=your-db-name`

`DB_USER=your-db-user`

`DB_PASSWORD=your-db-password`

`DB_HOST=your-db-host`

`DB_PORT=your-db-port`

## Run Docker

`docker-compose up --build`

## Run Migrations

`python manage.py migrate`

## AWS S3 Setup

Ensure you have an S3 bucket created in AWS. Update your .env file with the appropriate AWS credentials and bucket name.

## Running the Application

Start the Development Server

`python manage.py runserver`

Access the Application

Open your web browser and go to http://127.0.0.1:8000.

## API Endpoints

### User Registration

Endpoint:  POST `/users/register/`

Request Body:

    {
        "username": your-user,
        "email": your-email
        "password": your-password
    }

### User Login

Endpoint: POST `/api/token/`

Request Body:

    {
        "username": your-user,
        "password": your-password
    }

Response:

    {
        "refresh": your-jwt-refresh-token,
        "access": your-jwt-access-token
    }

Note the access token. It will be used as an authorization bearer token for your other requests.

### Upload Image

Endpoint: POST `/images/`

Headers:
Authorization: Bearer your-jwt-access-token

Request Body: Multipart form-data with an image file

Example Response:

    {
        "id": 1,
        "filename": "image.PNG",
        "original_url": "https://example-bucket.s3.amazonaws.com/image.PNG",
        "file_type": "png",
        "created_at": "2024-09-12T18:28:39.297899Z"
    }

### Retrieve Image

Endpoint: GET `/images/`

Example Response:

    [
        {
            "id": 1,
            "filename": "image1.jpg",
            "original_url": "https://your-bucket-name.s3.amazonaws.com/image1.jpg",
            "file_type": "jpeg",
            "created_at": "2024-09-12T13:48:13.103043Z"
        },
        {
            "id": 2,
            "filename": "image2.PNG",
            "original_url": "https://your-bucket-name.s3.amazonaws.com/image2.PNG",
            "file_type": "png",
            "created_at": "2024-09-12T18:28:39.297899Z"
        }
    ]

### Transform Image

Endpoint: POST `/images/<id>/transform/`

Headers:

Authorization: Bearer your-jwt-access-token

Example Request Body:

    {
        "transformation_type": "resize",
        "transformation_parameters": {
            "width": 800,
            "height": 600
        }
    }

Example Response:

    {
        "message": "Image transformation successful.",
        "transformed_image_url": "https://your-bucket-name.s3.amazonaws.com/transformed-image.jpg?<signature-params>",
        "expires_in": 3600
    }

The following transformation types are available, including their required paramaters:
    
    resize
        - width
        - height
    
    crop
        - x
        - y
        - width
        - height
    
    rotate
    
    watermark
        - image
        - position
    
    flip
    
    mirror
    
    compress
        - quality
    
    format
    
    filters
        - grayscale
        - sepia