from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


@cache_page(20, key_prefix='index_page')
def index(request):
    """Главная страница"""
    post_list = Post.objects.all()
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

    following = False
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=author).exists()

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'profile.html',
        {'page': page, 'paginator': paginator, 'author': author, 'user': request.user, 'following': following}
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
    """Вывод страницы с ошибкой 404"""
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    """Вывод страницы с ошибкой 500"""
    return render(request, 'misc/505.html', status=500)


@login_required
def add_comment(request, username, post_id):
    """Обработка формы отправки комментария"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None, instance=None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect("post", username=username, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)

    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'follow.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def profile_follow(request, username):
    follow_author = get_object_or_404(User, username=username)

    if follow_author != request.user and (
        not request.user.follower.filter(author=follow_author)
    ):
        Follow.objects.create(user=request.user, author=follow_author)

    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    follow_author = get_object_or_404(User, username=username)

    date_follow = request.user.follower.filter(author=follow_author)

    if date_follow:
        date_follow.delete()

    return redirect('profile', username=username)