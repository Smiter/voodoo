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

admin.site.register(Site)
admin.site.register(Group)
admin.site.register(User, UserAdmin)
