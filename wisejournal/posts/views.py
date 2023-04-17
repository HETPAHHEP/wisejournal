from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post, User, Comment
from .forms import PostForm, CommentForm


def index(request):
    """Главная страница"""
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    """Страница сообщества"""
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group).all()
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'group.html',
        {'page': page, 'paginator': paginator, 'group': group}
    )


def profile(request, username):
    """Страница профиля со всеми постами"""
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'profile.html',
        {'page': page, 'paginator': paginator, 'author': author, 'user': request.user}
    )


def post_view(request, username, post_id):
    """Страница конкретного поста"""
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=author)
    comments = post.comments.all()
    post_count = Post.objects.filter(author=author).count()
    form = CommentForm()

    return render(
        request,
        'post.html',
        {
            'post': post,
            'author': author,
            'user': request.user,
            'post_count': post_count,
            'items': comments,
            'form': form
        }
    )


@login_required
def new_post(request):
    """Добавить новый пост"""
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(
            request,
            'new_post.html',
            {
                'form': form,
                'errors': form.errors
            }
        )

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')


@login_required
def post_edit(request, username, post_id):
    """Редактировать нужный пост"""
    profile_user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)

    if profile_user == request.user:
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if not form.is_valid():
            edit_mode = True
            return render(
                request,
                'new_post.html',
                {
                    'form': form,
                    'errors': form.errors,
                    'edit_mode': edit_mode,
                    'username': username,
                    'post_id': post_id
                }
            )

        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
    return redirect("post", username=request.user.username, post_id=post_id)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/505.html', status=500)


@login_required
def add_comment(request, username, post_id):
    profile_commentator = get_object_or_404(User, username=request.user)
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None, instance=None)

    if not form.is_valid():
        return render(
            request,
            'post.html',
            {
                'form': form,
                'post': post,
                'author': post.author,
                'errors': form.errors
            }
        )

    comment = form.save(commit=False)
    comment.author = profile_commentator
    comment.post = post
    comment.save()

    return redirect("post", username=username, post_id=post_id)
