# -*- coding: utf-8 -*-
#from django.template import Template, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from mysite.bitwormhole.models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
import sys
import os
import re #regular expression
#bitwormhole is below
@csrf_exempt
def bfound(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')# to prevent UnicodeEncodeError
    size_limit = 1000
    domain_url = "http://bitwormhole.com/"
    download_domain = "http://res.bitwormhole.com/"
    static_file_url = "http://static.bitwormhole.com/static/"
    storage_path = "/home/pi/storage/mysite-download/"
    user_ip = request.META['REMOTE_ADDR']
    current_path = request.get_full_path()
    current_path = current_path.decode('utf-8')
    re_url_filter = re.compile(u'[_0-9a-zA-Z\u4e00-\u9fa5]*')
    current_path_ls = re_url_filter.findall(current_path)
    is_founder = False
    if current_path_ls:
        current_path = ""
        for sub in current_path_ls:
            current_path = current_path + sub
    if len(current_path)<1:
        return HttpResponse("Sorry,the bitwormhole name is not correct")

    if request.method == 'GET':
        #search for file on disk
        #downloadlist = []
        #file_storage_dir = storage_path+current_path
        #if os.path.exists(file_storage_dir.encode('utf-8')):
        #    listdir = os.listdir(file_storage_dir.encode('utf-8'))
        #    i = 0
        #    for filename in listdir:
        #        download_link = download_domain + current_path +u'/'+ filename
        #        downloadlist.append({'id':str(i),'name':str(filename),'link':download_link,'add':'没有备注'})
        #        i = i+1
        #search end
        head_info = u"欢迎造访虫洞"
        #database 
        downloadlist = []
        try:
            bname1 = BName.objects.get(name = current_path)
            #begin get filelist
            try:
                bfilelist = BFile.objects.filter(bname=bname1)
                for bfile_in_list in bfilelist:
                    if not bfile_in_list.key:
                        download_link = download_domain + current_path +u'/'+bfile_in_list.filename
                        downloadlist.append({'id':str(bfile_in_list.id),
                            'name':bfile_in_list.filename,
                            'time':bfile_in_list.datetime,
                            'link':download_link,
                            'add':bfile_in_list.add,
                            'like':bfile_in_list.like})
                    else:
                        download_link = download_domain + current_path+u'/'+bfile_in_list.filename
                        downloadlist.append({'id':str(bfile_in_list.id),
                            'name':bfile_in_list.filename,
                            'time':bfile_in_list.datetime,
                            'need_key':True,
                            'link':download_link,
                            'add':bfile_in_list.add,
                            'like':bfile_in_list.like})

            except BFile.DoesNotExist:
                a = 0
            try:#check if the visitor is founder
                buser2 = BUser.objects.get(username = user_ip)                
                is_founder = ((buser2 == bname1.founder) or (user_ip == '59.66.140.65'))
                if is_founder:
                    head_info = u"欢迎回到虫洞"
            except:
                a = 0

        except BName.DoesNotExist:
            head_info = u"新的虫洞被打开"            
        #database end
        download_link_head = download_domain+current_path+u"/"
        return render_to_response('bfound.htm',
        {"static_file_url":static_file_url,
        "domain_url":domain_url,
        "bitwormhole_name":current_path,
        "head_info":head_info,
        "user_ip":user_ip,
        "size_limit":size_limit,
        "time_limit":"255",
        "download_link_head":download_link_head,
        "is_founder":is_founder,
        "download_list":downloadlist })

    elif request.method == 'POST':
        downloadlist=[]
        noticehead = ""
        ip_filter = re.compile(u"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if 'user_ip' in request.POST and 'file' in request.FILES:
            if ip_filter.match(request.POST['user_ip']):#IP correct
                file1 = request.FILES['file']
                if file1.size > size_limit*1000000 or file1.size < 10:#10~size_limit
                    headinfo = "上传文件大小错误"
                    #return render_to_response('bfound.htm',
                    #{"static_file_url":static_file_url,
                    #"domain_url":domain_url,
                    #"bitwormhole_name":current_path,
                    #"head_info":"上传的文件大小错误",
                    #"user_ip":user_ip,
                    #"size_limit":size_limit,
                    #"time_limit":"255",
                    #"notice_head":" ",
                    #"download_list":downloadlist })
                #### 正确上传文件     
                else:
                    
                    #for add info
                    add_info = "没有备注"
                    if 'describe' in request.POST:
                        add_info = request.POST['describe']
                        if len(add_info)<1:
                            add_info = "没有备注"
                        elif len(add_info)>128:
                            add_info = add_info[0:127]
                    #for keyword
                    keyword_md5 = ""
                    if 'keyword' in request.POST:
                        keyword_md5 = request.POST['keyword']
                        if len(keyword_md5)==0:
                            keyword_md5_ = ""
                        elif len(keyword_md5)==16:
                            keyword_md5_ = keyword_md5+u'_'
                        else:
                            message = u"密码传输错误"+keyword_md5
                            return HttpResponse(message)
                    else:
                        message = u"密码传输错误"+keyword_md5
                        return HttpResponse(message)
                    #    if len(keyword)>0 and len(keyword)<20:
                    #        import hashlib
                    #        keyword_md5=hashlib.md5(keyword).hexdigest()
                    #        keyword_md5=keyword_md5[0:15]
                    
                    #for filename
                    filename1 = file1.name
                    if len(filename1)>80:
                        message = u"文件名太长，请缩短再上传"
                        return HttpResponse(message)
                    filename1 = filename1.decode('utf-8')
                        #then filename is unicode
                    #for storage i/o
                    file_storage_dir = storage_path+current_path
                    if not os.path.exists(file_storage_dir.encode('utf-8')):
                        #file i/o should encode from unicode to utf-8
                        os.makedirs(file_storage_dir.encode('utf-8'))
                    file_storage_path = storage_path+current_path+u'/'+keyword_md5_+filename1
                        #file_storage_path is md5 coded
                    with open(file_storage_path.encode('utf-8'),'wb+') as destination:
                        for chunk in file1.chunks():
                            destination.write(chunk)
                    #### database input begin
                    # user anyone has been created as unregistered user
                    downloadlist = []
                    try:#add user and wormhole record
                        bname1 = BName.objects.get(name = current_path)
                    except BName.DoesNotExist:
                        try:
                            buser1 = BUser.objects.get(username = user_ip)
                        except BUser.DoesNotExist:
                            buser1 = BUser(username=user_ip,
                                     email="",
                                     password="")
                            buser1.save()
                        #buser1 = BUser.objects.get(username = 'anyone')
                        bname1 = BName(name=current_path,
                                 datetime=datetime.datetime.now(),
                                 wormholeclass=1,#1 for normal
                                 volumnlimit=100000000,
                                 founder=buser1)
                        bname1.save()
                    try:#add file record
                        bfile1 = BFile.objects.get(filename=filename1)
                        bfile1.delete()
                    except BFile.DoesNotExist:
                        a = 0
                    bfile1 = BFile(filename=filename1,
                                 bname=bname1,
                                 datetime=datetime.datetime.now(),
                                 key = keyword_md5,
                                 add = add_info,
                                 like = 0)
                    bfile1.save()
                    

                    #### database input end
                    
                    message = u"上传成功！"
                    return HttpResponse(message)

        if 'user_ip' in request.POST and 'del_id' in request.POST:
            try:#check if the visitor is founder
                buser2 = BUser.objects.get(username = user_ip)
                
                is_founder = (buser2.username == request.POST['user_ip'])
                is_manager = (request.POST['user_ip'] == user_ip)
                del_id = request.POST['del_id']
                
                if is_founder or is_manager:
                    message = u"已删除"
                    try:
                        bfile2 = BFile.objects.get(id = del_id)
                        
                        keyword_md5_ = bfile2.key
                        if len(keyword_md5_)>0:
                            keyword_md5_ = keyword_md5_ + u'_'
                        filename2 = bfile2.filename
                        bfile2.delete()#delete from database
                        file_storage_path = storage_path+current_path+u'/'+keyword_md5_+filename2

                        if os.path.exists(file_storage_path.encode('utf-8')):
                            #file i/o should encode from unicode to utf-8
                            os.remove(file_storage_path.encode('utf-8'))
                    except:
                        message = u"已经删除过了"
                else:
                    message = u"删除出错"
                return HttpResponse(message)
            except:
                a = 0
        
        message = u'唉～你上传的文件不对头，是不是忘记添加文件了？后退重新上传吧！'
        #message = request.POST['user_ip']+"/"+request.POST['del_id']
        return HttpResponse(message)

@csrf_exempt
def bindex(request):

    if request.method == 'GET':
        return render_to_response('bindex.htm',
            {"static_file_url":"http://static.bitwormhole.com/static/",
            "domain_url":"http://bitwormhole.com/"})
    elif request.method == 'POST':
        ip_filter = re.compile(u'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        if 'user_ip' in request.POST:
            if ip_filter.match(request.POST['user_ip']):#IP correct
                message = 'Your IP is : %r ,it is correct' % request.POST['user_ip']

            else:
                message = 'Your IP is : %r ,it is incorrect' % request.POST['user_ip']
        else:
            message = 'Oh my god,I hate you'
        return HttpResponse(message)
