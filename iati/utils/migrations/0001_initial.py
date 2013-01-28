# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Publisher'
        db.create_table('utils_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('org_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('org_abbreviate', self.gf('django.db.models.fields.CharField')(max_length=55, null=True, blank=True)),
        ))
        db.send_create_signal('utils', ['Publisher'])

        # Adding model 'IATIXMLSource'
        db.create_table('utils_iatixmlsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['utils.Publisher'])),
            ('local_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('utils', ['IATIXMLSource'])


    def backwards(self, orm):
        # Deleting model 'Publisher'
        db.delete_table('utils_publisher')

        # Deleting model 'IATIXMLSource'
        db.delete_table('utils_iatixmlsource')


    models = {
        'utils.iatixmlsource': {
            'Meta': {'object_name': 'IATIXMLSource'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Publisher']"}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'source_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'utils.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org_abbreviate': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['utils']