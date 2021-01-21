import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from main.models import Voting, VoteVariant, VoteFact

from main.models import Voting


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'voting', 'name': 'Голосование'},
        {'url_name': 'votings', 'name': 'Голосования'},
        {'url_name': 'create', 'name': 'Создания голосования'},
    ]


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()

    }
    return render(request, 'pages/index.html', context)


def voting_page(request):
    vote_var = request.GET.get('vote_var', None)
    voting = get_object_or_404(Voting, id=1)
    vote_variants = voting.votevariant_set.all()
    curr_user = request.user

    if vote_var is not None:
        vote_var = get_object_or_404(VoteVariant, id=vote_var)
        vote_fact = VoteFact(author=curr_user, variant=vote_var, created=timezone.now())
        vote_fact.save()

    context = {
        'name': voting.name,
        'description': voting.description,
        'author_name': curr_user.username,
        'author': voting.author,
        'vote_variants': vote_variants
    }
    return render(request, 'pages/voting.html', context)


def voting_list_page(request):
    context = {
        'history': Voting.objects.all()
    }
    return render(request, 'pages/voting_list.html', context)


def voting_creation_page(request):
    header = request.POST.get('header', None)
    text = request.POST.get('text', None)
    context = {}
    user = request.user
    if request.method == 'POST':
        # form = Addform(request.POST)
        # if form.is_valid():
        context['status'] = 1
        adder = Voting(author=request.user, name=header, description=text, type=1,
                       published=datetime.datetime.now(), finished=datetime.datetime.now(), is_active=1)
        adder.save()
        redirect('')
        # else:
        # context['status'] = 1

    return render(request, 'pages/add_votings.html', context)
