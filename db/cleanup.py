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

print "Removing all root departments except of ", relevant_departments
for d in Department.objects.root_nodes():
    if d.name not in relevant_departments:
        d.delete()

print "Removing all departments without active members"
for d in Department.objects.all():
    if d.roles.active().count() == 0:
        d.delete()
Department.objects.rebuild()

print "Removing members without any roles"
for m in Member.objects.annotate(role_count=Count('roles')):
    if m.role_count == 0:
        m.delete()

print "Move Abteilunsgsstäbe"
for d in Department.objects.filter(name="Abteilungsstab"):
    for r in d.roles.all():
        r.department = d.parent
        r.save()
    d.delete()

print "Move Korpsstam"
for d in Department.objects.filter(name__in=("Korpsstab", "Korpsteam")):
    for r in d.roles.all():
        r.department = d.parent
        r.save()
    d.delete()

print "No members in Korpsstab"
for r in Department.objects.get(name="Glockenhof").roles.all():
    if r.type.name == "Mitglied / TeilnehmerIn":
        r.delete()

print "Make mobile phone numbers private"
for r in Reachability.objects.filter(type='phone', value__startswith='07'):
    if not r.kind == 'private':
        r.kind = 'private'
        r.save()

print "Remove duplicate phone numbers"
# for m in Member.objects.all():
#     if m.reachabilities.filter(type='phone').count() == 2:
#         p1, p2 = m.reachabilities.filter(type='phone')
#         if p1.value == p2.value:
#             p2.delete()

print "Update old phone preselection"
for r in Reachability.objects.filter(type='phone', value__startswith='01'):
    r.value = r.value.replace('01/', '044 ').replace('01 ', '044 ')
    r.save()

print "Fix the ladies"
Member.objects.exclude(gender='m').update(gender='f')