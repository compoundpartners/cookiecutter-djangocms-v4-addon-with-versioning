# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse, NoReverseMatch
from django.utils.translation import (
    ugettext as _, get_language_from_request, override)

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.i18n import get_language_tuple, get_language_dict
from cms.utils.urlutils import admin_reverse, add_url_parameters
from menus.utils import DefaultLanguageChanger


from {{ cookiecutter.project_slug }} import models

from cms.cms_toolbars import (
    ADMIN_MENU_IDENTIFIER,
    LANGUAGE_MENU_IDENTIFIER,
)

@toolbar_pool.register
class {{ cookiecutter.project_class }}Toolbar(CMSToolbar):
    watch_models = [models.{{ cookiecutter.project_class }}Content,]
    supported_apps = ('{{ cookiecutter.project_slug }}',)

    def _get_config(self):
        return getattr(self.request, '{{ cookiecutter.project_class.lower() }}_config', None)

    def populate(self):
        self.page = self.request.current_page
        config = self._get_config()
        if not config:
            # Do nothing if there is no NewsBlog {{ cookiecutter.project_config_class.lower() }} to work with
            return

        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            language = get_language_from_request(self.request, check_path=True)


            # get existing admin menu
            admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)

            # add new {{ cookiecutter.project_class }}s item
            admin_menu.add_sideframe_item(_('{{ cookiecutter.project_class }}s'), url='/admin/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_class.lower() }}content/', position=0)

            # If we're on an {{ cookiecutter.project_class }} detail page, then get the {{ cookiecutter.project_class.lower() }}
            if view_name == '{0}:detail'.format(config.namespace):
                kwargs = self.request.resolver_match.kwargs
                if 'pk' in kwargs:
                    {{ cookiecutter.project_class.lower() }} = {{ cookiecutter.project_class }}.all_objects.filter(pk=kwargs['pk']).first()
                elif 'slug' in kwargs:
                    filter_kwargs = {'slug': kwargs['slug'], 'language': language}
                    {{ cookiecutter.project_class.lower() }} = models.{{ cookiecutter.project_class }}Content.objects.filter(**filter_kwargs).first()
            else:
                {{ cookiecutter.project_class.lower() }} = None
            menu = self.toolbar.get_or_create_menu('{{ cookiecutter.project_slug }}_app', config.app_title)

            change_config_perm = user.has_perm(
                '{{ cookiecutter.project_slug }}.change_{{ cookiecutter.project_config_class.lower() }}')
            add_config_perm = user.has_perm(
                '{{ cookiecutter.project_slug }}.add_{{ cookiecutter.project_config_class.lower() }}')
            config_perms = [change_config_perm, add_config_perm]

            change_{{ cookiecutter.project_class.lower() }}_perm = user.has_perm(
                '{{ cookiecutter.project_slug }}.change_{{ cookiecutter.project_class.lower() }}content')
            delete_{{ cookiecutter.project_class.lower() }}_perm = user.has_perm(
                '{{ cookiecutter.project_slug }}.delete_{{ cookiecutter.project_class.lower() }}content')
            add_{{ cookiecutter.project_class.lower() }}_perm = user.has_perm('{{ cookiecutter.project_slug }}.add_{{ cookiecutter.project_class.lower() }}content')
            {{ cookiecutter.project_class.lower() }}_perms = [change_{{ cookiecutter.project_class.lower() }}_perm, add_{{ cookiecutter.project_class.lower() }}_perm,
                             delete_{{ cookiecutter.project_class.lower() }}_perm, ]

            if change_config_perm:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = add_url_parameters(
                    admin_reverse('{{ cookiecutter.project_slug }}_{{ cookiecutter.project_config_class.lower() }}_change',
                                  args=[config.pk, ]),
                    **url_args)

                menu.add_modal_item(_('Edit {{ cookiecutter.project_config_class.lower() }}'), url=url)

            if any(config_perms) and any({{ cookiecutter.project_class.lower() }}_perms):
                menu.add_break()

            if change_{{ cookiecutter.project_class.lower() }}_perm:
                url_args = {}
                if config and config.namespace != models.{{ cookiecutter.project_config_class }}.default_namespace:
                    url_args = {'{{ cookiecutter.project_config_class.lower() }}__id__exact': config.pk}
                url = add_url_parameters(
                    admin_reverse('{{ cookiecutter.project_slug }}_{{ cookiecutter.project_class.lower() }}content_changelist'),
                    **url_args)
                menu.add_sideframe_item(_('{{ cookiecutter.project_class }} list'), url=url)

            if add_{{ cookiecutter.project_class.lower() }}_perm:
                url_args = {'{{ cookiecutter.project_config_class.lower() }}': config.pk}
                if language:
                    url_args.update({'language': language, })
                url = add_url_parameters(
                    admin_reverse('{{ cookiecutter.project_slug }}_{{ cookiecutter.project_class.lower() }}content_add'),
                    **url_args)
                menu.add_modal_item(_('Add new {{ cookiecutter.project_class.lower() }}'), url=url)

            if change_{{ cookiecutter.project_class.lower() }}_perm and {{ cookiecutter.project_class.lower() }}:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = add_url_parameters(
                    admin_reverse('{{ cookiecutter.project_slug }}_{{ cookiecutter.project_class.lower() }}content_change',
                                  args=[{{ cookiecutter.project_class.lower() }}.pk, ]),
                    **url_args)
                menu.add_modal_item(_('Edit this {{ cookiecutter.project_class.lower() }}'), url=url,
                                    active=True)
