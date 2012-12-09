# -*- coding: utf-8 -*-
from admin_tools.dashboard import modules

class MyModule(modules.DashboardModule):
    def is_empty(self):
        return self.message == ''

    def __init__(self, **kwargs):
        super(MyModule, self).__init__(**kwargs)
        self.template = 'my_block/hello.html'
        self.message = kwargs.get('message', '')