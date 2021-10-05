from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question

import logging
logger = logging.getLogger('pybo')

def index(request):
    '''
    pybo 목록 출력
    '''
    # 입력 파라미터
    page = request.GET.get('page', '1')         # 페이지
    kw = request.GET.get('kw', '')              # 검색어
    so = request.GET.get('so', 'recent')              # 검색어

    logger.info(f'페이지: { page } 키워드: { kw } 정렬: { so }')
    # 조회
    if so == 'recommend':
        question_list = Question.objects.defer('content').annotate(num_voter=Count('voter')).order_by('-num_voter', '-last_upd')
    elif so == 'popular':
        question_list = Question.objects.defer('content').annotate(num_answer=Count('answer')).order_by('-num_answer', '-last_upd')
    else:
        question_list = Question.objects.order_by('-last_upd')
    
    # to do: distinct clob 컬럼 해결
    if kw: 
        question_list = question_list.defer('content').filter(
            Q(subject__icontains=kw)
            | Q(content__icontains=kw)
            | Q(author__username__icontains=kw)
            | Q(answer__author__username__icontains=kw)
        ).distinct()
    
    # logger.info(str(question_list.query))

    # 페이징
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    '''
    pybo 질문 내용 출력
    '''
    # logger.info(f'page = {page}')
    question = get_object_or_404(Question, pk=question_id)
    # context = {'question': question, 'page': page}
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)