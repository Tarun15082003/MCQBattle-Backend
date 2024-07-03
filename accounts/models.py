from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to = 'profile_images/' , null = True , blank = True)
    user_type = models.CharField(max_length=50,blank=True)
    online_status = models.BooleanField(default=False)
    number_of_games_won = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Friendship(models.Model):
    user1 = models.ForeignKey(UserProfile,related_name="friendship_user1",on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile,related_name="friendship_user2",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"