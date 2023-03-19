from __future__ import unicode_literals
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class comptes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    username = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=30, null=False)
    mail = models.CharField(max_length=30, null=False)
    def __str__(self):
        return self.username
