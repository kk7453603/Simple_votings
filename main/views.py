import datetime

from django.shortcuts import render

from main.models import Voting


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
    required_id = 2   # тут что нибудь умное придумаем
    context = {
        'voting' : Voting.objects.filter(id=required_id),
    }
    return render(request, 'pages/voting.html', context)


def voting_list_page(request):
    # author, name, description
    context = {
        'history' : Voting.objects.all()
    }
    return render(request, 'pages/voting_list.html', context)
