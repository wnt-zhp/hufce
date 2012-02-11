# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'HistoricalUprawnienie.date'
        db.add_column('registry_historicaluprawnienie', 'date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 2, 11), blank=True), keep_default=False)

        # Adding field 'Uprawnienie.date'
        db.add_column('registry_uprawnienie', 'date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 2, 11), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'HistoricalUprawnienie.date'
        db.delete_column('registry_historicaluprawnienie', 'date')

        # Deleting field 'Uprawnienie.date'
        db.delete_column('registry_uprawnienie', 'date')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'registry.adress': {
            'Meta': {'object_name': 'Adress'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'registry.corresponcence': {
            'Meta': {'object_name': 'Corresponcence'},
            'adress': ('historical.models.HistoricalForeignKey', [], {'to': "orm['registry.Adress']"}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'institution_no': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"}),
            'subject': ('django.db.models.fields.TextField', [], {})
        },
        'registry.dictionary': {
            'Meta': {'object_name': 'Dictionary'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'registry.historicaladress': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalAdress'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_adress_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['registry.Adress']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'no': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'registry.historicalcorresponcence': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalCorresponcence'},
            'adress': ('historical.models.KeyToHistoryMarker', [], {'to': "orm['registry.HistoricalAdress']"}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'data': ('django.db.models.fields.DateField', [], {}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_corresponcence_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'institution_no': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['registry.Corresponcence']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"}),
            'subject': ('django.db.models.fields.TextField', [], {})
        },
        'registry.historicalscoutbook': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalScoutBook'},
            'book_no': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_scoutbook_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['registry.ScoutBook']"}),
            'issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'troop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"})
        },
        'registry.historicaluprawnienie': {
            'Meta': {'ordering': "('-history_date',)", 'object_name': 'HistoricalUprawnienie'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'history_user': ('current_user.models.CurrentUserField', [], {'related_name': "'_uprawnienie_history'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['registry.Uprawnienie']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'rozkaz': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uprawnienie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"})
        },
        'registry.scoutbook': {
            'Meta': {'ordering': "['id']", 'object_name': 'ScoutBook'},
            'book_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'troop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"})
        },
        'registry.uprawnienie': {
            'Meta': {'ordering': "['id']", 'object_name': 'Uprawnienie'},
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'rozkaz': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uprawnienie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"})
        }
    }

    complete_apps = ['registry']
