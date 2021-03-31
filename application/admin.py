from django.contrib import admin
from .models import Post, Comments

class PostAdmin(admin.ModelAdmin):
    fields = ( 'id', 'title', 'body', 'user_id', 'comments')
    list_display  = ( 'id', 'title', 'body', 'user_id')
    
class CommentsAdmin(admin.ModelAdmin):
    fields = ( 'id', 'name', 'email', 'body', 'post')
    list_display  = ( 'id', 'name', 'email', 'body',)
    
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
