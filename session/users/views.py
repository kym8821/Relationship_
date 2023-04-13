from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib import auth
# TODO: 회원가입


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            # password1과 확인 패스워드가 같다면
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )

            profile = Profile(
                user=user,
                nickname=request.POST['nickname'],
                image=request.FILES.get('profile_image'),
                # get을 쓰는 이유는 파일이 없을 때 에러 안뜨게하려고 쓰는 것
            )

            profile.save()

            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

    # TODO: 로그인


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # 데이터베이스에 등록되어있다면 authenticate를 통해 user에 반환
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        return render(request, 'login.html')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
    # TODO: 로그아웃
