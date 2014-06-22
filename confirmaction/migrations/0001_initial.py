# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'confirmaction_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('action_func', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('confirm_code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'confirmaction', ['Action'])

        # Adding model 'ActionArg'
        db.create_table(u'confirmaction_actionarg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='arg_set', to=orm['confirmaction.Action'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'confirmaction', ['ActionArg'])


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'confirmaction_action')

        # Deleting model 'ActionArg'
        db.delete_table(u'confirmaction_actionarg')


    models = {
        u'confirmaction.action': {
            'Meta': {'object_name': 'Action'},
            'action_func': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'confirm_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'confirmaction.actionarg': {
            'Meta': {'object_name': 'ActionArg'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'arg_set'", 'to': u"orm['confirmaction.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['confirmaction']