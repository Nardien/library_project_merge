# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class Book(models.Model):
    code = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=3, blank=True, null=True)
    due = models.TimeField(blank=True, null=True)
    cid = models.ForeignKey('Client', models.DO_NOTHING, db_column='Cid', blank=True, null=True)  # Field name made lowercase.
    lname = models.ForeignKey('Library', models.DO_NOTHING, db_column='Lname', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book'


class Client(models.Model):
    cid = models.CharField(db_column='CID', primary_key=True, max_length=6)  # Field name made lowercase.
    name = models.CharField(max_length=15)
    c_type = models.CharField(db_column='C_type', max_length=9)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'client'


class Library(models.Model):
    name = models.CharField(primary_key=True, max_length=15)
    location = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'library'


class SeminarRoom(models.Model):
    name = models.CharField(primary_key=True, max_length=10)
    lname = models.ForeignKey(Library, models.DO_NOTHING, db_column='Lname')  # Field name made lowercase.
    available_num = models.IntegerField(db_column='AVAILABLE_NUM')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seminar_room'


class SeminarUse(models.Model):
    cid = models.ForeignKey(Client, models.DO_NOTHING, db_column='Cid', primary_key=True)  # Field name made lowercase.
    rname = models.ForeignKey(SeminarRoom, models.DO_NOTHING, db_column='Rname')  # Field name made lowercase.
    date = models.DateField(db_column='DATE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seminar_use'
        unique_together = (('cid', 'rname'),)


class Staff(models.Model):
    sid = models.CharField(db_column='Sid', primary_key=True, max_length=6)  # Field name made lowercase.
    name = models.CharField(max_length=15)
    s_type = models.CharField(db_column='S_type', max_length=9)  # Field name made lowercase.
    phone_n = models.CharField(max_length=4)
    lname = models.ForeignKey(Library, models.DO_NOTHING, db_column='Lname')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'staff'

class Search(models.Model):
    name=models.CharField(max_length=50)
