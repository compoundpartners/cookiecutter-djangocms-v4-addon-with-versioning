from django import forms

from {{ cookiecutter.project_slug }} import models


class {{ cookiecutter.project_class }}ContentForm(forms.ModelForm):
    {{ cookiecutter.project_config_class.lower() }} = forms.ModelChoiceField(queryset=models.{{ cookiecutter.project_config_class }}.objects.exclude(namespace=models.{{ cookiecutter.project_config_class }}.default_namespace))

    class Meta:
        model = models.{{ cookiecutter.project_class }}Content
        fields = (
            '{{ cookiecutter.project_config_class.lower() }}',
            '{{ cookiecutter.project_class.lower() }}',
            'language',
            'title',
            'slug',
            'meta_description',
            'template',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get('{{ cookiecutter.project_class.lower() }}'):
            self.fields['{{ cookiecutter.project_class.lower() }}'].widget = forms.HiddenInput()
            self.fields['{{ cookiecutter.project_class.lower() }}'].required = False
        if self.fields.get('language'):
            self.fields['language'].widget = forms.HiddenInput()
        if self.instance.{{ cookiecutter.project_class.lower() }} and self.instance.{{ cookiecutter.project_class.lower() }}.{{ cookiecutter.project_config_class.lower() }}:
            self.fields['{{ cookiecutter.project_config_class.lower() }}'].initial = self.instance.{{ cookiecutter.project_class.lower() }}.{{ cookiecutter.project_config_class.lower() }}

    def create_or_update_grouper(self, obj, **kwargs):
        '''
        If a grouper doesn't yet exist for the instance we may need to create one.
        :param obj: a {{ cookiecutter.project_class.lower() }} content instance
        :returns obj: a {{ cookiecutter.project_class.lower() }} content instance that may have a grouper attached.
        '''
        # Check whether the form used has the grouper attribute, as overrides do not.
        if isinstance(obj, self._meta.model) and not getattr(obj, '{{ cookiecutter.project_class.lower() }}'):
            obj.{{ cookiecutter.project_class.lower() }} = models.{{ cookiecutter.project_class }}.objects.create(**kwargs)
        else:
            obj.{{ cookiecutter.project_class.lower() }}.update(**kwargs)
        return obj

    def save(self, **kwargs):
        obj = super().save(commit=False)
        commit = kwargs.get('commit', True)
        # Create the grouper if it doesn't exist
        obj = self.create_or_update_grouper(obj, {{ cookiecutter.project_config_class.lower() }}=self.cleaned_data['{{ cookiecutter.project_config_class.lower() }}'])

        if commit:
            obj.save()
            obj.{{ cookiecutter.project_class.lower() }}.save()
        return obj
