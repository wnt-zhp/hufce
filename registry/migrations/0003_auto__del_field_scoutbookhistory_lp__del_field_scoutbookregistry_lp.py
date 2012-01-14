# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ScoutBookHistory.lp'
        db.delete_column('registry_scoutbookhistory', 'lp')

        # Deleting field 'ScoutBookRegistry.lp'
        db.delete_column('registry_scoutbookregistry', 'lp')


    def backwards(self, orm):
        
        # Adding field 'ScoutBookHistory.lp'
        db.add_column('registry_scoutbookhistory', 'lp', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'ScoutBookRegistry.lp'
        db.add_column('registry_scoutbookregistry', 'lp', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True), keep_default=False)


    models = {
        'registry.dictionary': {
            'Meta': {'object_name': 'Dictionary'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'registry.scoutbookhistory': {
            'Meta': {'object_name': 'ScoutBookHistory'},
            'book_no': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'parent_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['registry.ScoutBookRegistry']"}),
            'save_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'troop': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"})
        },
        'registry.scoutbookregistry': {
            'Meta': {'unique_together': "(('book_no',),)", 'object_name': 'ScoutBookRegistry'},
            'book_no': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'troop': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"})
        }
    }

    complete_apps = ['registry']
