import datetime

from django.shortcuts import render
from main.models import Voting
from .forms import *


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'voting', 'name': 'Голосование'},
        {'url_name': 'votings', 'name': 'Голосования'},
    ]


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()

    }
    return render(request, 'pages/index.html', context)


def time_page(request):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context()
    }
    return render(request, 'pages/time.html', context)


def voting_page(request):
    required_id = 2  # тут что нибудь умное придумаем
    context = {
        'voting': Voting.objects.filter(id=required_id),
    }
    return render(request, 'pages/voting.html', context)


def voting_list_page(request):
    # author, name, description
    context = {
        'history': Voting.objects.all()
    }
    return render(request, 'pages/voting_list.html', context)


def voting_creation_page(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = Addform(request.POST)
        if form.is_valid():
            context['status'] = 1
            adder = Voting(author=1, name=form.verh, author_name=user.USERNAME_FIELD, description=form.content, type=1,
                           published=datetime.now(), finished=datetime.now(), is_active=1)
            adder.save()
        else:
            context['status'] = 0

    return render(request, 'pages/add_votings.html', context)
