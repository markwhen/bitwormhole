#from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mysite.models import *
from django.views.decorators.csrf import csrf_exempt
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
def hello(request):
    return HttpResponse("Hello world")
def homepage(request):
    return HttpResponse("My Home Page")
def hours_ahead(request, name):
    try:
        name = str(name)
    except ValueError:
        raise Http404()
    html = "<html><body>It is %s.</body></html>" % name
    return HttpResponse(html)
def group(request):
    info = userlist.objects.all()
    return HttpResponse(info)
def aboutme(request):
    return render_to_response('aboutme.html',{'words':'Nice to meet every day','static_file_url':'http://static.bitwormhole.com/static/'})
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        content = request.FILES['file1']
        if content.size > 9000000:
            return render_to_response('upload.html', {"notice":"Your file is larger than 9MB. Upload failed.",'static_file_url':'http://static.bitwormhole.com/static/','domain_url':'http://bitwormhole.com/'})
        if content.size < 1:
            return render_to_response('upload.html', {"notice":"Your file is too small. Upload failed.",'static_file_url':'http://static.bitwormhole.com/static/','domain_url':'http://bitwormhole.com/'})
        from os import environ
        online = environ.get("APP_NAME", "")
        if online:
            import sae.const  
            access_key = sae.const.ACCESS_KEY  
            secret_key = sae.const.SECRET_KEY  
            appname = sae.const.APP_NAME  
            domain_name = "mfile"
            import sae.storage  
            s = sae.storage.Client()  
            ob = sae.storage.Object(content.read())
            url = s.put(domain_name, content.name, ob)
            return render_to_response('upload.html', {"notice":url,'static_file_url':'http://static.bitwormhole.com/static/','domain_url':'http://bitwormhole.com/'})
        else:
            return render_to_response('upload.html', {"notice":"save failed",'static_file_url':'http://static.bitwormhole.com/static/','domain_url':'http://bitwormhole.com/'}) 
    else:
        return render_to_response('upload.html',{'notice':'URLs will show here','static_file_url':'http://static.bitwormhole.com/static/','domain_url':'http://bitwormhole.com/'})
