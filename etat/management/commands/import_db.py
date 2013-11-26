# encoding: utf-8
import re
import csv
from datetime import datetime

from django.core.management.base import NoArgsCommand
from django.utils.datastructures import SortedDict

from etat.departments.models import Department, DepartmentType
from etat.members.models import (Member, RoleType, Role, Address, Reachability,
    EducationType, Education)

FLOAT_RE = re.compile(r'^\d+\.\d+$')
INT_RE = re.compile(r'^\d+$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2} 00:00:00$')
DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')


class Dataset(list):

    def __init__(self, csv_file):

        with open(csv_file, 'rb') as f:
            rows = csv.reader(f)
            header = rows.next()
            for row in rows:
                entry = SortedDict()
                for name, value in zip(header, row):
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

                    entry[name] = value
                self.append(entry)

    def map(self, mapping):
        res = []
        for entry in self:
            data = {}
            for k, v in entry.items():
                if k in mapping:
                    data[mapping[k]] = v
            res.append(data)
        return res

KORPS, __ = DepartmentType.objects.get_or_create(name='Korps / Region', order=1)
ABTEILUNG, __ = DepartmentType.objects.get_or_create(name='Abteilung', order=2)
EINHEIT, __ = DepartmentType.objects.get_or_create(name='Einheit', order=3)
GRUPPE, __ = DepartmentType.objects.get_or_create(name='Gruppe', order=4)


class Command(NoArgsCommand):
    help = 'Import the old database form csv export'

    def handle_noargs(self, **options):

        print "Load csv data"
        self.korps = Dataset('db/Tabelle:Korps.csv')
        self.abteilungen = Dataset('db/Tabelle:Abteilungen.csv')
        self.einheiten = Dataset('db/Tabelle:Einheiten.csv')
        self.gruppen = Dataset('db/Tabelle:Gruppen.csv')

        self.stammdaten = Dataset('db/Stammdaten.csv')
        self.funktionstypen = Dataset('db/Tabelle:Funktionstypen.csv')
        self.funktionen = Dataset('db/Tabelle:Funktionen.csv')
        self.ausbildungstypen = Dataset('db/Tabelle:Ausbildungstypen.csv')
        self.ausbildungen = Dataset('db/Tabelle:Ausbildungen.csv')

        self.existing_departments = Department.objects.all().values_list(
            'legacy_id', flat=True)

        self.import_korps()
        self.import_abteilungen()
        self.import_einheiten()
        self.import_gruppen()

        self.import_stammdaten()
        self.import_addressen()
        self.import_erreichbarkeiten()
        self.import_funktionstypen()
        self.import_funktionen()
        self.import_ausbildungstypen()
        self.import_ausbildungen()

    def import_korps(self):
        korps = self.korps.map({
            'Korpsnummer': 'legacy_id',
            'Korpsname': 'name',
            'Korpskurzname': 'short_name',
        })
        new_korps = []

        for k in korps:
            k['legacy_id'] = 'K%s' % k['legacy_id']
            if k['legacy_id'] in self.existing_departments:
                continue
            d = Department()
            for key, value in k.items():
                setattr(d, key, value)

            d.type = KORPS
            self.mptt_dummy(d)
            new_korps.append(d)

        if new_korps:
            print "Import %d Korps" % len(new_korps)
            Department.objects.bulk_create(new_korps)
            Department.objects.rebuild()

    def import_abteilungen(self):
        abteilungen = self.abteilungen.map({
            'Abteilungsnummer': 'legacy_id',
            'Korpsnummer': 'parent_legacy_id',
            'Abteilungsname': 'name',
            'Abteilungskurzname': 'short_name',
            'Homepage': 'website',
        })
        dep_mapping = self.department_mapping()
        new_abteilungen = []

        for a in abteilungen:
            a['legacy_id'] = 'A%s' % a['legacy_id']
            if a['legacy_id'] in self.existing_departments:
                continue
            d = Department()
            try:
                d.parent_id = dep_mapping['K%s' % a['parent_legacy_id']]
            except KeyError:
                continue

            for key, value in a.items():
                setattr(d, key, value)

            d.type = ABTEILUNG
            self.mptt_dummy(d)
            new_abteilungen.append(d)

        if new_abteilungen:
            print "Import %d Abteilungen" % len(new_abteilungen)
            Department.objects.bulk_create(new_abteilungen)
            Department.objects.rebuild()

    def import_einheiten(self):
        einheiten = self.einheiten.map({
            'Einheitennummer': 'legacy_id',
            'Einheitenname': 'name',
            'Einheitenkurzname': 'short_name',
            'Abteilungsnummer': 'parent_legacy_id',
            'Stufe': 'step',
        })
        dep_mapping = self.department_mapping()
        new_einheiten = []

        for e in einheiten:
            e['legacy_id'] = 'E%s' % e['legacy_id']
            if e['legacy_id'] in self.existing_departments:
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
            self.mptt_dummy(d)
            new_einheiten.append(d)

        if new_einheiten:
            print "Import %d Einheiten" % len(new_einheiten)
            Department.objects.bulk_create(new_einheiten)
            Department.objects.rebuild()

    def import_gruppen(self):
        gruppen = self.gruppen.map({
            'Gruppennummer': 'legacy_id',
            'Gruppenname': 'name',
            'Gruppenkurzname': 'short_name',
            'Einheitennummer': 'parent_legacy_id'
        })
        dep_mapping = self.department_mapping()
        new_gruppen = []

        for g in gruppen:
            g['legacy_id'] = 'G%s' % g['legacy_id']
            if g['legacy_id'] in self.existing_departments:
                continue
            d = Department()
            try:
                d.parent_id = dep_mapping['E%s' % g['parent_legacy_id']]
            except KeyError:
                continue
            for key, value in g.items():
                setattr(d, key, value)

            d.type = GRUPPE
            self.mptt_dummy(d)
            new_gruppen.append(d)

        if new_gruppen:
            print "Import %d Gruppen" % len(new_gruppen)
            Department.objects.bulk_create(new_gruppen)
            Department.objects.rebuild()

    def import_stammdaten(self):
        stammdaten = self.stammdaten.map({
            'Ref': 'legacy_id',
            'Vorname': 'first_name',
            'nachname': 'last_name',
            'vulgo': 'scout_name',
            'Geschlecht': 'gender',
            'Geburtsdatum': 'birthday',
            'Anmeldung': 'application',
            'Memo': 'notes',
        })
        existing_members = Member.objects.all().values_list('legacy_id', flat=True)
        new_members = []

        for p in stammdaten:
            if p['legacy_id'] in existing_members:
                continue
            m = Member()
            if not p['birthday'] or isinstance(p['birthday'], basestring):
                p['birthday'] = None
            if p.get('gender') == 'w':
                p['gender'] = 'f'
            for k, v in p.items():
                setattr(m, k, v)

            new_members.append(m)

        if new_members:
            print "Import %d Personen" % len(new_members)
            Member.objects.bulk_create(new_members)

    def import_addressen(self):
        stammdaten = self.stammdaten.map({
            'Ref': 'legacy_id',
            'Adresse1': 'street',
            'Adresse2': 'addition',
            'PLZ': 'postal_code',
            'Ort': 'city',
            u'Landeskürzel': 'country',
        })
        existing_addresses = Address.objects.all().values_list('legacy_id', flat=True)
        member_mapping = dict(Member.objects.all().values_list('legacy_id', 'id'))
        new_addresses = []

        for p in stammdaten:
            if p['legacy_id'] in existing_addresses:
                continue
            if not p['postal_code']:
                continue
            if p['addition']:
                p['street'] += ' ' + unicode(p['addition'])
            a = Address()
            for k, v in p.items():
                setattr(a, k, v)

            a.member_id = member_mapping[p['legacy_id']]
            a.main = True
            new_addresses.append(a)

        if new_addresses:
            print "Import %d Addressen" % len(new_addresses)
            Address.objects.bulk_create(new_addresses)

    def import_erreichbarkeiten(self):
        stammdaten = self.stammdaten.map({
            'Ref': 'legacy_id',
            'Telefon P': 'phone',
            'Telefon G': 'mobile',
            'EMail': 'email'
        })
        member_mapping = dict(Member.objects.all().values_list('legacy_id', 'id'))
        existing_reachabilites = Reachability.objects.all().values_list(
            'legacy_id', flat=True)
        new_reachabilities = []

        for p in stammdaten:
            # Reachability
            member_id = member_mapping[p['legacy_id']]

            if p['phone']:
                legacy_id = p['legacy_id']
                if legacy_id not in existing_reachabilites:
                    new_reachabilities.append(
                        Reachability(
                            member_id=member_id,
                            type='phone',
                            kind='private',
                            value=p['phone'],
                            legacy_id=legacy_id,
                        )
                    )
            if p['mobile']:
                legacy_id = p['legacy_id'] + 100000
                if legacy_id not in existing_reachabilites:
                    new_reachabilities.append(
                        Reachability(
                            member_id=member_id,
                            type='phone',
                            kind='work',
                            value=p['mobile'],
                            legacy_id=legacy_id,
                        )
                    )
            if p['email']:
                legacy_id = p['legacy_id'] + 2000000
                if legacy_id not in existing_reachabilites:
                    new_reachabilities.append(
                        Reachability(
                            member_id=member_id,
                            type='email',
                            value=p['email'],
                            legacy_id=legacy_id,
                        )
                    )

        if new_reachabilities:
            print "Import %d Reachabilities" % len(new_reachabilities)
            Reachability.objects.bulk_create(new_reachabilities)

    def import_funktionstypen(self):
        funktionstypen = self.funktionstypen.map({
            'Funktionsnummer': 'legacy_id',
            'Funktionsbezeichnung': 'name',
            'Sortierfolge': 'order'
        })
        existing_roles = RoleType.objects.all().values_list('legacy_id', flat=True)
        new_roles = []

        for f in funktionstypen:
            if f['legacy_id'] in existing_roles:
                continue
            r = RoleType()
            for k, v in f.items():
                setattr(r, k, v)
            new_roles.append(r)

        if new_roles:
            print "Import %d Funktionstypen" % len(new_roles)
            RoleType.objects.bulk_create(new_roles)

    def import_funktionen(self):
        funktionen = self.funktionen.map({
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
        new_funktionen = []

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

            role = Role(
                member_id=member_mapping[f['member_id']],
                department_id=department_id,
                type_id=role_type_mapping[f['role_type_id']],
                start=f['start'],
                end=f['end'],
                legacy_id=f['legacy_id']
            )
            new_funktionen.append(role)

        if new_funktionen:
            print "Import %d Funktionen" % len(new_funktionen)
            Role.objects.bulk_create(new_funktionen)

    def import_ausbildungstypen(self):
        ausbildungstypen = self.ausbildungstypen.map({
            'Ausbildungstypnummer': 'legacy_id',
            'Ausbildungsname': 'title',
            'Sortierfolge': 'order',
        })
        existing_education_types = EducationType.objects.all().values_list(
            'legacy_id', flat=True)
        new_ausbildungstypen = []

        for a in ausbildungstypen:
            if a['legacy_id'] in existing_education_types:
                continue
            e = EducationType()
            for k, v in a.items():
                setattr(e, k, v)
            new_ausbildungstypen.append(e)

        if new_ausbildungstypen:
            print "Import %d Ausbildungstypen" % len(new_ausbildungstypen)
            EducationType.objects.bulk_create(new_ausbildungstypen)

    def import_ausbildungen(self):
        ausbildungen = self.ausbildungen.map({
            'Ausbildungsnummer': 'legacy_id',
            'Ref zur Person': 'member_legacy_id',
            'Ausbildungstyp': 'education_type_legacy_id',
            'Beginn': 'date'
        })
        member_mapping = dict(Member.objects.all().values_list('legacy_id', 'id'))
        education_type_mapping = dict(
            EducationType.objects.all().values_list('legacy_id', 'id')
        )
        existing_educations = Education.objects.all().values_list(
            'legacy_id', flat=True)
        new_ausbildungen = []

        for a in ausbildungen:
            if a['legacy_id'] in existing_educations:
                continue
            if not a['date']:
                a['date'] = None
            e = Education(
                member_id=member_mapping[a['member_legacy_id']],
                type_id=education_type_mapping[a['education_type_legacy_id']],
                date=a['date'],
                legacy_id=a['legacy_id']
            )
            new_ausbildungen.append(e)

        if new_ausbildungen:
            print "Import %d Ausbildungen" % len(new_ausbildungen)
            Education.objects.bulk_create(new_ausbildungen)

    def department_mapping(self):
        return dict(Department.objects.all().values_list('legacy_id', 'id'))

    def mptt_dummy(self, obj):
        obj.lft = 0
        obj.rght = 0
        obj.level = 0
        obj.tree_id = 0
