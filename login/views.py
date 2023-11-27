from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile

from django.contrib.auth.models import Group


def custom_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = form.get_user()

            if user is not None:
                # Check group membership
                student_group = Group.objects.get(name='Student')
                if user.groups.filter(name='Student').exists():
                    login(request, user)
                    return redirect(reverse(main_view))
                else:
                    messages.error(request, '로그인 실패: 폼이 유효하지 않음')
            # else:
            #     messages.error(request, '로그인 실패: 사용자 인증 실패')
        else:
            messages.error(request, '로그인 실패: 폼이 유효하지 않음')
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})



def custom_logout(request):
    logout(request)
    messages.success(request, '(학생) 로그아웃 되었습니다.')
    return redirect(reverse('custom_login'))  # 여기서 'main'은 당신이 메인 페이지 URL 패턴에 지정한 이름입니다.


def main_view(request):
    stu_users = UserProfile.objects.order_by('-pk')
    context = {'stu_users': stu_users}
    # return render(request, 'login/main.html', context)

    if request.user.is_authenticated:
        # 인증된 사용자에게 메인 페이지를 렌더링합니다.
        context['user'] = request.user  # 사용자 정보를 context에 추가
        return render(request, 'login/main.html', context)
    else:
        # 미인증 사용자에게 로그인 페이지로 리디렉션합니다.
        return redirect(reverse('custom_login'))


from .models import UserProfile


@login_required(login_url='custom_login')
def mypage(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    context = {'user_profile': user_profile}
    return render(request, 'login/mypage.html', context)