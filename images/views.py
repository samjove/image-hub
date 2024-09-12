from django.shortcuts import render
import boto3
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

s3 = boto3.client(
    's3',
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
    region_name = settings.AWS_S3_REGION_NAME
)

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        try:
            s3.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                image_file.name,
                ExtraArgs={'ContentType': image_file.content_type}
            )
            return JsonResponse({'message': 'Upload successful', 'file_name': image_file.name})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)