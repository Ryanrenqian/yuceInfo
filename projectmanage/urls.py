from . import views
from django.urls import path,register_converter
import logging
app_name='YuceInfo'

# class FilePath:
#     regex=".*"
#     def to_python(self,value):
#         logging.info(str(value))
#         return str(value)
#     def to_url(self,value):
#         logging.info(str(value))
#         return '%s'%str(value)
#
# register_converter(FilePath,'fp')
urlpatterns=[
    path('', views.index),
    path('imageview/<path:path>/',views.fileview.imageview,name='imageview'),
    path('tableview/<path:path>/',views.fileview.tableview,name='tableview'),
    #项目管理的任务操作
    path('PMTaskHandle/pause/',views.pmtaskhandle.cmd), # 暂停操作 cmd：实验暂停 分析暂停
    # path('PMTaskHandle/add/',views.pmtaskhandle.add), # 保留项
    # path('PMTaskHandle/reset/',views.pmtaskhandle.reset), # 重置任务
    path('PMTaskHandle/go/', views.pmtaskhandle.go), # 保留项
    path('PMTaskHandle/modify/', views.pmtaskhandle.modify), # 任务修改
    path('PMTaskHandle/view/', views.pmtaskhandle.view), # 任务列表
    path('PMTaskHandle/stop/', views.pmtaskhandle.stop), #终止任务
    path('PMTaskHandle/cancel/', views.pmtaskhandle.cancel), # 取消操作 cmd： 取消实验 取消解读
    path('PMTaskHandle/allocate/', views.pmtaskhandle.allocate),  # 任务分配

    # 实验室管理的任务操作
    path('LabTaskHandle/cmd/', views.labtaskhandle.cmd), # cmd操作，进行，暂停，终止,重置
    # path('LabTaskHandle/reset/', views.labtaskhandle.reset), # 重置任务
    path('LabTaskHandle/loadsample/', views.labtaskhandle.loadsample), # 上机
    path('LabTaskHandle/view/', views.labtaskhandle.view), # 任务列表
    # path('LabTaskHandle/stop/', views.labtaskhandle.stop), #
    path('LabTaskHandle/finish/', views.labtaskhandle.finish), # 完成测序
    # 自动化投递任务操作
    # path('AutoTaskHandle/get/',views.autotaskhandle.GET),
    # 分析师任务操作
    path('AnaTaskHandle/view/',views.anataskhandle.view),
    path('AnaTaskHandle/modify/',views.anataskhandle.modify),
    path('AnaTaskHandle/qcview/', views.anataskhandle.qcview),
    # 解读师任务擦欧总
    path('JieduTaskHandle/view/', views.jiedutaskhandle.view),# 任务列表
    path('JieduTaskHandle/detailview/', views.jiedutaskhandle.detailview),#任务详细
    path('JieduTaskHandle/download/', views.jiedutaskhandle.download),#下载报告
    path('JieduTaskHandle/upload/', views.jiedutaskhandle.upload),#上传报告
    path('JieduTaskHandle/review/', views.jiedutaskhandle.review),#审核

    # path('AutoTaskHandle/post/', views.autotaskhandle.POST),
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
    path('PatientHandle/modify/', views.patienthandle.modify), # 患者列表
    path('PatientHandle/addproject/', views.patienthandle.addproject), # 直接下单
    path('PatientHandle/add2project/', views.patienthandle.add2project), # 添加到项目
    path('PatientHandle/batchadd/',views.patienthandle.batchadd), # 批量导入患者
    # 样本操作
    path('SampleHandle/init/', views.samplehandle.init), # 添加样本
    path('SampleHandle/modify/', views.samplehandle.modify), # 完善或者修改样本信息
    path('SampleHandle/view/', views.samplehandle.view), # 样本列表
    # 产品操作
    path('ProductHandle/view/',views.producthandle.view), # 产品列表
    path('ProductHandle/add/', views.producthandle.add), # 添加或修改产品

]