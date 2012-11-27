# -*- coding: utf-8 -*-
"""
Перерегистрируем стандартные модели.
"""
from __future__ import absolute_import
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from registration.admin import *
from russian_admin import admin

# from django.contrib.sites.models import RequestSite
# from voodoo.mainsite.models import MyRegistrationProfile, Profile
# from django.utils.translation import ugettext_lazy as _


# class MyRegistrationAdmin(admin.ModelAdmin):
#     actions = ['activate_users', 'resend_activation_email']
#     list_display = ('user', 'activation_key_expired')
#     raw_id_fields = ['user']
#     search_fields = ('user__username', 'user__first_name')

#     def activate_users(self, request, queryset):
#         """
#         Activates the selected users, if they are not alrady
#         activated.
#         """
#         for profile in queryset:
#             MyRegistrationProfile.objects.activate_user(profile.activation_key)
#     activate_users.short_description = _("Activate users")

#     def resend_activation_email(self, request, queryset):
#         """
#         Re-sends activation emails for the selected users.

#         Note that this will *only* send activation emails for users
#         who are eligible to activate; emails will not be sent to users
#         whose activation keys have expired or who have already
#         activated.
        
#         """
#         if Site._meta.installed:
#             site = Site.objects.get_current()
#         else:
#             site = RequestSite(request)

#         for profile in queryset:
#             if not profile.activation_key_expired():
#                 profile.send_activation_email(site)
#     resend_activation_email.short_description = _("Re-send activation emails")

# admin.site.register(MyRegistrationProfile, MyRegistrationAdmin)
# admin.site.register(Profile)
admin.site.register(Site)
admin.site.register(Group)
admin.site.register(User, UserAdmin)
# admin.site.register(RegistrationProfile, RegistrationAdmin)
