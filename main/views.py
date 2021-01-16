from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView

from main.models import Voting, VoteVariant, VoteFact


class VotingUpdateView(DetailView):
    model = Voting
    template_name = 'pages/voting.html'
    context_object_name = 'voting_update'


# class VotingUpdateView(DetailView):
#     model = Voting
#     template_name = 'pages/voting.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(VotingUpdateView, self).get_context_data(**kwargs)
#
#         context = {
#             'vote_variants': self.vote_variants,
#             'curr_user': self.curr_user,
#             'voting': self.voting,
#         }
#         return context
#
#     def post(self, request, **kwargs):
#         self.vote_var = request.POST.getlist('vote_var', None)  # берётся массив ответов
#         self.voting = get_object_or_404(Voting, id=1)  # это id голосования
#         self.vote_variants = self.voting.votevariant_set.all()
#         self.curr_user = request.user
#
#         if self.vote_var is not None:  # массив ответов записывается в БД
#             for var in self.vote_var:
#                 variant = get_object_or_404(VoteVariant, id=var)
#                 time = timezone.now()
#                 vote_fact = VoteFact(author=self.curr_user, variant=variant, created=time)
#                 vote_fact.save()
#
#         self.object = self.get_object()
#         context = super(VotingUpdateView, self).get_context_data(**kwargs)
#         context = {
#             'vote_variants': self.vote_variants,
#             'curr_user': self.curr_user,
#             'voting': self.voting,
#         }
#         return self.render_to_response(context=context)


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


def voting_page(request):
    vote_var = request.POST.getlist('vote_var', None)  # берётся массив ответов
    voting = get_object_or_404(Voting, id=1)  # это id голосования
    vote_variants = voting.votevariant_set.all()
    curr_user = request.user

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


def voting_list_page(request):
    context = {
        'history': Voting.objects.all()
    }
    return render(request, 'pages/voting_list.html', context)


def voting_results_page(request):
    context = {
        'user_name': request.user,
        'vote_name': 'name',
        'vote_results': '0%'
    }
    return render(request, 'pages/results.html', context)
