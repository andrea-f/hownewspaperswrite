from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import os
import sys
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import socket
from django.template import Library
from GeneralStatistics import GeneralDataView

def home(request):
    """Home view for Hownewspapers write app."""
    return render_to_response('home.html', locals(), RequestContext(request))

def statistiche_generali(request):
    """Returns aggregated information on data present in database."""
    gdw = GeneralDataView()
    response = gdw.fetch(request)
    return response

def testate(request):
    """Returns newspaper specific information."""
