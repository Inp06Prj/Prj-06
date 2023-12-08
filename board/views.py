from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Board
from django.contrib.auth.decorators import login_required


# # 황민지
# def index(request):
#     all_boards = Board.objects.all().order_by('-pk') # 모든 데이터 조회, 내림차순(-표시) 조회
#     paginator = Paginator(all_boards, 7)
#     page = int(request.GET.get('page', 1))
#     board_list = paginator.get_page(page)
#     return render(request, 'board/index.html', {'title':'Board List', 'board_list':board_list})


# 황민지
def detail(request, board_id):
    board = Board.objects.get(id=board_id)
    return render(request, 'board/detail.html', {'board': board})


# 황민지
def write(request):
    return render(request, 'board/write.html')
# write: 게시글 목록에서 "글쓰기" 버튼 클릭 시 쓰기 페이지 이동


# 황민지
def write_board(request):
    # 로그인되어 있는지 확인
    if request.user.is_authenticated:
        b = Board(title=request.POST['title'], content=request.POST['detail'], author=request.user,
                  create_date=timezone.now())
        b.save()
        return HttpResponseRedirect(reverse('board:index'))
    else:
        # 로그인되어 있지 않은 경우, 로그인 페이지로 리다이렉트 또는 다른 처리 수행
        messages.success(request, '글을 작성하기 위해서는 로그인을 해야합니다.')
        return HttpResponseRedirect(reverse('custom_login'))  # 또는 로그인 페이지로 리다이렉트하거나 다른 처리를 수행하세요.


# 황민지
@login_required(login_url='/login')
def create_reply(request, board_id):
    board = Board.objects.get(id=board_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')

        if comment:
            # 현재 로그인한 사용자를 댓글의 작성자로 설정
            author = request.user
            board.reply_set.create(comment=comment, author=author, rep_date=timezone.now())

            return HttpResponseRedirect(reverse('board:detail', args=(board_id,)))

    return HttpResponseRedirect(reverse('board:detail', args=(board_id,)))


# 황민지
@login_required(login_url='/login')
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if request.user == board.author:
        board.delete()
        # messages.success(request, '글이 삭제되었습니다.')
        return HttpResponse(status=204)  # HTTP 204 No Content
    else:
        messages.error(request, '글을 삭제할 권한이 없습니다.')

    return redirect('board:index')


# 황민지
@login_required(login_url='/login')
def edit_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if request.user == board.author:
        if request.method == 'POST':
            board.title = request.POST.get('title')
            board.content = request.POST.get('detail')
            board.save()
            return HttpResponseRedirect(reverse('board:detail', args=(board_id,)))
        else:
            return render(request, 'board/edit.html', {'board': board})
    else:
        messages.error(request, '글을 수정할 권한이 없습니다.')
        return redirect('board:index')


from django.db.models import Q


# 황민지
def index(request):
    # 검색 기능!
    search_query = request.GET.get('q', '')

    if search_query:
        # If there is a search query, filter the boards based on title and content
        all_boards = Board.objects.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)).order_by('-pk')
    else:
        # If there is no search query, retrieve all boards as before
        all_boards = Board.objects.all().order_by('-pk')

    paginator = Paginator(all_boards, 7)
    page = int(request.GET.get('page', 1))
    board_list = paginator.get_page(page)

    return render(request, 'board/index.html',
                  {'title': 'Board List', 'board_list': board_list, 'search_query': search_query})
