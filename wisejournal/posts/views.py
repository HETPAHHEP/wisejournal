from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post
from .forms import PostForm


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
    posts_list = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'group.html',
        {'page': page, 'paginator': paginator, 'group': group}
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'new_post.html', {'form': form, 'errors': form.errors})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('/')
