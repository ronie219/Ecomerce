import stripe
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from stripe.error import CardError

from Membership.models import Membership, UserMembership, Subscription


def get_membership(request):
    userMembership_qs = UserMembership.objects.filter(user=request.user)
    if userMembership_qs.exists():
        return userMembership_qs.first()
    else:
        return None


def get_subscription(request):
    user_subscription_qs = Subscription.objects.filter(user_membership=get_membership(request))
    if user_subscription_qs.exists():
        return user_subscription_qs
    else:
        return None


def get_selected_membership(request):
    membership_type = request.session['selected_mebership_type']
    seleted_membership_qs = Membership.objects.filter(membership_type=membership_type)
    if seleted_membership_qs.exists():
        return seleted_membership_qs.first()
    else:
        return None


class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_membership(self.request)
        context['curent_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        global selected_mebership
        selected_mebership_type = request.POST.get('memberships_type')

        user_membership = get_membership(request)
        user_subscription = get_subscription(request)

        selected_mebership_qs = Membership.objects.filter(membership_type=selected_mebership_type)
        if selected_mebership_qs.exists():
            selected_mebership = selected_mebership_qs.first()

        """ Validation """

        if user_membership.membership == selected_mebership:
            if user_subscription is not None:
                messages.info(request, 'Your subscription is Due, Due date is {}'.format('get from stripe'))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        # assign to session
        request.session['selected_mebership_type'] = selected_mebership.membership_type
        return HttpResponseRedirect(reverse('Membership:payment'))


def payment(request):
    user_membership = get_membership(request)
    seleted_membership = get_selected_membership(request)
    publish_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST.get('stripeToken', False)
            stripe.Customer.create(
                name='Jenny Rosen',
                address={
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'US',
                },
            )

            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token  # 4242424242424242
            customer.save()



            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[{"plan": seleted_membership.stripe_plan_id}],
            )
            return redirect(reverse("Membership:update-payment"), kwargs={
                'subscription_id': subscription.id
            })
        except CardError as e:
            messages.info(request, "Card get Declined")

        # except MultiValueDictKeyError:
        #     pass

    context = {
        'publish_key': publish_key,
        'seleted_membership': seleted_membership
    }
    return render(request, 'Membership/membership_payment.html', context)


def update_payment(request, subscription_id):
    user_membership = get_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_mebership_type']

    except:
        pass

    messages.info(request, "SuccessFull created {} membership".format(selected_membership))
    return redirect('/course/')
