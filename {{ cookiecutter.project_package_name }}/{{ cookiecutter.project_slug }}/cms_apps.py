# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from {{ cookiecutter.project_slug }} import models


@apphook_pool.register
class CMSConfigApp(CMSApp):
    name = _('{{ cookiecutter.project_name }}')
    app_name = '{{ cookiecutter.project_slug }}'
    app_config = models.{{ cookiecutter.project_config_class }}
    urls = ['{{ cookiecutter.project_slug }}.urls']

    def get_urls(self, *args, **kwargs):
        return self.urls

    def get_configs(self):
        self.app_config.get_default()
        return self.app_config.objects.all()

    def get_config(self, namespace):
        try:
            return self.app_config.objects.get(namespace=namespace)
        except ObjectDoesNotExist:
            return None

    def get_config_add_url(self):
        try:
            return reverse('admin:%s_%s_add' % (self.app_config._meta.app_label,
                                                self.app_config._meta.model_name))
        except AttributeError:  # pragma: no cover
            return reverse('admin:%s_%s_add' % (self.app_config._meta.app_label,
                                                self.app_config._meta.module_name))
