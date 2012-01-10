# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dictionary'
        db.create_table('registry_dictionary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('registry', ['Dictionary'])

        # Adding model 'ScoutBookRegistry'
        db.create_table('registry_scoutbookregistry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('srodowisko', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['registry.Dictionary'])),
            ('troop', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['registry.Dictionary'])),
            ('book_no', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('issue_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('registry', ['ScoutBookRegistry'])

        # Adding model 'ScoutBookHistory'
        db.create_table('registry_scoutbookhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('save_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('srodowisko', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['registry.Dictionary'])),
            ('troop', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['registry.Dictionary'])),
            ('book_no', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('issue_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('parent_instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', to=orm['registry.ScoutBookRegistry'])),
        ))
        db.send_create_signal('registry', ['ScoutBookHistory'])


    def backwards(self, orm):
        
        # Deleting model 'Dictionary'
        db.delete_table('registry_dictionary')

        # Deleting model 'ScoutBookRegistry'
        db.delete_table('registry_scoutbookregistry')

        # Deleting model 'ScoutBookHistory'
        db.delete_table('registry_scoutbookhistory')


    models = {
        'registry.dictionary': {
            'Meta': {'object_name': 'Dictionary'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'Meta': {'object_name': 'ScoutBookRegistry'},
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
