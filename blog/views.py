from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import TicketForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    latest_posts = posts.order_by('-published_date')[:8]
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
def ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)   
            ticket.name = "unknown"              
            ticket.save()
            messages.success(request, "Your ticket was successfully registered")
            return redirect('ticket_success')
        else:
            messages.error(request, "please check again form")
    else:
            
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "blog/login.html"
    
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(request, username=user.username, password=raw_password)
            login(request, user)
            return redirect("post_list")
    else:
        form = SignUpForm()
    return render(request, "blog/signup.html", {"form":form})