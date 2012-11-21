from mainsite.forms import UserRegistrationForm
from mainsite.models import Profile
import logging

def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    data = Profile(user=user)
    logging.error(form.data["fio"])
    data.fio = form.data["fio"]
    data.client_type = form.data["client_type"]
    data.country = form.data["country"]
    data.city = form.data["city"]
    data.phiz_adress = form.data["phiz_adress"]
    data.phone = form.data["phone"]
    data.contacts = form.data["contacts"]
    data.additional_info = form.data["additional_info"]
    data.carrier_default = form.data["carrier_default"]
    data.carrier_select = form.data["carrier_select"]
    data.save()

from registration.signals import user_registered
user_registered.connect(user_created)
