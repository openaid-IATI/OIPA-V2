# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Population.slum_proportion'
        db.delete_column('data_population', 'slum_proportion')

        # Deleting field 'Population.slum_population'
        db.delete_column('data_population', 'slum_population')

        # Adding field 'Population.urban_slum_population'
        db.add_column('data_population', 'urban_slum_population',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.under_five_mortality_rate'
        db.add_column('data_population', 'under_five_mortality_rate',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.slum_proportion_living_urban'
        db.add_column('data_population', 'slum_proportion_living_urban',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.improved_water'
        db.add_column('data_population', 'improved_water',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.piped_water'
        db.add_column('data_population', 'piped_water',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.public_tap_pump_borehole'
        db.add_column('data_population', 'public_tap_pump_borehole',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.protected_well'
        db.add_column('data_population', 'protected_well',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.improved_spring_surface_water'
        db.add_column('data_population', 'improved_spring_surface_water',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.rainwater'
        db.add_column('data_population', 'rainwater',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.bottle_water'
        db.add_column('data_population', 'bottle_water',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.improved_toilet'
        db.add_column('data_population', 'improved_toilet',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.improved_flush_toilet'
        db.add_column('data_population', 'improved_flush_toilet',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.improved_pit_latrine'
        db.add_column('data_population', 'improved_pit_latrine',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.pit_latrine_with_slab_or_covered_latrine'
        db.add_column('data_population', 'pit_latrine_with_slab_or_covered_latrine',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.composting_toilet'
        db.add_column('data_population', 'composting_toilet',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.pit_latrine_without_slab'
        db.add_column('data_population', 'pit_latrine_without_slab',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.pump_borehole'
        db.add_column('data_population', 'pump_borehole',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Population.population'
        db.alter_column('data_population', 'population', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Adding field 'Population.slum_proportion'
        db.add_column('data_population', 'slum_proportion',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population.slum_population'
        db.add_column('data_population', 'slum_population',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Population.urban_slum_population'
        db.delete_column('data_population', 'urban_slum_population')

        # Deleting field 'Population.under_five_mortality_rate'
        db.delete_column('data_population', 'under_five_mortality_rate')

        # Deleting field 'Population.slum_proportion_living_urban'
        db.delete_column('data_population', 'slum_proportion_living_urban')

        # Deleting field 'Population.improved_water'
        db.delete_column('data_population', 'improved_water')

        # Deleting field 'Population.piped_water'
        db.delete_column('data_population', 'piped_water')

        # Deleting field 'Population.public_tap_pump_borehole'
        db.delete_column('data_population', 'public_tap_pump_borehole')

        # Deleting field 'Population.protected_well'
        db.delete_column('data_population', 'protected_well')

        # Deleting field 'Population.improved_spring_surface_water'
        db.delete_column('data_population', 'improved_spring_surface_water')

        # Deleting field 'Population.rainwater'
        db.delete_column('data_population', 'rainwater')

        # Deleting field 'Population.bottle_water'
        db.delete_column('data_population', 'bottle_water')

        # Deleting field 'Population.improved_toilet'
        db.delete_column('data_population', 'improved_toilet')

        # Deleting field 'Population.improved_flush_toilet'
        db.delete_column('data_population', 'improved_flush_toilet')

        # Deleting field 'Population.improved_pit_latrine'
        db.delete_column('data_population', 'improved_pit_latrine')

        # Deleting field 'Population.pit_latrine_with_slab_or_covered_latrine'
        db.delete_column('data_population', 'pit_latrine_with_slab_or_covered_latrine')

        # Deleting field 'Population.composting_toilet'
        db.delete_column('data_population', 'composting_toilet')

        # Deleting field 'Population.pit_latrine_without_slab'
        db.delete_column('data_population', 'pit_latrine_without_slab')

        # Deleting field 'Population.pump_borehole'
        db.delete_column('data_population', 'pump_borehole')


        # User chose to not deal with backwards NULL issues for 'Population.population'
        raise RuntimeError("Cannot reverse this migration. 'Population.population' and its values cannot be restored.")

    models = {
        'data.activitystatistics': {
            'Meta': {'object_name': 'ActivityStatistics'},
            'iati_identifier': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.IATIActivity']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'data.countrystatistics': {
            'Meta': {'object_name': 'CountryStatistics'},
            'country': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Country']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_activities': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'data.currencytype': {
            'Meta': {'object_name': 'CurrencyType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']", 'null': 'True', 'blank': 'True'})
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
            'date_updated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'default_aid_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.AidType']", 'null': 'True', 'blank': 'True'}),
            'default_finance_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FinanceType']", 'null': 'True', 'blank': 'True'}),
            'default_flow_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FlowType']", 'null': 'True', 'blank': 'True'}),
            'default_tied_status_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.TiedAidStatusType']", 'null': 'True', 'blank': 'True'}),
            'end_actual': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_planned': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'iati_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'format': ('django.db.models.fields.CharField', [], {'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.IATIActivity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Language']", 'null': 'True', 'blank': 'True'}),
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
            'iati_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sectors'", 'to': "orm['data.IATIActivity']"}),
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
        'data.organisationstatistics': {
            'Meta': {'object_name': 'OrganisationStatistics'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['data.Organisation']", 'unique': 'True'}),
            'total_activities': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        'data.population': {
            'Meta': {'object_name': 'Population'},
            'bottle_water': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'composting_toilet': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improved_flush_toilet': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'improved_pit_latrine': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'improved_spring_surface_water': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'improved_toilet': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'improved_water': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'piped_water': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pit_latrine_with_slab_or_covered_latrine': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pit_latrine_without_slab': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'protected_well': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'public_tap_pump_borehole': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pump_borehole': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rainwater': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'slum_proportion_living_urban': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'under_five_mortality_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'urban_slum_population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
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
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.CurrencyType']", 'null': 'True', 'blank': 'True'}),
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