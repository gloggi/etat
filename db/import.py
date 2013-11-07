#! /usr/bin/env python
# encoding: utf-8

import re
import os
import sys
import csv
from datetime import datetime

activate_this = '../venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etat.settings")
sys.path.append('..')

from django.utils.datastructures import SortedDict

FLOAT_RE = re.compile(r'^\d+\.\d+$')
INT_RE = re.compile(r'^\d+$')


class Dataset(list):

    def __init__(self, csv_file, mapping):

        with open(csv_file, 'rb') as f:
            rows = csv.reader(f)

            header = rows.next()

            for row in rows:
                entry = SortedDict()
                for name, value in zip(header, row):
                    key_name = mapping.get(name, name)

                    if FLOAT_RE.match(value):
                        value = float(value)
                    elif INT_RE.match(value):
                        value = int(value)
                    else:
                        value = value.decode('utf-8').strip()

                    entry[key_name] = value
                self.append(entry)


# Department import

from etat.departments.models import Department, DepartmentType

KORPS, __ = DepartmentType.objects.get_or_create(name='Korps / Region')
ABTEILUNG, __ = DepartmentType.objects.get_or_create(name='Abteilung')
EINHEIT, __ = DepartmentType.objects.get_or_create(name='Einheit')


existing_departments = Department.objects.all().values_list('legacy_id', flat=True)

korps = Dataset('Tabelle:Korps.csv', {
    'Korpsnummer': 'legacy_id',
    'Korpsname': 'name',
})

for k in korps:
    k['legacy_id'] = 'K%s' % k['legacy_id']

    if k['legacy_id'] in existing_departments:
        continue

    d = Department()
    for key, value in k.items():
        setattr(d, key, value)

    d.type = KORPS

    print d.legacy_id
    d.save()


abteilungen = Dataset('Tabelle:Abteilungen.csv', {
    'Abteilungsnummer': 'legacy_id',
    'Korpsnummer': 'parent_legacy_id',
    'Abteilungsname': 'name',
    'Homepage': 'website',
})

for a in abteilungen:
    a['legacy_id'] = 'A%s' % a['legacy_id']

    if a['legacy_id'] in existing_departments:
        continue

    d = Department()

    try:
        parent_id = 'K%s' % a['parent_legacy_id']
        d.parent = Department.objects.get(legacy_id=parent_id)
    except Department.DoesNotExist:
        continue

    for key, value in a.items():
        setattr(d, key, value)

    d.type = ABTEILUNG

    print d.legacy_id
    d.save()


einheiten = Dataset('Tabelle:Einheiten.csv', {
    'Einheitennummer': 'legacy_id',
    'Einheitenname': 'name',
    'Abteilungsnummer': 'parent_legacy_id',
})

for e in einheiten:
    e['legacy_id'] = 'E%s' % e['legacy_id']

    if e['legacy_id'] in existing_departments:
        continue

    d = Department()

    try:
        parent_id = 'A%s' % e['parent_legacy_id']
        d.parent = Department.objects.get(legacy_id=parent_id)
    except Department.DoesNotExist:
        continue

    for key, value in e.items():
        setattr(d, key, value)

    d.type = EINHEIT

    print d.legacy_id
    d.save()


# Member import

from etat.members.models import (Member, RoleType, Role, Address, Reachability,
    EducationType)

funktionstypen = Dataset('Tabelle:Funktionstypen.csv', {
    'Funktionsnummer': 'legacy_id',
    'Funktionsbezeichnung': 'name',
    'Sortierfolge': 'order'
})

existing_roles = RoleType.objects.all().values_list('legacy_id', flat=True)

for f in funktionstypen:

    if f['legacy_id'] in existing_roles:
        continue

    r = RoleType()

    for k, v in f.items():
        setattr(r, k, v)

    print r.legacy_id


stammdaten = Dataset('Stammdaten.csv', {
    'Ref': 'legacy_id',
    'Vorname': 'first_name',
    'nachname': 'last_name',
    'vulgo': 'scout_name',
    'Geschlecht': 'gender',
    'Memo': 'notes',

    'Adresse1': 'street',
    'PLZ': 'postal_code',
    'Ort': 'city',
    u'Landeskürzel': 'country',
})

Member.objects.all().delete()

existing_members = Member.objects.all().values_list('legacy_id', flat=True)

for p in stammdaten[:1000]:
    if p['legacy_id'] in existing_members:
        continue

    # Member
    m = Member()

    for k, v in p.items():
        setattr(m, k, v)

    if not m.gender:
        m.gender = 'w'

    if p['Geburtsdatum']:
        m.birthday = datetime.strptime(p['Geburtsdatum'], '%Y-%m-%d %H:%M:%S')

    m.save()

    # Adresse
    a = Address()

    for k, v in p.items():
        setattr(a, k, v)

    a.member = m
    a.main = True
    try:
        a.save()
    except:
        pass

    # Reachability

    if p['Telefon P']:
        Reachability.objects.create(
            member=m,
            type='phone',
            kind='private',
            value=p['Telefon P']
        )

    if p['Telefon G']:
        Reachability.objects.create(
            member=m,
            type='phone',
            kind='work',
            value=p['Telefon G']
        )

    if p['EMail']:
        Reachability.objects.create(
            member=m,
            type='email',
            value=p['EMail']
        )