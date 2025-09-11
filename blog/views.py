from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import TicketForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import LoginForm, SignUpForm, PasswordResetRequestForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.core.mail import send_mail

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


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
            messages.error(request, "Please check the form again")
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


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip()
            users = User.objects.filter(email__iexact=email)
            for user in users:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                reset_path = reverse("password_reset_confirm", kwargs={"uidb64":uidb64, "token":token})
                reset_url = request.build_absolute_uri(reset_path)

                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link below to reset your password:\n{reset_url}",
                    from_email="no-reply@myblog.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            messages.success(request, "If an email with this address exists in the system, a recovery link will be sent")
            return redirect("login")
        else:
            form = PasswordResetRequestForm()

        return render(request, "blog/password_reset_request.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password changed successfully. You can now log in")
                return redirect("login")
        else:
            form = SetPasswordForm(user)
        return render(request, "blog/password_reset_confirm.html", {"form":form})
    else:
        messages.error(request, "The recovery link is invalid or expired")
        return redirect("password_reset")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

EXCLUDE_PATHS = ["/admin/"]

def coming_soon(request):
    if request.path in EXCLUDE_PATHS:
        return redirect(request.path)
    return render(request, "coming_soon.html")