from django.contrib import admin
from Membership.models import Membership, UserMembership, Subscription

admin.site.register(Membership)
admin.site.register(Subscription)
admin.site.register(UserMembership)