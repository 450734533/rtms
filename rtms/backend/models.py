# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import hashlib
import time

from django.conf import settings
from django.db import models
from djcelery.models import PeriodicTask


class Case(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, null=True, blank=True)
    header = models.CharField(max_length=255, null=True, blank=True)
    boby = models.CharField(max_length=10000, null=True, blank=True)
    cookies = models.CharField(max_length=255, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    expect = models.CharField(max_length=100, null=True, blank=True)
    retId = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Case'
        verbose_name_plural = verbose_name


class Result(models.Model):
    caseId = models.IntegerField(default=10)
    resultall = models.CharField(max_length=1000, null=True)
    resultId = models.CharField(max_length=50, null=True)
    ret = models.CharField(max_length=50, null=True)


class Flow(models.Model):
    name = models.CharField(max_length=50)
    cards = models.CharField(max_length=10000, null=True, blank=True)
    flowRemark = models.CharField(max_length=100, null=True, blank=True)


class Suite(models.Model):
    casesuite = models.CharField(max_length=50, null=True)
    flowId = models.IntegerField(default=10)


class Auth(models.Model):
    auths = models.CharField(max_length=1000, null=True, blank=True)
    authCase = models.CharField(max_length=100, null=True, blank=True)


def upload_to(instance, filename):
    m = hashlib.md5()
    m.update(str(instance.id) + str(time.time()))
    md5_path = os.path.join(os.path.join(settings.JAR_PATH, str(instance.id)), m.hexdigest())
    return os.path.join(md5_path, filename)


class AuthScript1(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    auth_jar = models.CharField(max_length=1000, null=True, blank=True)


class Plan(models.Model):
    name = models.CharField(max_length=20)
    flag = models.CharField(max_length=10)
    execute_time = models.CharField(max_length=200, null=True, blank=True)
    frikcy = models.IntegerField(default=10)
    cases_id = models.CharField(max_length=100)
    switch = models.BooleanField(default=True)
    create_time = models.CharField(max_length=200, null=True, blank=True)
    period = models.ForeignKey(PeriodicTask, verbose_name="PeriodicTask", null=True, on_delete=models.SET_NULL)





