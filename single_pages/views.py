from django.shortcuts import render


# 황민지
def landing(request):
    return render(
        request,
        'single_pages/landing.html',
    )

