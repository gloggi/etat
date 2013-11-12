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
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2} 00:00:00$')
DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

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
                    elif DATE_RE.match(value):
                        value = value.split(' ')[0]
                        value = datetime.strptime(value, '%Y-%m-%d').date()
                    elif DATETIME_RE.match(value):
                        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    else:
                        value = value.decode('utf-8').strip()

                    entry[key_name] = value
                self.append(entry)


# Department import

from etat.departments.models import Department, DepartmentType

KORPS, __ = DepartmentType.objects.get_or_create(name='Korps / Region', order=1)
ABTEILUNG, __ = DepartmentType.objects.get_or_create(name='Abteilung', order=2)
EINHEIT, __ = DepartmentType.objects.get_or_create(name='Einheit', order=3)
GRUPPE, __ = DepartmentType.objects.get_or_create(name='Gruppe', order=4)

existing_departments = Department.objects.all().values_list('legacy_id', flat=True)


with Department.objects.delay_mptt_updates():
    korps = Dataset('Tabelle:Korps.csv', {
        'Korpsnummer': 'legacy_id',
        'Korpsname': 'name',
        'Korpskurzname': 'short_name',
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
        'Abteilungskurzname': 'short_name',
        'Homepage': 'website',
    })

    dep_mapping = dict(Department.objects.all().values_list('legacy_id', 'id'))

    for a in abteilungen:
        a['legacy_id'] = 'A%s' % a['legacy_id']

        if a['legacy_id'] in existing_departments:
            continue

        d = Department()

        try:
            d.parent_id = dep_mapping['K%s' % a['parent_legacy_id']]
        except KeyError:
            continue

        for key, value in a.items():
            setattr(d, key, value)

        d.type = ABTEILUNG

        print d.legacy_id
        d.save()


    einheiten = Dataset('Tabelle:Einheiten.csv', {
        'Einheitennummer': 'legacy_id',
        'Einheitenname': 'name',
        'Einheitenkurzname': 'short_name',
        'Abteilungsnummer': 'parent_legacy_id',
        'Stufe': 'step',
    })

    dep_mapping = dict(Department.objects.all().values_list('legacy_id', 'id'))

    for e in einheiten:
        e['legacy_id'] = 'E%s' % e['legacy_id']

        if e['legacy_id'] in existing_departments:
            continue

        if not type(e['step']) == int:
            del e['step']

        d = Department()

        try:
            d.parent_id = dep_mapping['A%s' % e['parent_legacy_id']]
        except KeyError:
            continue

        for key, value in e.items():
            setattr(d, key, value)

        d.type = EINHEIT

        print d.legacy_id
        d.save()


    gruppen = Dataset('Tabelle:Gruppen.csv', {
        'Gruppennummer': 'legacy_id',
        'Gruppenname': 'name',
        'Gruppenkurzname': 'short_name',
        'Einheitennummer': 'parent_legacy_id'
    })

    dep_mapping = dict(Department.objects.all().values_list('legacy_id', 'id'))

    for g in gruppen:
        g['legacy_id'] = 'G%s' % g['legacy_id']

        if g['legacy_id'] in existing_departments:
            continue

        d = Department()

        try:
            d.parent_id = dep_mapping['E%s' % g['parent_legacy_id']]
        except KeyError:
            continue

        for key, value in g.items():
            setattr(d, key, value)

        d.type = GRUPPE

        print d.legacy_id
        d.save()

# Member import

from etat.members.models import (Member, RoleType, Role, Address, Reachability,
    EducationType, Education)

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

    print 'Funktionstyp', r.legacy_id
    r.save()


stammdaten = Dataset('Stammdaten.csv', {
    'Ref': 'legacy_id',
    'Vorname': 'first_name',
    'nachname': 'last_name',
    'vulgo': 'scout_name',
    'Geschlecht': 'gender',
    'Geburtsdatum': 'birthday',
    'Memo': 'notes',

    'Adresse1': 'street',
    'Adresse2': 'additon',
    'PLZ': 'postal_code',
    'Ort': 'city',
    u'Landeskürzel': 'country',
})

existing_members = Member.objects.all().values_list('legacy_id', flat=True)

for p in stammdaten:
    if p['legacy_id'] in existing_members:
        continue

    # Member
    m = Member()

    if not p['birthday']:
        p['birthday'] = None

    if p['additon']:
        p['street'] += ' ' + unicode(p['additon'])

    for k, v in p.items():
        setattr(m, k, v)

    if not m.gender:
        m.gender = 'f'

    print 'Person ', m.legacy_id
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


funktionen = Dataset('Tabelle:Funktionen.csv', {
    'Beziehungsnummer': 'legacy_id',
    'Ref zur Person': 'member_id',
    'Funktionstyp': 'role_type_id',
    'Korpsnummer': 'korps_id',
    'Abteilungsnummer': 'abteilung_id',
    'Einheitsnummer': 'einheit_id',
    'Gruppennummer': 'gruppe_id',
    'Beginn': 'start',
    'Ende': 'end',
})

member_mapping = dict(Member.objects.all().values_list('legacy_id', 'id'))

role_type_mapping = dict(RoleType.objects.all().values_list('legacy_id', 'id'))

department_mapping = dict(Department.objects.all().values_list('legacy_id', 'id'))

existing_roles = Role.objects.all().values_list('legacy_id', flat=True)

for f in funktionen:

    if f['legacy_id'] in existing_roles:
        continue

    try:
        if f['gruppe_id']:
            department_id = department_mapping['G%d' % f['gruppe_id']]
        elif f['einheit_id']:
            department_id = department_mapping['E%d' % f['einheit_id']]
        elif f['abteilung_id']:
            department_id = department_mapping['A%d' % f['abteilung_id']]
        elif f['korps_id']:
            department_id = department_mapping['K%d' % f['korps_id']]
        else:
            continue
    except:
        continue

    if type(f['start']) == unicode:
        f['start'] = None
    elif type(f['start']) == datetime:
        f['start'] = f['start'].date()

    if type(f['end']) == unicode:
        f['end'] = None
    elif type(f['start']) == datetime:
        f['end'] = f['end'].date()

    print 'Funktion ', f['legacy_id']
    Role.objects.create(
        member_id=member_mapping[f['member_id']],
        department_id=department_id,
        type_id=role_type_mapping[f['role_type_id']],
        start=f['start'],
        end=f['end'],
        legacy_id=f['legacy_id']
    )

ausbildungstypen = Dataset('Tabelle:Ausbildungstypen.csv', {
    'Ausbildungstypnummer': 'legacy_id',
    'Ausbildungsname': 'title',
    'Sortierfolge': 'order',
})

existing_education_types = EducationType.objects.all().values_list('legacy_id', flat=True)

for a in ausbildungstypen:
    if a['legacy_id'] in existing_education_types:
        continue

    e = EducationType()

    for k, v in a.items():
        setattr(e, k, v)

    print 'Ausbildungstyp', e.legacy_id
    e.save()


education_type_mapping = dict(EducationType.objects.all().values_list('legacy_id', 'id'))

ausbildungen = Dataset('Tabelle:Ausbildungen.csv', {
    'Ausbildungsnummer': 'legacy_id',
    'Ref zur Person': 'member_legacy_id',
    'Ausbildungstyp': 'education_type_legacy_id',
    'Beginn': 'date'
})

existing_educations = Education.objects.all().values_list('legacy_id', flat=True)

for a in ausbildungen:
    if a['legacy_id'] in existing_educations:
        continue

    if not a['date']:
        a['date'] = None

    try:
        Education.objects.create(
            member_id=member_mapping[a['member_legacy_id']],
            type_id=education_type_mapping[a['education_type_legacy_id']],
            date=a['date'],
            legacy_id=a['legacy_id']
        )
        print 'Ausbildung', a['legacy_id']
    except:
        continue