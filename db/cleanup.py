#! /usr/bin/env python
# encoding: utf-8

import os
import sys

activate_this = '../venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etat.settings")
sys.path.append('..')

from django.db.models import Count

from etat.departments.models import Department
from etat.members.models import Member, RoleType, Reachability

relevant_departments = ('Glockenhof', 'APV Glockenhof', 'HV Glockenhof')

print u"Entferne alle Abteilungen ausser ", relevant_departments
for d in Department.objects.root_nodes():
    if d.name not in relevant_departments:
        d.delete()

print u"Entferne alle inaktiven Einheiten"
for d in Department.objects.all():
    if d.roles.active().count() == 0:
        d.delete()
Department.objects.rebuild()

print u"Entferne Personen ohne jegliche Funktionen"
for m in Member.objects.annotate(role_count=Count('roles')):
    if m.role_count == 0:
        m.delete()

print u"Abteilunsgsstaebe zu Abteilungen migrieren"
for d in Department.objects.filter(name="Abteilungsstab"):
    for r in d.roles.all():
        r.department = d.parent
        r.save()
    d.delete()

print u"Korpsteam zum Korps migrieren"
for d in Department.objects.filter(name__in=("Korpsstab", "Korpsteam")):
    for r in d.roles.all():
        r.department = d.parent
        r.save()
    d.delete()

print "Gruppen der Stufe ihrer Einheit zuweisen"
for d in Department.objects.filter(type__name="Gruppe", step__isnull=True):
    d.step = d.parent.step
    d.save()

print u"Keine normalen Mitglieder im Korpsstab"
for r in Department.objects.get(name="Glockenhof").roles.all():
    if r.type.name == "Mitglied / TeilnehmerIn":
        r.delete()

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
Member.objects.exclude(gender='m').update(gender='f')

print u"Setze Stufen fuer Funktionstypen"
RoleType.objects.filter(name="FSL").update(step=0)
RoleType.objects.filter(name="WBSL").update(step=1)
RoleType.objects.filter(name="PSL").update(step=2)
RoleType.objects.filter(name="PioSL").update(step=3)
RoleType.objects.filter(name="RSL").update(step=4)