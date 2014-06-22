# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Action.user_contact'
        db.add_column(u'confirmaction_action', 'user_contact',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Action.user_contact'
        db.delete_column(u'confirmaction_action', 'user_contact')


    models = {
        u'confirmaction.action': {
            'Meta': {'object_name': 'Action'},
            'action_func': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'action_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'confirm_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'executed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_contact': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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