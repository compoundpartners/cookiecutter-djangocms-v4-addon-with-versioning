from django.conf import settings

from cms.app_base import CMSAppConfig
from cms.utils.i18n import get_language_tuple

from djangocms_versioning.datastructures import VersionableItem, default_copy
from djangocms_versioning.admin import ExtendedVersionAdminMixin

from {{ cookiecutter.project_slug }}.admin import ChangeLinkesAdminMixin
from {{ cookiecutter.project_slug }}.models import {{ cookiecutter.project_class }}Content
from {{ cookiecutter.project_slug }}.rendering import render_{{ cookiecutter.project_class.lower() }}_content


try:
    from djangocms_versioning.constants import DRAFT  # NOQA
    djangocms_versioning_installed = True
except ImportError:
    djangocms_versioning_installed = False


class {{ cookiecutter.project_class }}Config(CMSAppConfig):
    cms_enabled = True
    djangocms_versioning_enabled = True
    cms_toolbar_enabled_models = [({{ cookiecutter.project_class }}Content, render_{{ cookiecutter.project_class.lower() }}_content)]
    moderated_models = [{{ cookiecutter.project_class }}Content]

    djangocms_versioning_enabled = getattr(
        settings, 'VERSIONING_CMS_MODELS_ENABLED', True)

    if djangocms_versioning_enabled and djangocms_versioning_installed:

        versioning = [
            VersionableItem(
                content_model={{ cookiecutter.project_class }}Content,
                grouper_field_name='{{ cookiecutter.project_class.lower() }}',
                copy_function=lambda content: content.copy(),
                extra_grouping_fields=['language'],
                version_list_filter_lookups={'language': get_language_tuple},
                content_admin_mixin=ExtendedVersionAdminMixin,
            ),
        ]
