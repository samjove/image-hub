from rest_framework import serializers
from .models import Image, ImageTransformation

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'filename', 'original_url', 'file_type', 'created_at']
        read_only_fields = ['id', 'original_url', 'file_type', 'created_at']

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
     
        image.original_url = upload_to_s3(image.file) 
        image.save()
        return image

class ImageTransformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTransformation
        fields = ['id', 'image', 'transformation_type', 'transformation_parameters', 'transformed_url', 'created_at']
        read_only_fields = ['id', 'transformed_url', 'created_at']

    def create(self, validated_data):
        transformation = ImageTransformation.objects.create(**validated_data)
        
        transformation.transformed_url = apply_transformation_and_upload(
            transformation.image, transformation.transformation_parameters
        ) 
        
        transformation.save()
        return transformation
