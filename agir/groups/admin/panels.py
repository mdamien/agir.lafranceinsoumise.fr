from datetime import timedelta

from django.conf import settings
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.db.models import Count, Q, QuerySet
from django.db.models.expressions import RawSQL
from django.urls import path
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from functools import partial, update_wrapper

from agir.events.models import Event
from agir.groups import proxys
from agir.lib.admin import (
    CenterOnFranceMixin,
    DepartementListFilter,
    RegionListFilter,
    CountryListFilter,
)
from agir.lib.display import display_price
from agir.lib.utils import front_url
from . import actions
from . import views
from .forms import SupportGroupAdminForm
from .. import models
from ..actions.promo_codes import get_promo_codes
from ..models import Membership


class MembershipInline(admin.TabularInline):
    model = models.Membership
    fields = ("person_link", "membership_type")
    readonly_fields = ("person_link",)

    def person_link(self, obj):
        return mark_safe(
            '<a href="%s">%s</a>'
            % (
                reverse("admin:people_person_change", args=(obj.person.id,)),
                escape(obj.person),
            )
        )

    person_link.short_description = _("Personne")

    def has_add_permission(self, request, obj=None):
        return False


class GroupHasEventsFilter(admin.SimpleListFilter):
    title = _("Événements organisés dans les 2 mois précédents ou mois à venir")

    parameter_name = "is_active"

    def lookups(self, request, model_admin):
        return (("yes", _("Oui")), ("no", _("Non")))

    def queryset(self, request, queryset):
        queryset = queryset.annotate(
            current_events_count=Count(
                "organized_events",
                filter=Q(
                    organized_events__start_time__range=(
                        timezone.now() - timedelta(days=62),
                        timezone.now() + timedelta(days=31),
                    ),
                    organized_events__visibility=Event.VISIBILITY_PUBLIC,
                ),
            )
        )
        if self.value() == "yes":
            return queryset.exclude(current_events_count=0)
        if self.value() == "no":
            return queryset.filter(current_events_count=0)


class MembersFilter(admin.SimpleListFilter):
    title = "Membres"
    parameter_name = "members"

    def lookups(self, request, model_admin):
        return (("no_members", "Aucun membre"), ("no_referent", "Aucun animateur"))

    def queryset(self, request, queryset):
        if self.value() == "no_members":
            return queryset.filter(members=None)

        if self.value() == "no_referent":
            return queryset.exclude(
                memberships__membership_type=Membership.MEMBERSHIP_TYPE_REFERENT
            )


@admin.register(models.SupportGroup)
class SupportGroupAdmin(CenterOnFranceMixin, OSMGeoAdmin):
    form = SupportGroupAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "link",
                    "created",
                    "modified",
                    "action_buttons",
                    "promo_code",
                    "allocation",
                )
            },
        ),
        (
            _("Informations"),
            {
                "fields": (
                    "type",
                    "subtypes",
                    "description",
                    "allow_html",
                    "image",
                    "tags",
                    "published",
                )
            },
        ),
        (
            _("Lieu"),
            {
                "fields": (
                    "location_name",
                    "location_address1",
                    "location_address2",
                    "location_city",
                    "location_zip",
                    "location_state",
                    "location_country",
                    "coordinates",
                    "coordinates_type",
                    "redo_geocoding",
                )
            },
        ),
        (
            _("Contact"),
            {
                "fields": (
                    "contact_name",
                    "contact_email",
                    "contact_phone",
                    "contact_hide_phone",
                )
            },
        ),
        (_("NationBuilder"), {"fields": ("nb_id", "nb_path", "location_address")}),
    )
    inlines = (MembershipInline,)
    readonly_fields = (
        "id",
        "link",
        "action_buttons",
        "created",
        "modified",
        "coordinates_type",
        "promo_code",
        "allocation",
    )
    date_hierarchy = "created"

    list_display = (
        "name",
        "type",
        "published",
        "location_short",
        "membership_count",
        "created",
        "referents",
        "allocation",
    )
    list_filter = (
        "published",
        GroupHasEventsFilter,
        CountryListFilter,
        DepartementListFilter,
        RegionListFilter,
        "coordinates_type",
        MembersFilter,
        "type",
        "subtypes",
        "tags",
    )

    search_fields = ("name", "description", "location_city")
    actions = (actions.export_groups, actions.make_published, actions.unpublish)

    def promo_code(self, object):
        if object.pk and object.tags.filter(label=settings.PROMO_CODE_TAG).exists():
            return ", ".join(get_promo_codes(object))
        else:
            return "-"

    promo_code.short_description = _("Code promo du mois")

    def referents(self, object):
        referents = object.memberships.filter(
            membership_type__gte=Membership.MEMBERSHIP_TYPE_REFERENT
        ).select_related("person")
        if referents:
            return " / ".join(a.person.email for a in referents)

        return "-"

    referents.short_description = _("Animateur⋅ices")

    def location_short(self, object):
        return _("{zip} {city}, {country}").format(
            zip=object.location_zip,
            city=object.location_city,
            country=object.location_country.name,
        )

    location_short.short_description = _("Lieu")
    location_short.admin_order_field = "location_zip"

    def membership_count(self, object):
        return format_html(
            _('{nb} (<a href="{link}">Ajouter un membre</a>)'),
            nb=object.membership_count,
            link=reverse("admin:groups_supportgroup_add_member", args=(object.pk,)),
        )

    membership_count.short_description = _("Nombre de membres")
    membership_count.admin_order_field = "membership_count"

    def allocation(self, object, show_add_button=False):
        value = display_price(object.allocation) if object.allocation else "-"

        if show_add_button:
            value = format_html(
                '{value} (<a href="{link}">Changer</a>)',
                value=value,
                link=reverse("admin:donations_operation_add")
                + "?group="
                + str(object.pk),
            )

        return value

    allocation.short_description = _("Allocation")
    allocation.admin_order_field = "allocation"

    def link(self, object):
        if object.pk:
            return format_html(
                '<a href="{0}">{0}</a>',
                front_url("view_group", kwargs={"pk": object.pk}),
            )
        else:
            return mark_safe("-")

    link.short_description = _("Page sur le site")

    def action_buttons(self, object):
        if object._state.adding:
            return mark_safe("-")
        else:
            return format_html(
                '<a href="{add_member_link}" class="button">Ajouter un membre</a> '
                '<a href="{add_allocation_link}" class="button">Changer l\'allocation</a>'
                " <small>Attention : cliquer"
                " sur ces boutons quitte la page et perd vos modifications courantes.</small>",
                add_member_link=reverse(
                    "admin:groups_supportgroup_add_member", args=(object.pk,)
                ),
                add_allocation_link=reverse("admin:donations_operation_add")
                + "?group="
                + str(object.pk),
            )

    action_buttons.short_description = _("Actions")

    def get_queryset(self, request):
        qs: QuerySet = super().get_queryset(request)

        # noinspection SqlResolve
        return qs.annotate(
            membership_count=RawSQL(
                'SELECT COUNT(*) FROM "groups_membership" WHERE "supportgroup_id" = "groups_supportgroup"."id"',
                (),
            ),
            allocation=RawSQL(
                'SELECT SUM(amount) FROM "donations_operation" WHERE "group_id" = "groups_supportgroup"."id"',
                (),
            ),
        )

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            queryset = queryset.search(search_term)

        use_distinct = False

        return queryset, use_distinct

    def get_urls(self):
        return [
            path(
                "<uuid:pk>/add_member/",
                self.admin_site.admin_view(self.add_member),
                name="{}_{}_add_member".format(
                    self.opts.app_label, self.opts.model_name
                ),
            )
        ] + super().get_urls()

    def add_member(self, request, pk):
        return views.add_member(self, request, pk)

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        if request.user.has_perm("donations.add_operation"):
            try:
                idx = cl.list_display.index("allocation")
            except ValueError:
                pass
            else:
                cl.list_display[idx] = update_wrapper(
                    partial(self.allocation, show_add_button=True), self.allocation
                )
        return cl


@admin.register(proxys.ThematicGroup)
class ThematicGroupAdmin(SupportGroupAdmin):
    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + ("type",)


@admin.register(models.SupportGroupTag)
class SupportGroupTagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SupportGroupSubtype)
class SupportGroupSubtypeAdmin(admin.ModelAdmin):
    search_fields = ("label", "description")
    list_display = ("label", "description", "type", "visibility")
    list_filter = ("type", "visibility")
