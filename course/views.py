import os

from django.contrib import messages
from docx import *
from py2neo import Graph

from course.util import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from course.models import Course
from course.models import *
import json
# Create your views here.
from course.utilForIndexpoint import createAndSaveRelationToDB

# 全局变量
graph = Graph("http://localhost:7474", username="neo4j", password='431879')
uploadPath = 'upload\course'
dirPath = os.path.abspath('.') + '\\' + uploadPath

def data(request):
    cql = request.GET.get('cql')
    datadic = {}
    if cql:
        pass
    else:
        # cql = 'match (n) return n'
        cql = 'MATCH p=()-->() RETURN p'
        cql = 'MATCH p=()-[r:CONTRIBUTION]->() RETURN p'

    datadic['data'] = getdata(cql)
    return render(request, 'data.html', datadic)

def data2(request):
    return render(request,'data2.html')
def data3(request):
    return render(request,'data.gexf')



def testjson(request):
    resp = {'errorcode': 100, 'detail': 'Get success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")

# 中间跳转
def tip(request):
    message = request.GET.get('str')
    context ={}
    context['message'] = message
    return render(request,'base.html',context)

# 基础风格模板
def base(request):
    return render(request, 'base.html')

# 主页视图
# 根据设置的资源不同，动态调整主页
def index(request):
    resources = [
        {'a': '/course/index/', 'img': '/static/img/1.jpg', 'h1': '主页','p': '课程体系知识图谱系统' },
        {'a': '/course/upload/', 'img': '/static/img/2.jpg', 'h1': '上传文件','p': '上传课程大纲' },
        {'a': '/course/files/', 'img': '/static/img/3.jpg', 'h1': '文件管理','p': '管理上传的文件' },
        {'a': '/course/data/', 'img': '/static/img/4.jpg', 'h1': '信息展示','p': '课程体系知识图谱信息展示' },
    ]
    context = {}
    context['resources'] = resources
    return render(request, 'index.html',context)

#上传功能
# def upload(request):
#     if request.method == 'GET':
#         err = {}
#         err['err'] = 0
#         err['message'] = 'not upload'
#         return render(request,'upload.html',err)
#     elif request.method == 'POST':
#
#         uploadFile = request.FILES.get('upload')    #获取上传文件
#
#         uploadPath = 'upload\course\\'               #文件上传路径
#         fileName = uploadFile.name                  #文件名
#
#         dirPath = os.path.abspath('.') + '\\' + uploadPath
#         while(os.path.exists(dirPath + '\\' +fileName )):
#             # index = 1
#             temp = fileName.split('.')
#             fileName = temp[len(temp)-2] +'(1).' + temp[len(temp)-1]
#             # index  = index +  1
#         #     保存文件
#         with open(os.path.join(uploadPath,fileName),'wb') as f:
#             for line in uploadFile.chunks():
#                 f.write(line)
#
#         filePath =  os.path.abspath('.') + '\\' + uploadPath + fileName  #文件绝对路径
#         err = {}
#         err['err'] = 1
#         err['message'] = '上传成功'
#         return render(request,'upload.html',err)
#         # return HttpResponseRedirect('uploadfiles')

# 批量上传
def upload2(request):
    if request.method == 'GET':
        err = {}
        err['err'] = 0
        err['message'] = 'not upload'
        return render(request, 'upload.html', err)
    elif request.method == 'POST':
        uploadFiles = request.FILES  # 获取上传文件
        for name,uploadFile in uploadFiles.items():
            # uploadPath = 'upload\course\\'  # 文件上传路径
            fileName = uploadFile.name  # 文件名
            # dirPath = os.path.abspath('.') + '\\' + uploadPath  #上传目录绝对路径
            # 如果存在同名文件，修改现在上传文件的文件名
            while (os.path.exists(dirPath + '\\' + fileName)):
                temp = fileName.split('.')
                fileName = temp[len(temp) - 2] + '(1).' + temp[len(temp) - 1]
            #     保存文件
            with open(os.path.join(uploadPath, fileName), 'wb') as f:
                for line in uploadFile.chunks():
                    f.write(line)
        err = {}
        err['err'] = 1
        err['message'] = '上传成功'
        return render(request, 'upload.html', err)


# 上传文件信息展示
# 根据请求参数不同完成对上传的文件的操作
def uploadfiles(request):
    context ={}
    context['message'] = 'test message'
    deletekey = request.GET.get('delete')
    changekey = request.GET.get('change')
    updatekey = request.GET.get('update')
    startkey  = request.GET.get('start')
    if startkey:
        start(request)
    if deletekey :
        delete(request,context)
    if changekey:
        change(request,context)
        context['data'] = getFileInformation(dirPath)
        print(context)
        return render(request, 'uploadfiles.html', context)
    if updatekey:
        update(request,context)

    context['data']= getFileInformation(dirPath)
    print(context)
    return render(request, 'uploadfiles.html', context)
# 已上传文件的删除功能
def delete(request,context):
    deletefile = request.GET['delete']
    deletefile = deletefile.replace('../','')
    deletefile = deletefile.replace('..\\','')

    filePath = dirPath + '\\' + deletefile
    if os.path.exists(filePath):
        try:
            os.remove(filePath )
            context['message'] = 'delete success'
        except Exception as e:
            print(e)
    else:
        context['message'] = 'not found file'
# 已上传文件doc转换为docx功能
def change(request,context):
    changefile = request.GET['change']

    filePath = dirPath + '\\' + changefile
    if getFileType(filePath) == 'doc':
        filePath = docSaveToDocx(filePath)
        context['message'] = 'doc 成功转换为docx'
    else:
        context['message'] = '不是doc文件不能转换'

def update(request,context):
    updatefile = request.GET['update']

    filePath = dirPath + '\\' + updatefile
    if os.path.exists(filePath):
        try:
            saveRelationToDB(filePath,graph)
            context['message'] = 'update success'
        except Exception as e:
            print(e)
    else:
        context['message'] = 'update fail'

# 预先创建指标点/毕业要求
def start(request):
    file = 'E:\pycharmProject\CourseSystem\static\\毕业要求.docx'
    createAndSaveRelationToDB(file,graph)





# if __name__ == '__main__':
#     path = 'asffw/../sfsf/../wfwf'
#     p = path.split('../')
#     print(p)