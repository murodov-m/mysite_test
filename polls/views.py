from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
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
    return HttpResponse('You\'re looking at the results page')


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.all().get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did\'nt select a choice.',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Black button
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def test(request):
    return HttpResponse('TEST WORKS!')
