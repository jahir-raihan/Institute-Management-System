from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from PIL import Image
from django.utils import timezone

User = get_user_model()


# Create your models here.

class Post(models.Model):

    """This model is used for posting a notice or anything
        Valuable for students in HOME|Feed."""

    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, upload_to='post_images/', null=True)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        """Overriding save method to reduce  size of uploaded image."""

        super(Post, self).save(*args, **kwargs)
        if self.image:

            image = Image.open(self.image.path)
            print(image.size)

            if image.width > 400 or image.height > 400:
                output_size = (400, 400)
                image.thumbnail(output_size)
                image.save(self.image.path)
                print(image.size)

    def __str__(self):
        return self.title


class Comment(models.Model):

    """This model build on top of a post.
        Every post can contain numerous comment.
        Every one can comment on a notice/post."""

    comment = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'( {self.post.title} ) comment'


class Liked(models.Model):

    """This model is for tracking likes .
        ex: If a user already liked a post then
        the user cannot like the post again because
        the like data is being saved at here to avoid
        collision."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self): 
        return f'( {self.user} ) liken on {self.post}'


# notification section

class Notifications(models.Model):

    """When a post being made this model saves the post data
        including author , and time when the post has been
        made .
        This model is being used for notification system."""

    notification = models.CharField(max_length=200)
    notification_author = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_date = models.DateTimeField(default=timezone.now)
    post_id = models.IntegerField()

    def __str__(self):
        return self.notification
