from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Blog, Comment, Tag, Liker
from .forms import BlogForm
from users.views import *


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    # TODO: Comment 추가
    comments = Comment.objects.filter(blog=blog)

    # TODO: Tag 추가
    tags = blog.tag.all()
    return render(request, 'detail.html', {'blog': blog, 'comments': comments, 'tags': tags})


def new(request):
    # TODO: Tag 추가
    tags = Tag.objects.all()
    return render(request, 'new.html', {'tags': tags})


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user
    # TODO: author 추가

    new_blog.save()

    # TODO: tags 추가
    tags = request.POST.getlist('tags')

    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag)
    return redirect('detail', new_blog.id)


def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id)

    # TODO: 본인이 쓴 글이 아니면 home으로 redirect
    if request.user != edit_blog.author:
        return redirect('home')

    return render(request, 'edit.html', {'edit_blog': edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)

# def update(request, blog_id):
#     old_blog = get_object_or_404(Blog, pk=blog_id)
#     form = BlogForm(request.POST, instance=old_blog)

    # 클라이언트가 유효한 값을 입력한 경우
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.save()
        return redirect('detail', old_blog.id)

    return render(request, 'new.html', {'old_blog': old_blog})


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    delete_blog.delete()
    return redirect('home')

# TODO: new_comment, create_comment 추가


def create_comment(request, blog_id):
    comment = Comment()
    comment.content = request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user
    comment.save()

    return redirect('detail', blog_id)


def new_comment(request, blog_id):
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, pk=blog_id)
        return render(request, 'new_comment.html', {'blog': blog})
    return redirect('login')


def prefer(request, blog_id):
    if request.user.is_authenticated:
        # 로그인이 되어있다면
        blog = get_object_or_404(Blog, pk=blog_id)
        # 현재 블로그 정보 받아오가
        liker_list = None
        # liker_list는 none으로 초기화
        if blog.liker:
            # blog.liker에 연결된 값이 있다면 (없는데 가져오려고 하면 error)
            liker_list = blog.liker.likerList.filter(pk=request.user.pk)
            # filter로 현재 사용자가 likerList에 들어있는지 확인
        if not liker_list:
            # 만약 lier_list에 값이 없다면 ( blog.liker에 현재 사용자 정보가 없다면 )
            if not blog.liker:
                # 만약 연결된 정보가 없는 것이라면 새로 할당
                blog.liker = Liker.objects.create()
            blog.liker.likerList.add(request.user)
            # likerList에 현재 사용자 정보 저장
            blog.liker.likeTimes += 1
            # likeTimes(좋아요 횟수)에 1 더하기
            blog.liker.save()
            # Liker 모델 업데이트
            blog.save()
            # Blog 모델 업데이트
        return redirect("detail", blog_id)
    return redirect("login")
