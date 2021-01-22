from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView

from main.models import Voting, VoteVariant, VoteFact, Complaint, User


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

    if request.method == "POST":
        vote_var = request.POST.getlist('vote_var', None)  # берётся массив ответов
        if vote_var is not None:  # массив ответов записывается в БД
            for var in vote_var:
                variant = get_object_or_404(VoteVariant, id=var)
                time = timezone.now()
                vote_fact = VoteFact(author=curr_user, variant=variant, created=time)
                vote_fact.save()
        return HttpResponseRedirect('/votings')
    elif request.method == "GET":
        context = {
            'vote_variants': vote_variants,
            'curr_user': curr_user,
            'voting': voting,
        }
        return render(request, 'pages/voting.html', context)


def complaint_page(request, pk):
    voting = get_object_or_404(Voting, id=pk)
    curr_user = request.user
    reason = request.POST.get('text', None)
    context = {}
    context['voting_text'] = voting.description
    user = request.user
    if request.method == 'POST':
        context['status'] = 1
        adder = Complaint(author_id=user.id, description=reason,status=0,voting_id=pk)
        adder.save()

    return render(request, 'pages/voting_complaint.html', context)


@login_required
def voting_list_page(request):
    context = {
        'history': Voting.objects.all()
    }
    return render(request, 'pages/voting_list.html', context)


@login_required
def complaint_list_page(request):
    context = {
        'history': Complaint.objects.filter(author_id=request.user.id)
    }
    return render(request, 'pages/complaint_list.html', context)


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
        return HttpResponseRedirect("/votings")
    return render(request, 'pages/creating.html', context)


def profile_page(request):
    return render(request, 'pages/profile.html')


def profile_editing_page(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.pk)
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return HttpResponseRedirect("/profile")
    elif request.method == 'GET':
        return render(request, 'pages/profile_editing.html')
