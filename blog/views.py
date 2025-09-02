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
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post_index = list(posts).index(post)
    prev_post = posts[post_index - 1] if post_index > 0 else None
    next_post = posts[post_index + 1] if post_index < len(posts) - 1 else None
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        
        
    })

# Create your views here.
