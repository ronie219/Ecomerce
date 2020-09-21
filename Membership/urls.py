from django.urls import path
from Membership.views import MembershipSelectView, payment, update_payment

app_name = 'Membership'

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', payment, name='payment'),
    path('update-transaction/<subscription_id>',update_payment,name='update-transactions')
]
