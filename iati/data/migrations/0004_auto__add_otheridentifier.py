# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OtherIdentifier'
        db.create_table('data_otheridentifier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('owner_ref', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('owner_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('data', ['OtherIdentifier'])


    def backwards(self, orm):
        # Deleting model 'OtherIdentifier'
        db.delete_table('data_otheridentifier')


    models = {
        'data.activitystatistics': {
            'Meta': {'object_name': 'ActivityStatistics'},
            'iati_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'total_budget': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '2', 'blank': 'True'})
        },
        'data.activitystatustype': {
            'Meta': {'object_name': 'ActivityStatusType'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']", 'null': 'True', 'blank': 'True'})
        },
        'data.aidtype': {
            'Meta': {'object_name': 'AidType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        'data.budget': {
            'Meta': {'object_name': 'Budget'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.CurrencyType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_end': ('django.db.models.fields.DateField', [], {}),
            'period_start': ('django.db.models.fields.DateField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'})
        },
        'data.collaborationtype': {
            'Meta': {'object_name': 'CollaborationType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '55', 'primary_key': 'True'})
        },
        'data.country': {
            'Meta': {'object_name': 'Country'},
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'})
        },
        'data.currencytype': {
            'Meta': {'object_name': 'CurrencyType'},
            'code': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'data.financetype': {
            'Meta': {'object_name': 'FinanceType'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        'data.flowtype': {
            'Meta': {'object_name': 'FlowType'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        'data.iatiactivity': {
            'Meta': {'object_name': 'IATIActivity'},
            'activity_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ActivityStatusType']", 'null': 'True', 'blank': 'True'}),
            'collaboration_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.CollaborationType']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {}),
            'default_aid_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.AidType']", 'null': 'True', 'blank': 'True'}),
            'default_finance_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FinanceType']", 'null': 'True', 'blank': 'True'}),
            'default_flow_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FlowType']", 'null': 'True', 'blank': 'True'}),
            'default_tied_status_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.TiedAidStatusType']", 'null': 'True', 'blank': 'True'}),
            'end_actual': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_planned': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'iati_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'reporting_organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Organisation']"}),
            'start_actual': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'start_planned': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'data.iatiactivitybudget': {
            'Meta': {'object_name': 'IATIActivityBudget', '_ormbases': ['data.Budget']},
            'budget_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Budget']", 'unique': 'True', 'primary_key': 'True'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"})
        },
        'data.iatiactivitycontact': {
            'Meta': {'object_name': 'IATIActivityContact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'data.iatiactivitycountry': {
            'Meta': {'object_name': 'IATIActivityCountry'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']"}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'data.iatiactivitydescription': {
            'Meta': {'object_name': 'IATIActivityDescription'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Language']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'data.iatiactivitydocument': {
            'Meta': {'object_name': 'IATIActivityDocument'},
            'format': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Language']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'data.iatiactivitypolicymarker': {
            'Meta': {'object_name': 'IATIActivityPolicyMarker'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'significance_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.SignificanceType']", 'null': 'True', 'blank': 'True'}),
            'vocabulary_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.VocabularyType']", 'null': 'True', 'blank': 'True'})
        },
        'data.iatiactivityregion': {
            'Meta': {'object_name': 'IATIActivityRegion'},
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Region']"})
        },
        'data.iatiactivitysector': {
            'Meta': {'object_name': 'IATIActivitySector'},
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Sector']"})
        },
        'data.iatiactivitytitle': {
            'Meta': {'object_name': 'IATIActivityTitle'},
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Language']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.iatiactivitywebsite': {
            'Meta': {'object_name': 'IATIActivityWebsite'},
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'data.iatitransaction': {
            'Meta': {'object_name': 'IATITransaction', '_ormbases': ['data.Transaction']},
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'transaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Transaction']", 'unique': 'True', 'primary_key': 'True'})
        },
        'data.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'org_name_lang': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'data.otheridentifier': {
            'Meta': {'object_name': 'OtherIdentifier'},
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner_ref': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.participatingorganisation': {
            'Meta': {'object_name': 'ParticipatingOrganisation'},
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'org_name_lang': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'data.planneddisbursement': {
            'Meta': {'object_name': 'PlannedDisbursement'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.CurrencyType']"}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_end': ('django.db.models.fields.DateField', [], {}),
            'period_start': ('django.db.models.fields.DateField', [], {})
        },
        'data.region': {
            'Meta': {'object_name': 'Region'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        'data.sector': {
            'Meta': {'object_name': 'Sector'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '55', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vocabulary_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.VocabularyType']", 'null': 'True', 'blank': 'True'})
        },
        'data.significancetype': {
            'Meta': {'object_name': 'SignificanceType'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        'data.tiedaidstatustype': {
            'Meta': {'object_name': 'TiedAidStatusType'},
            'code': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'primary_key': 'True'})
        },
        'data.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'aid_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.AidType']", 'null': 'True', 'blank': 'True'}),
            'disbursement_channel': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'finance_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FinanceType']", 'null': 'True', 'blank': 'True'}),
            'flow_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FlowType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider_org': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'provider_org'", 'to': "orm['data.Organisation']"}),
            'receiver_org': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'receiver_org'", 'null': 'True', 'to': "orm['data.Organisation']"}),
            'tied_aid_status_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'value_date': ('django.db.models.fields.DateField', [], {})
        },
        'data.vocabularytype': {
            'Meta': {'object_name': 'VocabularyType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'})
        }
    }

    complete_apps = ['data']