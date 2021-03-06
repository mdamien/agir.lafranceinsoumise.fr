from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.postgres.forms import DateRangeField

from data_france.models import CollectiviteDepartementale, CollectiviteRegionale
from django.core.exceptions import NON_FIELD_ERRORS

from agir.elus.models import (
    MandatMunicipal,
    STATUT_A_VERIFIER_INSCRIPTION,
    MUNICIPAL_DEFAULT_DATE_RANGE,
    DEPARTEMENTAL_DEFAULT_DATE_RANGE,
    REGIONAL_DEFAULT_DATE_RANGE,
    DELEGATIONS_CHOICES,
    STATUT_A_VERIFIER_IMPORT,
    STATUT_A_VERIFIER_ADMIN,
    MandatDepartemental,
    MandatRegional,
)
from agir.lib.form_fields import CommuneField
from agir.people.models import Person


class BaseMandatForm(forms.ModelForm):
    default_date_range = None

    membre_reseau_elus = forms.ChoiceField(
        label="Souhaitez-vous faire partie du réseau des élu⋅es ?",
        choices=(
            (Person.MEMBRE_RESEAU_SOUHAITE, "Oui"),
            (Person.MEMBRE_RESEAU_NON, "Non"),
        ),
        required=True,
    )

    dates = DateRangeField(
        label="Dates de votre mandat",
        required=True,
        help_text="Indiquez la date de votre entrée au conseil, et la date approximative à laquelle votre"
        " mandat devrait se finir (à moins que vous n'ayiez déjà démissionné).",
    )

    delegations = forms.MultipleChoiceField(
        label="Si vous êtes vice-président⋅e, indiquez dans quels domains rentrent vos"
        " délégations.",
        choices=DELEGATIONS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, person, **kwargs):
        super().__init__(*args, **kwargs)

        self.instance.person = person

        self.fields["mandat"].choices = [
            (None, "Indiquez votre situation au conseil")
        ] + self.fields["mandat"].choices[1:]

        if person.membre_reseau_elus == Person.MEMBRE_RESEAU_NON:
            self.fields["membre_reseau_elus"].initial = Person.MEMBRE_RESEAU_NON
        elif person.membre_reseau_elus != Person.MEMBRE_RESEAU_INCONNU:
            del self.fields["membre_reseau_elus"]

        self.fields["dates"].initial = self.default_date_range

        self.helper = FormHelper()
        self.helper.add_input(Submit("valider", "Valider"))
        self.helper.layout = Layout("mandat", "dates", "delegations")
        if "membre_reseau_elus" in self.fields:
            self.helper.layout.fields.insert(0, "membre_reseau_elus")

    def save(self, commit=True):
        if self.instance.statut in [STATUT_A_VERIFIER_ADMIN, STATUT_A_VERIFIER_IMPORT]:
            self.instance.statut = STATUT_A_VERIFIER_INSCRIPTION

        if "membre_reseau_elus" in self.fields:
            self.instance.person.membre_reseau_elus = self.cleaned_data[
                "membre_reseau_elus"
            ]
            self.instance.person.save(update_fields=["membre_reseau_elus"])

        return super().save(commit=commit)

    class Meta:
        fields = ("dates", "mandat")
        error_messages = {
            NON_FIELD_ERRORS: {
                "dates_overlap": "Vous avez déjà indiqué un autre mandat pour ce conseil à des dates qui se"
                " chevauchent. Modifiez plutôt cet autre mandat."
            }
        }


class MandatMunicipalForm(BaseMandatForm):
    default_date_range = MUNICIPAL_DEFAULT_DATE_RANGE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["delegations"].help_text = (
            "Si vous êtes maire adjoint⋅e ou vice-président⋅e de l'EPCI, indiquez dans quels domaines rentrent vos"
            " délégations."
        )

        self.fields["communautaire"].choices = [
            (None, "Indiquez si vous êtes délégué⋅e à l'intercommunalité")
        ] + [
            c
            for c in self.fields["communautaire"].choices
            if c[0] != MandatMunicipal.MANDAT_EPCI_MANDAT_INCONNU
        ]

        if self.instance.conseil_id is not None:
            if self.instance.conseil.epci:
                self.fields[
                    "communautaire"
                ].label = f"Élu⋅e à la {self.instance.conseil.epci.nom}"
            else:
                del self.fields["communautaire"]

        self.helper.layout = Layout("mandat", "communautaire", "dates", "delegations")
        if "membre_reseau_elus" in self.fields:
            self.helper.layout.fields.insert(2, "membre_reseau_elus")

    class Meta(BaseMandatForm.Meta):
        model = MandatMunicipal
        fields = BaseMandatForm.Meta.fields + ("communautaire", "delegations",)


class CreerMandatMunicipalForm(MandatMunicipalForm):
    conseil = CommuneField(types=["COM", "SRM"], label="Commune")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout.fields.insert(0, "conseil")

    class Meta(MandatMunicipalForm.Meta):
        fields = ("conseil",) + MandatMunicipalForm.Meta.fields


class MandatDepartementalForm(BaseMandatForm):
    default_date_range = DEPARTEMENTAL_DEFAULT_DATE_RANGE

    class Meta(BaseMandatForm.Meta):
        model = MandatDepartemental
        fields = BaseMandatForm.Meta.fields + ("delegations",)


class CreerMandatDepartementalForm(MandatDepartementalForm):
    conseil = forms.ModelChoiceField(
        CollectiviteDepartementale.objects.all(),
        label="Département ou métropole",
        empty_label="Choisissez la collectivité",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout.fields.insert(0, "conseil")

    class Meta(MandatDepartementalForm.Meta):
        fields = ("conseil",) + MandatDepartementalForm.Meta.fields


class MandatRegionalForm(BaseMandatForm):
    default_date_range = REGIONAL_DEFAULT_DATE_RANGE

    class Meta(BaseMandatForm.Meta):
        model = MandatRegional
        fields = BaseMandatForm.Meta.fields + ("delegations",)


class CreerMandatRegionalForm(MandatRegionalForm):
    conseil = forms.ModelChoiceField(
        CollectiviteRegionale.objects.all(),
        label="Région ou collectivité unique",
        empty_label="Choisissez la collectivité",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout.fields.insert(0, "conseil")

    class Meta(MandatRegionalForm.Meta):
        fields = ("conseil",) + MandatRegionalForm.Meta.fields
