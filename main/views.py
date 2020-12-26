import datetime

from django.shortcuts import render

from main.models import Voting, User, VoteVariant, VoteFact


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'time', 'name': 'Текущее время'},
        {'url_name': 'voting', 'name': 'Голосование'},
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
    #для начала работы надо иметь одного юзера(id=1), затем
    #хотя бы одно голосование Voting(id=1) и у этого голосования добавить в VoteVariant несколько вариантов ответа
    #в таблицу VoteFact сохраняются все голосования
    vote_var = request.GET.get('vote_var', None)
    voting = Voting.objects.get(id=1)
    vote_variants = VoteVariant.objects.filter(voting=voting.id)
    curr_user = User.objects.get(id=1)

    if vote_var != None:
        vote_fact = VoteFact(author=curr_user.id,variant=vote_var,created=datetime.datetime.now())
        vote_fact.save()

    context = {
        'name': voting.name,
        'description': voting.description,
        'author_name': curr_user.username,
        'author': voting.author,
        'vote_variants': vote_variants
    }
    return render(request, 'pages/voting.html', context)
