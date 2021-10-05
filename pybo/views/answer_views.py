from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from django.utils import timezone

from ..models import Question, Answer
from ..forms import AnswerForm

@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    pybo 답변 등록
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user    # author 속성에 로그인 계정 저장
            created_time = timezone.now()
            answer.created = created_time
            answer.last_upd = created_time
            answer.question = question
            answer.save()
            # return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
            return redirect(f'{resolve_url("pybo:detail", question_id=question.id)}#answer_{answer.id}')
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    '''
    pybo 답변 수정
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        # messages.error(request, f'requset.user: {str(request.user)}')
        # messages.error(request, f'answer.author: {str(answer.author)}')
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.last_upd = timezone.now()
            answer.save()
            # return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
            return redirect(f'{resolve_url("pybo:detail", question_id=answer.question.id)}#answer_{answer.id}')
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    '''
    pybo 답변 삭제
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)    