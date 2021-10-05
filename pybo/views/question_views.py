from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from ..models import Question
from ..forms import QuestionForm

@login_required(login_url='common:login')
def question_create(request):
    '''
    pybo 질문 등록
    '''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user    # author 속성에 로그인 계정 저장
            created_time = timezone.now()
            question.created = created_time
            question.last_upd = created_time
            
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''
    pybo 질문 수정
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        # messages.error(request, f'requset.user: {str(request.user)}')
        # messages.error(request, f'question.author: {str(question.author)}')
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.last_upd = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    '''
    pybo 질문 삭제
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    question.delete()
    return redirect('pybo:index')