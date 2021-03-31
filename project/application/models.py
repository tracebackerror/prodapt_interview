from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    def __str__(self):
        return self.body
        
    class Meta:
      db_table = "post_store"


class Comments(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    body = models.TextField()
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.body
        
    class Meta:
      db_table = "comments_store"