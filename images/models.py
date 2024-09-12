from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    original_url = models.URLField(max_length=255)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.filename} uploaded by {self.user.username}"
    
class ImageTransformation(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="transformations")
    transformation_type = models.CharField(max_length=50)
    transformation_parameters = models.JSONField()
    transformed_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transformation {self.transformation_type} on {self.image}"    