from django.shortcuts import redirect, render
from django.template import loader

from FTPManager import FTPManager
import logging
from django.http import HttpResponse

from .models import Site
from bs4 import BeautifulSoup
import html

logger = logging.getLogger(__name__)

###
### HOME
###

def home(request):
    return render(request, 'home.html')

###
### WEBSITES
###

def websites_connect(request):
    host = request.POST['host']
    port = request.POST['port']
    username = request.POST['username']
    pwd = request.POST['pwd']

    # todo: ftp test, redirect back if it fails

    try:
        site = Site.objects.get(ftp_host=host, ftp_user=username)
    except Site.DoesNotExist:
        return redirect('home')
        # todo: create a website

    request.session['pwd'] = pwd

    return redirect('pages_index', website_id=site.id)

###
### PAGES
###

def izi_edit(request):
    """Handle requests from the bookmarklet"""
    # todo: retrieve a Site model from url parameter
    # todo: magic to get the page
    return HttpResponse(request.GET.get('url', 'no url provided'))

def pages_index(request, website_id):
    site = Site.objects.get(id=website_id)

    return render(request, 'pages/index.html', {
            'site':site,
            'pages':site.page_set.all()
        })

def pages_edit(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.session['pwd']
    file = FTPManager.download(site.ftp_host, site.ftp_port, site.ftp_user, pwd, "", page.path)

    soup = BeautifulSoup(file, "html.parser")
    tag = soup.find(id="iziEdit")
    template = loader.get_template('pages/edit.html')

    return render(request, 'pages/edit.html', {'site':site,'page':page, 'file':file, 'tag':str(tag)})

def pages_add(request, website_id):
    site = Site.objects.get(id=website_id)
    return render(request, 'pages/add.html', {'site':site})

def pages_update(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.session['pwd']
    pageContent = request.POST['pageContent']
    editContent = request.POST['editContent']

    soup = BeautifulSoup(pageContent, "html.parser")

    newDiv = soup.new_tag('div')
    newDiv['id'] = 'iziEdit'
    newDiv.string = editContent

    soup.find(id="iziEdit").replace_with(newDiv)

    FTPManager.upload(site.ftp_host, site.ftp_port, site.ftp_user, pwd, "", page.path, html.unescape(str(soup)))

    return redirect('pages_index', website_id=site.id)

###
### OTHER
###
