from mainsite.forms import UserRegistrationForm
from mainsite.models import Profile
import logging

def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    data = Profile(user=user)
    logging.error(form.data["fio"])
    data.fio = form.data["fio"]
    data.fio = form.data["client_type"]
    data.fio = form.data["country"]
    data.fio = form.data["city"]
    data.fio = form.data["phiz_adress"]
    data.fio = form.data["phone"]
    data.fio = form.data["contacts"]
    data.fio = form.data["additional_info"]
    data.fio = form.data["carrier_default"]
    data.fio = form.data["carrier_select"]
    data.save()

from registration.signals import user_registered
user_registered.connect(user_created)
