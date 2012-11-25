"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register
from voodoo.mainsite.forms import UserRegistrationForm

urlpatterns = patterns('',
    url(r'^activate/complete/$',
       direct_to_template,
       {'template': 'registration/activation_complete.html'},
       name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
       activate,
       {'backend': 'voodoo.mainsite.RegistrationBackend.DefaultBackend'},
       name='registration_activate'),
    url(r'^accounts/register/$',
        register,
        {'backend': 'voodoo.mainsite.RegistrationBackend.DefaultBackend',
          'form_class': UserRegistrationForm
        },
        name='registration_register'),
    url(r'^register/complete/$',
       direct_to_template,
       {'template': 'registration/registration_complete.html'},
       name='registration_complete'),
    url(r'^register/closed/$',
       direct_to_template,
       {'template': 'registration/registration_closed.html'},
       name='registration_disallowed'),
    (r'', include('registration.auth_urls')),
)
