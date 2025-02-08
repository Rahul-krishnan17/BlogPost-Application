from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from django.contrib.auth.decorators import login_required
import traceback
from django.contrib import messages

# Create your views here.

#====================Home view====================#
def home(request):
    try:
        posts = BlogPost.objects.all()
        # Only add the user's first and last name if the user is logged in
        user_first_name = request.user.first_name if request.user.is_authenticated else None
        user_last_name = request.user.last_name if request.user.is_authenticated else None
        return render(request, 'blog/home.html', {
            'posts': posts,
            'user_first_name': user_first_name,
            'user_last_name': user_last_name
        })
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc() # To find the exact line of error
        print('Exception in home:', e) # For debugging
        print('Traceback:', traceback_str) # For debugging
        return render(request, 'blog/home.html')

#====================Create new blog post====================#
@login_required
def create_post(request):
    try:
        if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']
            BlogPost.objects.create(title=title, content=content, author=request.user)
            messages.success(request, "Post created successfully!")
            return redirect('blog-home')
        return render(request, 'blog/create_post.html')
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in create_post:', e)
        print('Traceback:', traceback_str)
        return redirect('blog-home')

#====================HUpdate the blog post====================#
@login_required
def update_post(request, post_id):
    try:
        post = get_object_or_404(BlogPost, id=post_id)
        if post.author != request.user:
            messages.error(request, "You are not authorized to update this post.")
            return redirect('blog-home')
        
        if request.method == "POST":
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.save()
            messages.success(request, "Post updated successfully!")
            return redirect('blog-home')
        return render(request, 'blog/edit_post.html', {'post': post})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in update_post:', e)
        print('Traceback:', traceback_str)
        return redirect('blog-home')

#====================Delete the blog post====================#
@login_required
def delete_post(request, post_id):
    try:
        post = get_object_or_404(BlogPost, id=post_id)
        if post.author != request.user:
            messages.error(request, "You are not authorized to delete this post.")
            return redirect('blog-home')
        
        if request.method == "POST":
            post.delete()
            messages.success(request, "Post deleted successfully!")
            return redirect('blog-home')
        return render(request, 'blog/delete_post.html', {'post': post})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in delete_post:', e)
        print('Traceback:', traceback_str)
        return redirect('blog-home')

#====================View user specific posts====================#    
@login_required
def my_posts(request):
    try:
        posts = BlogPost.objects.filter(author=request.user)
        return render(request, 'blog/my_posts.html', {'posts': posts})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please contact support.')
        traceback_str = traceback.format_exc()
        print('Exception in my_posts:', e)
        print('Traceback:', traceback_str)
        return redirect('blog-home')

