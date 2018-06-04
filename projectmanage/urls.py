from django.conf.urls import url
from . import views
from django.urls import path
app_name='YuceInfo'
urlpatterns=[
    path('', views.index),
    #项目管理的任务操作
    path('PMTaskHandle/pause/',views.pmtaskhandle.pause), # 暂停操作 cmd：实验暂停 分析暂停
    path('PMTaskHandle/add/',views.pmtaskhandle.add), # 保留项
    path('PMTaskHandle/reset/',views.pmtaskhandle.reset), # 重置任务
    path('PMTaskHandle/go/', views.pmtaskhandle.go), # 保留项
    path('PMTaskHandle/modify/', views.pmtaskhandle.modify), # 任务修改
    path('PMTaskHandle/view/', views.pmtaskhandle.view), # 任务列表
    path('PMTaskHandle/stop/', views.pmtaskhandle.stop), #终止任务
    path('PMTaskHandle/cancel/', views.pmtaskhandle.cancel), # 取消操作 cmd： 取消实验 取消解读
    # 实验室管理的任务操作
    path('LabTaskHandle/cmd/', views.labtaskhandle.pause), # cmd操作，进行，暂停，终止,重置
    # path('LabTaskHandle/reset/', views.labtaskhandle.reset), # 重置任务
    path('LabTaskHandle/loadsample/', views.labtaskhandle.go), # 上机
    path('LabTaskHandle/view/', views.labtaskhandle.view), # 任务列表
    # path('LabTaskHandle/stop/', views.labtaskhandle.stop), #
    path('LabTaskHandle/finish/', views.labtaskhandle.finish), # 完成测序
    # 自动化投递任务操作
    path('AutoTaskHandle/get/',views.autotaskhandle.GET),
    path('AutoTaskHandle/post/', views.autotaskhandle.POST),
    # 项目操作
    path('ProjectHandle/init/',views.projecthandle.init), # 添加项目
    path('ProjectHandle/stop/', views.projecthandle.stop), # 终止项目
    path('ProjectHandle/addpatient/', views.projecthandle.addpatient), #添加患者
    path('ProjectHandle/pay/', views.projecthandle.pay), # 项目缴费
    path('ProjectHandle/pause/', views.projecthandle.pause), #项目暂停
    path('ProjectHandle/reset/', views.projecthandle.reset), #项目重置
    path('ProjectHandle/view/', views.projecthandle.view), # 项目列表
    path('ProjectHandle/cancel/', views.projecthandle.cancel), # 项目列表
    # 患者操作
    path('PatientHandle/init/', views.patienthandle.init), # 添加患者
    path('PatientHandle/view/', views.patienthandle.view), # 患者列表
    path('PatientHandle/addproject/', views.patienthandle.addproject), # 直接下单
    path('PatientHandle/add2project/', views.patienthandle.add2project), # 添加到项目
    # 样本操作
    path('SampleHandle/init/', views.samplehandle.init), # 添加样本
    path('SampleHandle/add/', views.samplehandle.add), # 补充样本
    path('SampleHandle/view/', views.samplehandle.view), # 样本列表
    # 产品操作
    path('ProductHandle/view/',views.producthandle.view), # 产品列表
    path('ProductHandle/add/', views.producthandle.add), # 添加或修改产品

]