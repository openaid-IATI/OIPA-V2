# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organisation'
        db.create_table('data_organisation', (
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=25, primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('org_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('org_name_lang', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('data', ['Organisation'])

        # Adding model 'ParticipatingOrganisation'
        db.create_table('data_participatingorganisation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('org_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('org_name_lang', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('data', ['ParticipatingOrganisation'])

        # Adding model 'Language'
        db.create_table('data_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=55)),
        ))
        db.send_create_signal('data', ['Language'])

        # Adding model 'Country'
        db.create_table('data_country', (
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
        ))
        db.send_create_signal('data', ['Country'])

        # Adding model 'Region'
        db.create_table('data_region', (
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('data', ['Region'])

        # Adding model 'VocabularyType'
        db.create_table('data_vocabularytype', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=15, primary_key=True)),
        ))
        db.send_create_signal('data', ['VocabularyType'])

        # Adding model 'SignificanceType'
        db.create_table('data_significancetype', (
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('data', ['SignificanceType'])

        # Adding model 'CollaborationType'
        db.create_table('data_collaborationtype', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=55, primary_key=True)),
        ))
        db.send_create_signal('data', ['CollaborationType'])

        # Adding model 'FlowType'
        db.create_table('data_flowtype', (
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('data', ['FlowType'])

        # Adding model 'FinanceType'
        db.create_table('data_financetype', (
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('data', ['FinanceType'])

        # Adding model 'AidType'
        db.create_table('data_aidtype', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('data', ['AidType'])

        # Adding model 'TiedAidStatusType'
        db.create_table('data_tiedaidstatustype', (
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5, primary_key=True)),
        ))
        db.send_create_signal('data', ['TiedAidStatusType'])

        # Adding model 'CurrencyType'
        db.create_table('data_currencytype', (
            ('code', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Country'], null=True, blank=True)),
        ))
        db.send_create_signal('data', ['CurrencyType'])

        # Adding model 'ActivityStatusType'
        db.create_table('data_activitystatustype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=8, unique=True, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Country'], null=True, blank=True)),
        ))
        db.send_create_signal('data', ['ActivityStatusType'])

        # Adding model 'Budget'
        db.create_table('data_budget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('period_start', self.gf('django.db.models.fields.DateField')()),
            ('period_end', self.gf('django.db.models.fields.DateField')()),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.CurrencyType'], null=True, blank=True)),
        ))
        db.send_create_signal('data', ['Budget'])

        # Adding model 'Transaction'
        db.create_table('data_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('provider_org', self.gf('django.db.models.fields.related.ForeignKey')(related_name='provider_org', to=orm['data.Organisation'])),
            ('receiver_org', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='receiver_org', null=True, to=orm['data.Organisation'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('value_date', self.gf('django.db.models.fields.DateField')()),
            ('transaction_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('flow_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FlowType'], null=True, blank=True)),
            ('finance_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FinanceType'], null=True, blank=True)),
            ('aid_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.AidType'], null=True, blank=True)),
            ('disbursement_channel', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tied_aid_status_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('data', ['Transaction'])

        # Adding model 'IATIActivity'
        db.create_table('data_iatiactivity', (
            ('iati_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('reporting_organisation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Organisation'])),
            ('activity_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ActivityStatusType'], null=True, blank=True)),
            ('start_planned', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('start_actual', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_planned', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_actual', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('collaboration_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.CollaborationType'], null=True, blank=True)),
            ('default_flow_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FlowType'], null=True, blank=True)),
            ('default_aid_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.AidType'], null=True, blank=True)),
            ('default_finance_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FinanceType'], null=True, blank=True)),
            ('default_tied_status_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.TiedAidStatusType'], null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('data', ['IATIActivity'])

        # Adding model 'IATIActivityTitle'
        db.create_table('data_iatiactivitytitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Language'], null=True, blank=True)),
        ))
        db.send_create_signal('data', ['IATIActivityTitle'])

        # Adding model 'IATIActivityDescription'
        db.create_table('data_iatiactivitydescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Language'], null=True, blank=True)),
        ))
        db.send_create_signal('data', ['IATIActivityDescription'])

        # Adding model 'IATIActivityRegion'
        db.create_table('data_iatiactivityregion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Region'])),
            ('percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('data', ['IATIActivityRegion'])

        # Adding model 'IATIActivityCountry'
        db.create_table('data_iatiactivitycountry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Country'])),
            ('percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('data', ['IATIActivityCountry'])

        # Adding model 'IATIActivitySector'
        db.create_table('data_iatiactivitysector', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('vocabulary_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.VocabularyType'], null=True, blank=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('data', ['IATIActivitySector'])

        # Adding model 'IATITransaction'
        db.create_table('data_iatitransaction', (
            ('transaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['data.Transaction'], unique=True, primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
        ))
        db.send_create_signal('data', ['IATITransaction'])

        # Adding model 'IATIActivityBudget'
        db.create_table('data_iatiactivitybudget', (
            ('budget_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['data.Budget'], unique=True, primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
        ))
        db.send_create_signal('data', ['IATIActivityBudget'])

        # Adding model 'PlannedDisbursement'
        db.create_table('data_planneddisbursement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('period_start', self.gf('django.db.models.fields.DateField')()),
            ('period_end', self.gf('django.db.models.fields.DateField')()),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.CurrencyType'])),
        ))
        db.send_create_signal('data', ['PlannedDisbursement'])

        # Adding model 'IATIActivityContact'
        db.create_table('data_iatiactivitycontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('mailing_address', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
        ))
        db.send_create_signal('data', ['IATIActivityContact'])

        # Adding model 'IATIActivityDocument'
        db.create_table('data_iatiactivitydocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Language'])),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
        ))
        db.send_create_signal('data', ['IATIActivityDocument'])

        # Adding model 'IATIActivityWebsite'
        db.create_table('data_iatiactivitywebsite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
        ))
        db.send_create_signal('data', ['IATIActivityWebsite'])

        # Adding model 'IATIActivityPolicyMarker'
        db.create_table('data_iatiactivitypolicymarker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iati_activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.IATIActivity'])),
            ('code', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('vocabulary_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.VocabularyType'], null=True, blank=True)),
            ('significance_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.SignificanceType'], null=True, blank=True)),
        ))
        db.send_create_signal('data', ['IATIActivityPolicyMarker'])


    def backwards(self, orm):
        # Deleting model 'Organisation'
        db.delete_table('data_organisation')

        # Deleting model 'ParticipatingOrganisation'
        db.delete_table('data_participatingorganisation')

        # Deleting model 'Language'
        db.delete_table('data_language')

        # Deleting model 'Country'
        db.delete_table('data_country')

        # Deleting model 'Region'
        db.delete_table('data_region')

        # Deleting model 'VocabularyType'
        db.delete_table('data_vocabularytype')

        # Deleting model 'SignificanceType'
        db.delete_table('data_significancetype')

        # Deleting model 'CollaborationType'
        db.delete_table('data_collaborationtype')

        # Deleting model 'FlowType'
        db.delete_table('data_flowtype')

        # Deleting model 'FinanceType'
        db.delete_table('data_financetype')

        # Deleting model 'AidType'
        db.delete_table('data_aidtype')

        # Deleting model 'TiedAidStatusType'
        db.delete_table('data_tiedaidstatustype')

        # Deleting model 'CurrencyType'
        db.delete_table('data_currencytype')

        # Deleting model 'ActivityStatusType'
        db.delete_table('data_activitystatustype')

        # Deleting model 'Budget'
        db.delete_table('data_budget')

        # Deleting model 'Transaction'
        db.delete_table('data_transaction')

        # Deleting model 'IATIActivity'
        db.delete_table('data_iatiactivity')

        # Deleting model 'IATIActivityTitle'
        db.delete_table('data_iatiactivitytitle')

        # Deleting model 'IATIActivityDescription'
        db.delete_table('data_iatiactivitydescription')

        # Deleting model 'IATIActivityRegion'
        db.delete_table('data_iatiactivityregion')

        # Deleting model 'IATIActivityCountry'
        db.delete_table('data_iatiactivitycountry')

        # Deleting model 'IATIActivitySector'
        db.delete_table('data_iatiactivitysector')

        # Deleting model 'IATITransaction'
        db.delete_table('data_iatitransaction')

        # Deleting model 'IATIActivityBudget'
        db.delete_table('data_iatiactivitybudget')

        # Deleting model 'PlannedDisbursement'
        db.delete_table('data_planneddisbursement')

        # Deleting model 'IATIActivityContact'
        db.delete_table('data_iatiactivitycontact')

        # Deleting model 'IATIActivityDocument'
        db.delete_table('data_iatiactivitydocument')

        # Deleting model 'IATIActivityWebsite'
        db.delete_table('data_iatiactivitywebsite')

        # Deleting model 'IATIActivityPolicyMarker'
        db.delete_table('data_iatiactivitypolicymarker')


    models = {
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vocabulary_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.VocabularyType']", 'null': 'True', 'blank': 'True'})
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