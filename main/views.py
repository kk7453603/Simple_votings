from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView

from main.models import Voting, VoteVariant, VoteFact, Complaint, User, VoteImages, Comments
from main.forms import ProfileEditingForm, VotingForm, PasswordEditingForm, ComplaintForm

import json


class VotingUpdateView(DetailView):
    model = Voting
    template_name = 'pages/voting.html'
    context_object_name = 'voting_update'


def get_menu_context():
    return [
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
    comments = Comments.objects.filter(voting=voting)
    if timezone.now() > voting.finished:
        voting.is_active = 0
        voting.save()
    if VoteFact.objects.filter(voting=voting, author=curr_user):
        votefact = True
    else:
        votefact = False
    if request.method == "POST":
        parameter = request.POST.get('parameter', None)
        if parameter == 'voting':
            if not votefact:
                if voting.is_active:
                    vote_var = request.POST.getlist('vote_var', None)  # берётся массив ответов
                    if vote_var is not None:  # массив ответов записывается в БД
                        for var in vote_var:
                            variant = get_object_or_404(VoteVariant, id=var)
                            time = timezone.now()
                            vote_fact = VoteFact(voting=voting, author=curr_user, variant=variant, created=time)
                            vote_fact.save()
        elif parameter == 'comment':
            comment = request.POST.get('comment', None)
            if comment:
                data = Comments(author=request.user, voting_id=pk, content=comment)
                data.save()
        return HttpResponseRedirect(f'/voting/{pk}')
    elif request.method == "GET":
        context = {
            'vote_variants': vote_variants,
            'curr_user': curr_user,
            'voting': voting,
            'votefact': votefact,
            'images': images,
            'menu': get_menu_context(),
            'comments': comments
        }
        return render(request, 'pages/voting.html', context)


@login_required
def complaint_page(request, pk):
    voting = get_object_or_404(Voting, id=pk)
    context = {
        'voting_text': voting.description,
        'menu': get_menu_context(),
    }
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            reason = form.data['text']
            adder = Complaint(author_id=request.user.id, description=reason, status=0, voting_id=pk)
            adder.save()
            return HttpResponseRedirect('/complaint_list/')
        else:
            return HttpResponseRedirect(f'/voting/{pk}/complaint/')
    elif request.method == 'GET':
        form = ComplaintForm()
        context['form'] = form
        return render(request, 'pages/voting_complaint.html', context)


@login_required
def voting_list_page(request):
    votefact = False
    votings = []
    votings_info=[]
    for i in VoteFact.objects.filter(author=request.user):
        votings.append(Voting.objects.get(id=i.voting_id))
    for i in Voting.objects.all():
        if not i in votings:
            votings_info.append(i)
    context = {
        'votefact': votefact,
        'history': votings_info,
        'menu': get_menu_context(),
    }
    return render(request, 'pages/voting_list.html', context)


@login_required
def voting_history_page(request):
    vote_vars = []
    voting_names = []
    voting_des = []
    voting_id = []
    context = {
        'history': VoteFact.objects.filter(author_id=request.user.id)
    }
    for obj in context['history']:
        vote_vars.append(VoteVariant.objects.get(id=obj.variant_id).description)
        voting_names.append(Voting.objects.get(id=obj.voting_id).name)
        voting_des.append(Voting.objects.get(id=obj.voting_id).description)
        voting_id.append(Voting.objects.get(id=obj.voting_id).id)
    vote_info = []
    for obj in range(len(voting_names)):
        vote_info.append([voting_names[obj], voting_des[obj], vote_vars[obj], voting_id[obj]] )

    context = {
        'vote_info': vote_info,
        'menu': get_menu_context()
    }

    return render(request, 'pages/voting_history.html', context)


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
        return HttpResponseRedirect("/votings/")
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
        statistic[i.description] = VoteFact.objects.filter(voting=voting, variant=i).count()  # votefacts.objects.filter(variant=i)

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
        form = ProfileEditingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.pk)
            user.username = form.data['username']
            user.first_name = form.data['first_name']
            user.last_name = form.data['last_name']
            user.email = form.data['email']
            user.save()
            return HttpResponseRedirect("/profile/")
        else:
            return HttpResponseRedirect("/profile/editing/")
    elif request.method == 'GET':
        user = User.objects.get(id=request.user.pk)
        form = ProfileEditingForm(
            initial={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        )
        context = {
            'form': form,
            'menu': get_menu_context(),
        }
        return render(request, 'pages/profile_editing.html', context)


@login_required
def password_editing_page(request):
    if request.method == 'POST':
        form = PasswordEditingForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'is_old_password_wrong': True,
                'is_new_password_wrong': True,
                'is_repeat_password_wrong': True,
            }
            user = User.objects.get(id=request.user.pk)
            password = form.data['old_password']
            if user.check_password(password):
                new_password = form.data['new_password']
                repeat_new_password = form.data['repeat_new_password']
                context['is_old_password_wrong'] = False
                if new_password == repeat_new_password:
                    context['is_repeat_password_wrong'] = False
                    if len(new_password) > 7 and len(repeat_new_password) > 7:
                        context['is_new_password_wrong'] = False
                        user.set_password(new_password)
                        user.save()
                        return HttpResponseRedirect("/")
            return render(request, 'pages/password_editing.html', context)
        else:
            return HttpResponseRedirect("/profile/editing/change_password/")
    elif request.method == 'GET':
        form = PasswordEditingForm()
        context = {
            'form': form,
            'menu': get_menu_context(),
        }
        return render(request, 'pages/password_editing.html', context)
