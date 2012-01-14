# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UprawnienieRegistryHistory'
        db.create_table('registry_uprawnienieregistryhistory', (
            ('save_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uprawnienie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['registry.Dictionary'])),
            ('rozkaz', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('srodowisko', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['registry.Dictionary'])),
            ('parent_instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', to=orm['registry.UprawnienieRegistry'])),
        ))
        db.send_create_signal('registry', ['UprawnienieRegistryHistory'])

        # Adding model 'UprawnienieRegistry'
        db.create_table('registry_uprawnienieregistry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uprawnienie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['registry.Dictionary'])),
            ('rozkaz', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('srodowisko', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['registry.Dictionary'])),
        ))
        db.send_create_signal('registry', ['UprawnienieRegistry'])


    def backwards(self, orm):
        
        # Deleting model 'UprawnienieRegistryHistory'
        db.delete_table('registry_uprawnienieregistryhistory')

        # Deleting model 'UprawnienieRegistry'
        db.delete_table('registry_uprawnienieregistry')


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
            'troop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"})
        },
        'registry.scoutbookregistry': {
            'Meta': {'unique_together': "(('book_no',),)", 'object_name': 'ScoutBookRegistry'},
            'book_no': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'troop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"})
        },
        'registry.uprawnienieregistry': {
            'Meta': {'object_name': 'UprawnienieRegistry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'rozkaz': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uprawnienie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"})
        },
        'registry.uprawnienieregistryhistory': {
            'Meta': {'object_name': 'UprawnienieRegistryHistory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'parent_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['registry.UprawnienieRegistry']"}),
            'rozkaz': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'save_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'srodowisko': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['registry.Dictionary']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'uprawnienie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registry.Dictionary']"})
        }
    }

    complete_apps = ['registry']
