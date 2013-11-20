# encoding: utf-8

from django.db.models import Count
from django.utils.timezone import now

from etat.departments.models import Department
from etat.members.models import Member, Role, RoleType, Reachability

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Migrate data from import'

    def handle_noargs(self, **options):
        relevant_departments = ('Glockenhof', 'APV Glockenhof', 'HV Glockenhof',
            u'Pfadi Züri', 'Flamberg', 'PBS', u'CVJM Zürich 1')

        print u"Deaktiviere alle Korps ausser ", relevant_departments
        for d in Department.objects.root_nodes():
            if d.name not in relevant_departments:
                d.get_descendants(include_self=True).update(active=False)

        print u"Speichere aktive Rollen"
        Role.objects.active().update(active=True)
        Role.objects.inactive().update(active=False)

        print u"Abteilunsgsstaebe zu Abteilungen migrieren"
        staebe = Department.objects.filter(name="Abteilungsstab")
        for d in staebe:
            for r in d.roles.all():
                r.department = d.parent
                r.save()

        print u"Korpsteam zum Korps migrieren"
        korpstab = Department.objects.filter(name__in=("Korpsstab", "Korpsteam"))
        for d in korpstab:
            for r in d.roles.all():
                r.department = d.parent
                r.save()

        print u"Deaktiviere alle Gruppen ohne aktive Rollen"
        Department.objects.exclude(roles__active=True).update(active=False)

        print "Gruppen der Stufe ihrer Einheit zuweisen"
        for d in Department.objects.filter(type__name="Gruppe", step__isnull=True):
            Department.objects.filter(pk=d.pk).update(step=d.parent.step)

        print u"Keine normalen Mitglieder im Korpsstab"
        for r in Department.objects.get(name="Glockenhof").roles.filter(active=True):
            if r.type.name == "Mitglied / TeilnehmerIn":
                r.end = now().date()
                r.save()

        print u"Handy nummern als privat markieren"
        for r in Reachability.objects.filter(type='phone', value__startswith='07'):
            if not r.kind == 'private':
                r.kind = 'private'
                r.save()

        print u"Aktualisiere alte Vorwahl von Zuerich"
        for r in Reachability.objects.filter(type='phone', value__startswith='01'):
            r.value = r.value.replace('01/', '044 ').replace('01 ', '044 ')
            r.save()

        print u"Maedels korrigieren"
        Member.objects.filter(gender='w').update(gender='f')

        print u"Setze Stufen fuer Funktionstypen"
        RoleType.objects.filter(name="FSL").update(step=0)
        RoleType.objects.filter(name="WBSL").update(step=1)
        RoleType.objects.filter(name="PSL").update(step=2)
        RoleType.objects.filter(name="PioSL").update(step=3)
        RoleType.objects.filter(name="RSL").update(step=4)

        print u"Auch der Praesi muss anstehen"
        RoleType.objects.filter(name="Präsident / Obmann").update(order=666)