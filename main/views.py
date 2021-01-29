from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView

from main.models import Voting, VoteVariant, VoteFact, Complaint, User, VoteImages

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


def index_page(request):
    items = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }

    context = {"json": json.dumps(items)}

    return render(request, 'pages/index.html', context)


@login_required
def voting_page(request, pk):
    voting = get_object_or_404(Voting, id=pk)  # это id голосования
    vote_variants = voting.votevariant_set.all()
    curr_user = request.user
    images = VoteImages.objects.filter(voting=voting)
    if timezone.now() > voting.finished:
        voting.is_active = 0
        voting.save()
    if VoteFact.objects.filter(voting=voting, author=curr_user):
        votefact = True
    else:
        votefact = False
    if request.method == "POST":
        if not votefact:
            if voting.is_active:
                vote_var = request.POST.getlist('vote_var', None)  # берётся массив ответов
                if vote_var is not None:  # массив ответов записывается в БД
                    for var in vote_var:
                        variant = get_object_or_404(VoteVariant, id=var)
                        time = timezone.now()
                        vote_fact = VoteFact(voting=voting, author=curr_user, variant=variant, created=time)
                        vote_fact.save()
        return HttpResponseRedirect('/votings')
    elif request.method == "GET":
        context = {
            'vote_variants': vote_variants,
            'curr_user': curr_user,
            'voting': voting,
            'votefact': votefact,
            'images': images,
            'menu': get_menu_context(),
        }
        return render(request, 'pages/voting.html', context)


@login_required
def complaint_page(request, pk):
    voting = get_object_or_404(Voting, id=pk)
    curr_user = request.user
    reason = request.POST.get('text', None)
    context = {
        'voting_text': voting.description,
        'menu': get_menu_context(),
    }
    user = request.user
    if request.method == 'POST':
        context['status'] = 1
        adder = Complaint(author_id=user.id, description=reason, status=0, voting_id=pk)
        adder.save()

    return render(request, 'pages/voting_complaint.html', context)


@login_required
def voting_list_page(request):
    context = {
        'history': Voting.objects.all(),
        'menu': get_menu_context(),
    }
    return render(request, 'pages/voting_list.html', context)


@login_required
def complaint_list_page(request):
    context = {
        'history': Complaint.objects.filter(author_id=request.user.id),
        'menu': get_menu_context(),
    }
    return render(request, 'pages/complaint_list.html', context)


@login_required
def voting_creation_page(request):
    context = {
        'menu': get_menu_context(),
    }
    if request.method == "POST":
        vote_name = request.POST.get('voting_name', None)
        vote_description = request.POST.get('voting_description', None)
        vote_type = request.POST.get('voting_type', None)
        curr_user = request.user
        vote_variants = request.POST.getlist('vote_var', None)
        date_finish = request.POST.get('finish_date', timezone.now())
        images = request.POST.getlist('images_url', None)

        voting = Voting(author=curr_user, name=vote_name, description=vote_description, type=vote_type, published=timezone.now(), finished=date_finish, is_active=1)
        voting.save()
        voting_id = voting.pk
        for i in vote_variants:
            vote_var = VoteVariant(description=i, voting_id=voting_id)
            vote_var.save()
        for i in images:
            image = VoteImages(voting_id=voting_id, image_url=i)
            image.save()
        return HttpResponseRedirect("/votings")
    return render(request, 'pages/creating.html', context)


@login_required
def voting_editing_page(request, pk):
    context = {
        'menu': get_menu_context(),
    }
    curr_user = request.user
    voting = get_object_or_404(Voting, id=pk)
    if curr_user == voting.author:
        vote_vars = VoteVariant.objects.filter(voting_id=pk)
        if request.method == "POST":
            vote_name = request.POST.get('voting_name', None)
            vote_vars_edited = request.POST.getlist('vote_var', None)
            vote_description = request.POST.get('voting_description', None)
            voting.name = vote_name
            voting.description = vote_description
            voting.save()
            for i, j in zip(vote_vars, vote_vars_edited):
                i.description = j
                i.save()
            return HttpResponseRedirect(f'/voting/{pk}')

        context = {
            'voting': voting,
            'vote_vars': vote_vars,
            'menu': get_menu_context(),
        }
    else:
        return HttpResponseRedirect("/votings/")
    return render(request, 'pages/editing.html', context)


@login_required
def voting_results(request, pk):
    curr_user = request.user
    voting = get_object_or_404(Voting, id=pk)
    votevariants = VoteVariant.objects.filter(voting=voting)
    statistic = {}
    if VoteFact.objects.filter(voting=voting, author=curr_user):
        votefact = True
    else:
        votefact = False

    for i in votevariants:
        statistic[i.description] = VoteFact.objects.filter(voting=voting, variant=i).count() #votefacts.objects.filter(variant=i)

    context = {
        'votefact': votefact,
        'statistic': statistic,
        'voting': voting,
        'menu': get_menu_context(),
    }
    return render(request, 'pages/voting_results.html', context)


@login_required
def profile_page(request):
    context = {
        'menu': get_menu_context(),
    }
    return render(request, 'pages/profile.html', context)


@login_required
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
        context = {
            'menu': get_menu_context(),
        }
        return render(request, 'pages/profile_editing.html', context)


@login_required
def password_editing_page(request):
    if request.method == 'POST':
        context = {
            'is_old_password_wrong': True,
            'is_new_password_wrong': True,
            'is_repeat_password_wrong': True,
        }
        user = User.objects.get(id=request.user.pk)
        password = request.POST.get('old_password')
        if user.check_password(password):
            new_password = request.POST.get('new_password')
            repeat_new_password = request.POST.get('repeat_new_password')
            context['is_old_password_wrong'] = False
            if new_password == repeat_new_password:
                context['is_repeat_password_wrong'] = False
                if len(new_password) > 7 and len(repeat_new_password) > 7:
                    context['is_new_password_wrong'] = False
                    user.set_password(new_password)
                    user.save()
                    return HttpResponseRedirect("/")
        return render(request, 'pages/password_editing.html', context)
    elif request.method == 'GET':
        context = {
            'menu': get_menu_context(),
        }
        return render(request, 'pages/password_editing.html', context)
