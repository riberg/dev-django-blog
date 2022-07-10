from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Post

class MainView(View):
    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'weblog/home.html', context={
            'page_obj': page_obj
        })

class PostDetailView(View):
    def get(self, reauest, slug):
        post = get_object_or_404(Post, url=slug)
        return render(reauest, 'weblog/post_detail.html', context={
            'post': post
        })