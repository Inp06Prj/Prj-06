from django.shortcuts import render


# Create your views here.

def landing(request):
    return render(
        request,
        'single_pages/landing.html',
    )


# def stu_login(request):
#     return render(
#         request,
#         'single_pages/stu_login.html',
#     )


# def main(request):
#     return render(
#         request,
#         'single_pages/main.html',
#     )
