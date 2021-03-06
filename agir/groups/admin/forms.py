from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.utils.translation import ugettext_lazy as _

from agir.groups.models import SupportGroupSubtype, SupportGroup
from agir.lib.form_fields import AdminRichEditorWidget
from agir.lib.forms import CoordinatesFormMixin
from agir.people.models import Person
from .. import models


class SupportGroupAdminForm(CoordinatesFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_creation = self.instance._state.adding
        if self.is_creation:
            self.fields[
                "subtypes"
            ].label_from_instance = lambda instance: "{} ({})".format(
                instance.label, dict(SupportGroup.TYPE_CHOICES)[instance.type]
            )
        else:
            self.fields["subtypes"].queryset = SupportGroupSubtype.objects.filter(
                type=self.instance.type
            )

    class Meta:
        exclude = ("id", "members")
        widgets = {
            "description": AdminRichEditorWidget(),
            "tags": forms.CheckboxSelectMultiple(),
            "subtypes": forms.CheckboxSelectMultiple(),
        }


class AddMemberForm(forms.Form):
    person = forms.ModelChoiceField(
        Person.objects.all(), required=True, label=_("Personne à ajouter")
    )

    def __init__(self, group, model_admin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.fields["person"].widget = AutocompleteSelect(
            rel=Person._meta.get_field("memberships"),
            admin_site=model_admin.admin_site,
            choices=self.fields["person"].choices,
        )

    def clean_person(self):
        person = self.cleaned_data["person"]
        if models.Membership.objects.filter(
            person=person, supportgroup=self.group
        ).exists():
            raise forms.ValidationError(_("Cette personne fait déjà partie du groupe"))

        return person

    def save(self):
        return models.Membership.objects.create(
            person=self.cleaned_data["person"], supportgroup=self.group
        )
