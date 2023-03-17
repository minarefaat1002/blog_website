from django.db import models

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from users.models import Profile
from ckeditor.fields import RichTextField
# Create your models here.

def user_directory_path(instance,filename):
    return 'blogs/{0}/{1}'.format(instance.id,filename)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Blog(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    likes = models.ManyToManyField(Profile,related_name="blogs",null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,default=1)
    favorites = models.ManyToManyField(Profile,related_name='favorite',default=None,blank=True)
    likes = models.ManyToManyField(Profile,related_name='like',default=None,blank=True)
    featured_image = models.ImageField(null=True, blank=True,upload_to=user_directory_path, default="default.jpg")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    @property
    def total_likes(self):
        return self.likes.count()
    @property
    def total_comments(self):
        return self.comments.count()
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

class Comment(models.Model):
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"comment by {self.owner}"

