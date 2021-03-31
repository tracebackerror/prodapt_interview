import json
import logging
import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django_tables2 import SingleTableView

from .models import Post, Comments
from .tables import PostTable

def ping(request):
    return HttpResponse("Hello, world. I am alive.")



class ETLView(View):
    exception_format = "Exception raised at :: {}"
    post_url = "https://jsonplaceholder.typicode.com/posts"
    comment_url = "https://jsonplaceholder.typicode.com/comments"
    
    def fetch_contents(self, url, *args, **kwargs):
        raw_contents = urllib.request.urlopen(url).read()

        post = json.loads(raw_contents)
        
        return post
        
    def dump_post(self, posts, *args, **kwargs):
        _post_model_obj = []
        try:
            for each_posts in posts:
                post_ = Post(id = each_posts["id"],
                             user_id = int(each_posts["userId"]),
                             title = str(each_posts["title"]),
                             body = str(each_posts["body"]).strip()
                )
                _post_model_obj.append(post_)
            Post.objects.bulk_create(_post_model_obj)
        except Exception as e:
            logging.error(self.exception_format.format("Post Dump"))
            logging.error(str(e))
            return False, str(e)
        return True, len(_post_model_obj)
        
    def dump_comments(self, comments, *args, **kwargs):
        _cm_model_obj = []
        print(comments)
        try:
            for each_comments in comments:
                comments_ = Comments(id = int(each_comments["id"]),
                                     name = str(each_comments["name"]).strip(),
                                     email = str(each_comments["email"]).strip(),
                                     body = str(each_comments["body"]).strip(),
                                     post = Post.objects.get(id=each_comments["postId"])
                )
                _cm_model_obj.append(comments_)
                
            Comments.objects.bulk_create(_cm_model_obj)
                
        except Exception as e:
            logging.error(self.exception_format.format("Comments Dump"))
            logging.error(str(e))
            return False, str(e)
        return True, len(_cm_model_obj)
        
    def get(self, request):
        posts = self.fetch_contents(self.post_url)
        status_, total_post_ = self.dump_post(posts)
        
        comments = self.fetch_contents(self.comment_url)
        status_, total_post_ = self.dump_comments(comments)
        
        return redirect("/")
        
class WipeView(View):   
    def get(self, request):
        Comments.objects.all().delete()
        Post.objects.all().delete()
        return redirect("/")
        
class PostListView(SingleTableView):
    model = Post
    table_class = PostTable
    template_name = 'post.html'
    