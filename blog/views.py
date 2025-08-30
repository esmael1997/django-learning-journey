from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request,'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.counted_view += 1
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

# Create your views here.
