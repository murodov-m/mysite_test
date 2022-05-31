from django.http import HttpResponse, Http404
from .models import Question
from django.shortcuts import render, get_object_or_404


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print(latest_question_list)
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # try:
    #     q = Question.objects.get(pk=question_id)
    # except:
    #     raise Http404(
    #         "Не смог найти данный вопрос."
    #     )
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = 'Results page'
    pass


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def test(request):
    return HttpResponse('TEST WORKS!')
