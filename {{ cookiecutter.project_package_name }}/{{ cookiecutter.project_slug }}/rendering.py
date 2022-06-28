from django.template.response import TemplateResponse


from {{ cookiecutter.project_slug }}.cache import set_{{ cookiecutter.project_class.lower() }}_cache
from {{ cookiecutter.project_slug }} import models


def render_{{ cookiecutter.project_class.lower() }}_content(request, {{ cookiecutter.project_class.lower() }}_content):
    language = {{ cookiecutter.project_class.lower() }}_content.language
    {{ cookiecutter.project_class.lower() }} = {{ cookiecutter.project_class.lower() }}_content.{{ cookiecutter.project_class.lower() }}
    {{ cookiecutter.project_class.lower() }}.translation_cache[language] = {{ cookiecutter.project_class.lower() }}_content
    context = {}
    context['lang'] = language
    context['{{ cookiecutter.project_class.lower() }}'] = {{ cookiecutter.project_class.lower() }}
    request.{{ cookiecutter.project_class.lower() }}_config = {{ cookiecutter.project_class.lower() }}.{{ cookiecutter.project_config_class.lower() }} or models.{{ cookiecutter.project_config_class }}.get_default()

    response = TemplateResponse(request, {{ cookiecutter.project_class.lower() }}_content.get_template(), context)
    response.add_post_render_callback(set_{{ cookiecutter.project_class.lower() }}_cache)
    return response
