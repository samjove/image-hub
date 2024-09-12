from rest_framework import serializers
from .models import Image, ImageTransformation

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'filename', 'original_url', 'file_type', 'created_at']
        read_only_fields = ['id', 'original_url', 'file_type', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ImageTransformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTransformation
        fields = ['id', 'transformation_type', "transformation_parameters", "transformed_url"]

    def create(self, validated_data):
        return super().create(validated_data)
