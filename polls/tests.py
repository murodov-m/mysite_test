from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
import datetime


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>No polls are available</p>')
        print("############", response.context)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text='Past question', days=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_future_question(self):
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, '<p>No polls are available</p>')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text='Past question', days=-3)
        create_question(question_text='Future question', days=3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_two_past_questions(self):
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text='Past question 2', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 1>', '<Question: Past question 2>']
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('polls:detail', args=[future_question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question', days=-1)
        url = reverse('polls:detail', args=[past_question.id])
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
