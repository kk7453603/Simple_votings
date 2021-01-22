from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from hashlib import sha256
from main.models import Voting, VoteVariant, VoteFact, User


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
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


def new_password(request):
    password1 = request.POST.get('password1', None)
    # password2 = request.POST.get('password2', None)
    context = {}
    if request.method == 'POST':
        adder = User.objects.get(username=request.user.username)

        adder.password = sha256(str(password1).encode('utf-8')).hexdigest()
        adder.save()

        return redirect('/')

    return render(request, 'registration/new_password.html', context)
