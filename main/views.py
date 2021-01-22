from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView

from main.models import Voting, VoteVariant, VoteFact


class VotingUpdateView(DetailView):
    model = Voting
    template_name = 'pages/voting.html'
    context_object_name = 'voting_update'


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
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


def voting_page(request, pk):
    voting = get_object_or_404(Voting, id=pk)  # это id голосования
    vote_variants = voting.votevariant_set.all()
    curr_user = request.user

    vote_var = request.POST.getlist('vote_var', None)  # берётся массив ответов
    if vote_var is not None:  # массив ответов записывается в БД
        for var in vote_var:
            variant = get_object_or_404(VoteVariant, id=var)
            time = timezone.now()
            vote_fact = VoteFact(author=curr_user, variant=variant, created=time)
            vote_fact.save()

    context = {
        'vote_variants': vote_variants,
        'curr_user': curr_user,
        'voting': voting,
    }
    return render(request, 'pages/voting.html', context)


@login_required
def voting_list_page(request):
    context = {
        'history': Voting.objects.all()
    }
    return render(request, 'pages/voting_list.html', context)


def voting_creation_page(request):
    context = {}
    if request.method == "POST":
        vote_name = request.POST.get('voting_name', None)
        vote_description = request.POST.get('voting_description', None)
        vote_type = request.POST.get('voting_type', None)
        curr_user = request.user
        vote_variants = request.POST.getlist('vote_var', None)
        voting = Voting(author=curr_user, name=vote_name, description=vote_description, type=vote_type, published=timezone.now(), finished=timezone.now(), is_active=1)
        voting.save()
        voting_id = voting.pk
        for i in vote_variants:
            vote_var = VoteVariant(description=i, voting_id=voting_id)
            vote_var.save()
    return render(request, 'pages/creating.html', context)
