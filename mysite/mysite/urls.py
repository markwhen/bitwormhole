from django.conf.urls import patterns, include, url
from mysite.views import *#import the view package
from mysite.bitwormhole.views import *
from settings import TEMPLATE_DIRS,STATICFILES_DIRS
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #('^hello/$', hello),#hello world
    #('^time$',current_datetime),#show datetime
    #(r'^(\d{1,2})/$', hours_ahead),
    #('^group/$',group),
    #('^upload/$',upload),
    ('^aboutme/$', aboutme),
    #(r'^static','django.views.static.serve',
    #    {'document_root':STATICFILES_DIRS, 'show_indexes': True}),
    #(r'^static/(?P<path>.*)$','django.views.static.serve',
    #    {'document_root':STATICFILES_DIRS, 'show_indexes': True}),
    ('^$',bindex),#homepage
    ('^/*',bfound),#bitwormhole
    #(r'^js/(?P<path>.*)$','django.views.static.serve',
    #                     {'document_root':TEMPLATE_DIRS[0]+'/js'}),
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
