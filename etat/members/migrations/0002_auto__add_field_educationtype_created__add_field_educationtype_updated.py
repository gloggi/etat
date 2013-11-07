# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EducationType.created'
        db.add_column(u'members_educationtype', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'EducationType.updated'
        db.add_column(u'members_educationtype', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'EducationType.legacy_id'
        db.add_column(u'members_educationtype', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Role.created'
        db.add_column(u'members_role', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Role.updated'
        db.add_column(u'members_role', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Role.legacy_id'
        db.add_column(u'members_role', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reachability.created'
        db.add_column(u'members_reachability', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Reachability.updated'
        db.add_column(u'members_reachability', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Reachability.legacy_id'
        db.add_column(u'members_reachability', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Education.created'
        db.add_column(u'members_education', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Education.updated'
        db.add_column(u'members_education', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Education.legacy_id'
        db.add_column(u'members_education', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Member.created'
        db.add_column(u'members_member', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Member.updated'
        db.add_column(u'members_member', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Member.legacy_id'
        db.add_column(u'members_member', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Address.created'
        db.add_column(u'members_address', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Address.updated'
        db.add_column(u'members_address', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Address.legacy_id'
        db.add_column(u'members_address', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'RoleType.created'
        db.add_column(u'members_roletype', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'RoleType.updated'
        db.add_column(u'members_roletype', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'RoleType.legacy_id'
        db.add_column(u'members_roletype', 'legacy_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EducationType.created'
        db.delete_column(u'members_educationtype', 'created')

        # Deleting field 'EducationType.updated'
        db.delete_column(u'members_educationtype', 'updated')

        # Deleting field 'EducationType.legacy_id'
        db.delete_column(u'members_educationtype', 'legacy_id')

        # Deleting field 'Role.created'
        db.delete_column(u'members_role', 'created')

        # Deleting field 'Role.updated'
        db.delete_column(u'members_role', 'updated')

        # Deleting field 'Role.legacy_id'
        db.delete_column(u'members_role', 'legacy_id')

        # Deleting field 'Reachability.created'
        db.delete_column(u'members_reachability', 'created')

        # Deleting field 'Reachability.updated'
        db.delete_column(u'members_reachability', 'updated')

        # Deleting field 'Reachability.legacy_id'
        db.delete_column(u'members_reachability', 'legacy_id')

        # Deleting field 'Education.created'
        db.delete_column(u'members_education', 'created')

        # Deleting field 'Education.updated'
        db.delete_column(u'members_education', 'updated')

        # Deleting field 'Education.legacy_id'
        db.delete_column(u'members_education', 'legacy_id')

        # Deleting field 'Member.created'
        db.delete_column(u'members_member', 'created')

        # Deleting field 'Member.updated'
        db.delete_column(u'members_member', 'updated')

        # Deleting field 'Member.legacy_id'
        db.delete_column(u'members_member', 'legacy_id')

        # Deleting field 'Address.created'
        db.delete_column(u'members_address', 'created')

        # Deleting field 'Address.updated'
        db.delete_column(u'members_address', 'updated')

        # Deleting field 'Address.legacy_id'
        db.delete_column(u'members_address', 'legacy_id')

        # Deleting field 'RoleType.created'
        db.delete_column(u'members_roletype', 'created')

        # Deleting field 'RoleType.updated'
        db.delete_column(u'members_roletype', 'updated')

        # Deleting field 'RoleType.legacy_id'
        db.delete_column(u'members_roletype', 'legacy_id')


    models = {
        u'departments.department': {
            'Meta': {'object_name': 'Department'},
            'default_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['members.RoleType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['departments.Department']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['departments.DepartmentType']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'departments.departmenttype': {
            'Meta': {'object_name': 'DepartmentType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'members.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'CH'", 'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': u"orm['members.Member']"}),
            'postal_code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'members.education': {
            'Meta': {'unique_together': "(('member', 'type'),)", 'object_name': 'Education'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'educations'", 'to': u"orm['members.Member']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.EducationType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'members.educationtype': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EducationType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'members.member': {
            'Meta': {'object_name': 'Member'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'members'", 'symmetrical': 'False', 'through': u"orm['members.Role']", 'to': u"orm['departments.Department']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'portrait': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'scout_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'members.reachability': {
            'Meta': {'object_name': 'Reachability'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reachabilities'", 'to': u"orm['members.Member']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'members.role': {
            'Meta': {'object_name': 'Role'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'department': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['departments.Department']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['members.Member']"}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.RoleType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'members.roletype': {
            'Meta': {'ordering': "('order',)", 'object_name': 'RoleType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['members']