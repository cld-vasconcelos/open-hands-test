from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Contest, User, Picture, ContestSubmission
from django.utils import timezone

class WinnersViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass', name_first='Test', name_last='User')
        self.picture = Picture.objects.create(user=self.user, name='Test Picture')
        self.contest = Contest.objects.create(title='Test Contest', description='Test Description', voting_phase_end=timezone.now(), internal_status='CLOSED')
        self.contest.winners.add(self.user)
        self.submission = ContestSubmission.objects.create(contest=self.contest, picture=self.picture)

    def test_winners_view(self):
        response = self.client.get(reverse('winners'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['contest_title'], 'Test Contest')
        self.assertEqual(response.data[0]['winner_name'], 'Test User')
