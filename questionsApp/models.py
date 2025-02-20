from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('lecturer', 'Lecturer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='lecturer')

    # Fix conflicts by adding related_name
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True
    )


class MCQ(models.Model):
    subject = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='mcq_images/', blank=True, null=True)

    option_a = models.CharField(max_length=255)
    option_a_image = models.ImageField(upload_to='mcq_images/', blank=True, null=True)

    option_b = models.CharField(max_length=255)
    option_b_image = models.ImageField(upload_to='mcq_images/', blank=True, null=True)

    option_c = models.CharField(max_length=255)
    option_c_image = models.ImageField(upload_to='mcq_images/', blank=True, null=True)

    option_d = models.CharField(max_length=255)
    option_d_image = models.ImageField(upload_to='mcq_images/', blank=True, null=True)

    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    tags = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Assessment Model
class Assessment(models.Model):
    title = models.CharField(max_length=255)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    mcqs = models.ManyToManyField(MCQ)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title