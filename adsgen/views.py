# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home(request):
    last=request.GET.get("last") or "0xDEADBEEF"
    return render(request,'index.html',locals())
