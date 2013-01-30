# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SlumParserLog'
        db.create_table('utils_slumparserlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_file', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slum_population_diff', self.gf('django.db.models.fields.IntegerField')()),
            ('slum_proportion_diff', self.gf('django.db.models.fields.FloatField')()),
            ('population_diff', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slum_proportion', self.gf('django.db.models.fields.FloatField')()),
            ('slum_population', self.gf('django.db.models.fields.IntegerField')()),
            ('population', self.gf('django.db.models.fields.IntegerField')()),
            ('country_iso', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('utils', ['SlumParserLog'])

        # Adding model 'CountryToIsoLog'
        db.create_table('utils_countrytoisolog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_iso', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('utils', ['CountryToIsoLog'])


    def backwards(self, orm):
        # Deleting model 'SlumParserLog'
        db.delete_table('utils_slumparserlog')

        # Deleting model 'CountryToIsoLog'
        db.delete_table('utils_countrytoisolog')


    models = {
        'utils.countrytoisolog': {
            'Meta': {'object_name': 'CountryToIsoLog'},
            'country_iso': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        'utils.slumparserlog': {
            'Meta': {'object_name': 'SlumParserLog'},
            'country_iso': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'csv_file': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'population_diff': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slum_population': ('django.db.models.fields.IntegerField', [], {}),
            'slum_population_diff': ('django.db.models.fields.IntegerField', [], {}),
            'slum_proportion': ('django.db.models.fields.FloatField', [], {}),
            'slum_proportion_diff': ('django.db.models.fields.FloatField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['utils']