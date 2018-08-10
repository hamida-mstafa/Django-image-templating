# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home(request):
    a=1
    b=2
    c=3
    return render(request,'index.html',locals())
