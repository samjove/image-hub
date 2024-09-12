import boto3
import io
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageSerializer, ImageTransformationSerializer
from .models import Image
from PIL import Image as PILImage
from .transformations import apply_transformations

# Initiate boto3 client for S3
s3 = boto3.client(
    's3',
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
    region_name = settings.AWS_S3_REGION_NAME
)
bucket_name = settings.AWS_STORAGE_BUCKET_NAME

class ImageAPIView(APIView):
    # GET action to retrieve user's images
    def get(self, request):
        images = Image.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    
    # POST action to post a new image to the S3 bucket
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Image not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            s3.upload_fileobj(
                image_file,
                bucket_name,
                image_file.name,
                ExtraArgs={
                    'ContentType': image_file.content_type
                    }
            )
            
            # Creates an Image object for the image. Assigns an AWS URL.
            image = Image.objects.create(
                user=request.user,
                original_url=f'https://{bucket_name}.s3.amazonaws.com/{image_file.name}',
                filename=image_file.name,
                file_type=image_file.content_type.split('/')[-1]
            )
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ImageTransformationAPIView(APIView):
    # POST action to submit an image transformation request with an image id, transformation type, and parameters.
    def post(self, request, pk):
        
        serializer = ImageTransformationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            # Fetches image object using id. Then uses the image's filename as a key for the S3 bucket to fetch the image file itself.
            image = Image.objects.get(id=pk, user=request.user)
            fetch_image = s3.get_object(Bucket=bucket_name,Key=image.filename)
            
            # Read the image from s3 into memory.
            # target_image is an Image object from the PIL, based off the original image. It enables transformations.
            image_data = fetch_image['Body'].read()
            target_image = PILImage.open(io.BytesIO(image_data))
            transformation_type = request.data.get('transformation_type')
            transformation_parameters = request.data.get('transformation_parameters')
            transformations = {}
            transformations[transformation_type] = transformation_parameters
            transformed_image = apply_transformations(target_image, transformations)
            if not transformed_image.format:
                transformed_image.format = 'PNG'
            transformed_image_key = f'transformed-{image.filename}'
            
            # Upload transformed image back to S3
            with io.BytesIO() as output:
                transformed_image.save(output, format=transformed_image.format)
                output.seek(0)
                s3.upload_fileobj(
                    output,
                    bucket_name,
                    transformed_image_key,
                    ExtraArgs={
                        'ContentType': f'image/{transformed_image.format.lower()}'
                    }
                )
            
            # Generate a temporary presigned URL with an expiration of 1 hour to present the transformed image.
            expiration_time = 3600
            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': transformed_image_key,
                },
                ExpiresIn=expiration_time
            )
            
            return Response({
                'message': 'Image transformation successful.',
                'transformed_image_url': presigned_url,
                'expires_in': expiration_time
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)