# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DatasetSync'
        db.create_table('utils_datasetsync', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interval', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('utils', ['DatasetSync'])


    def backwards(self, orm):
        # Deleting model 'DatasetSync'
        db.delete_table('utils_datasetsync')


    models = {
        'utils.conversationcitynames': {
            'Meta': {'object_name': 'ConversationCityNames'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unusable_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'usable_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.datasetsync': {
            'Meta': {'object_name': 'DatasetSync'},
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'utils.iatixmlsource': {
            'Meta': {'ordering': "['ref']", 'object_name': 'IATIXMLSource'},
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
            'Meta': {'ordering': "['org_name']", 'object_name': 'Publisher'},
            'default_interval': ('django.db.models.fields.CharField', [], {'default': "u'MONTHLY'", 'max_length': '55'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org_abbreviate': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'utils.unhabitatparserlog': {
            'Meta': {'object_name': 'UnHabitatParserLog'},
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_errors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_processed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type_upload': ('django.db.models.fields.IntegerField', [], {})
        },
        'utils.unhabitatrecordlog': {
            'Meta': {'object_name': 'UnhabitatRecordLog'},
            'city_input_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city_success': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country_input_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country_iso': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country_success': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['utils.UnHabitatParserLog']"}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['utils']