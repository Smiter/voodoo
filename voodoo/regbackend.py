from mainsite.forms import UserRegistrationForm
from mainsite.models import Profile
import logging

def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    data = Profile(user=user)
    logging.error(form.data["fio"])
    data.fio = form.data["fio"]
    data.save()

from registration.signals import user_registered
user_registered.connect(user_created)
