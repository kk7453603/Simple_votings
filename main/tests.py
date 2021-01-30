from django.test import TestCase
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView
from main.models import Voting, VoteVariant, VoteFact, Complaint, User
from datetime import datetime
import json


class VotingUpdateView(DetailView):
    model = Voting
    template_name = 'pages/voting.html'
    context_object_name = 'voting_update'


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'votings', 'name': 'Голосования'},
        {'url_name': 'complaint_list', 'name': 'Список жалоб'},
    ]


def test_page(request):
    context = {
        'history': Voting.objects.all()
    }
    return render(request, 'pages/voting.html', context)
