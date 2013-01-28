# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Publisher.default_interval'
        db.add_column('utils_publisher', 'default_interval',
                      self.gf('django.db.models.fields.CharField')(default=u'MONTHLY', max_length=55),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Publisher.default_interval'
        db.delete_column('utils_publisher', 'default_interval')


    models = {
        'utils.iatixmlsource': {
            'Meta': {'object_name': 'IATIXMLSource'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.Publisher']"}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'source_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'utils.parseschedule': {
            'Meta': {'object_name': 'ParseSchedule'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'iati_xml_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.IATIXMLSource']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.CharField', [], {'max_length': '55'})
        },
        'utils.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'default_interval': ('django.db.models.fields.CharField', [], {'default': "u'MONTHLY'", 'max_length': '55'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org_abbreviate': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['utils']