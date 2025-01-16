from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import CommentReplyForm
import logging
logger = logging.getLogger(__name__)


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('home')
    return render(request, 'posts/create_post.html')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    top_level_comments = post.comments.filter(parent=None)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'top_level_comments': top_level_comments
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'likes_count': post.likes.count()})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()  # Get the content from the form
        if content:  # Check if content is not empty
            comment = Comment.objects.create(
                user=request.user,  # Associate the comment with the logged-in user
                post=post,  # Associate the comment with the post
                content=content  # Set the comment content
            )
            return redirect('post_detail', post_id=post.id)  # Redirect back to the post detail page

    # If no POST request, redirect to the post detail page
    return redirect('post_detail', post_id=post.id)

@login_required
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post  # Get the post associated with the comment
    
    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent = parent_comment  # Set the parent comment
            reply.user = request.user  # Associate with the current logged-in user
            reply.post = post  # Associate with the same post
            reply.save()
            return redirect('post_detail', post_id=post.id)  # Redirect to the post detail page
    else:
        form = CommentReplyForm()
    
    return render(request, 'comments/reply_to_comment.html', {'form': form, 'parent_comment': parent_comment})
