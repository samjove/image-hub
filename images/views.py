import boto3
from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageSerializer
from .models import Image

# Create your views here.

s3 = boto3.client(
    's3',
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
    region_name = settings.AWS_S3_REGION_NAME
)
class ImageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        images = Image.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Image not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            s3.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                image_file.name,
                ExtraArgs={'ContentType': image_file.content_type}
            )
            
            image = Image.objects.create(
                user=request.user,
                original_url=f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_file.name}',
                filename=image_file.name,
                file_type=image_file.content_type.split('/')[-1]
            )
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ImageTransformationAPIView(APIView):
    pass