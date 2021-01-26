from django.contrib import admin

# Register your models here.
from main.models import Voting, VoteVariant, Complaint

admin.site.register(Voting)
admin.site.register(VoteVariant)
admin.site.register(Complaint)
