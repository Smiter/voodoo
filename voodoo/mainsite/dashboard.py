"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'test_project.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'test_project.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for test_project.
    """
    def init_with_context(self, context):
        self.children += [
            modules.AppList(
                _('Applications'),
                exclude=('django.contrib.*',),
            ),
            modules.AppList(
                _('Administration'),
                models=('django.contrib.*',),
            )
        ]


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for test_project.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(_(self.app_title), self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]
