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
    path('PMTaskHandle/reset/',views.pmtaskhandle.reset), # 重置任务
    path('PMTaskHandle/go/', views.pmtaskhandle.go), # 保留项
    path('PMTaskHandle/modify/', views.pmtaskhandle.modify), # 任务修改
    path('PMTaskHandle/view/', views.pmtaskhandle.view), # 任务列表
    path('PMTaskHandle/stop/', views.pmtaskhandle.stop), #终止任务
    path('PMTaskHandle/cancel/', views.pmtaskhandle.cancel), # 取消操作 cmd： 取消实验 取消解读
    path('PMTaskHandle/allocate/', views.pmtaskhandle.allocate),  # 任务分配


    # 分析师任务操作
    path('AnaTaskHandle/view/',views.anataskhandle.view),
    path('AnaTaskHandle/modify/',views.anataskhandle.modify),
    path('AnaTaskHandle/qcview/', views.anataskhandle.qcview),
    # 解读师任务操作
    path('JieduTaskHandle/view/', views.jiedutaskhandle.view),# 任务列表
    path('JieduTaskHandle/detailview/', views.jiedutaskhandle.detailview),#任务详细
    path('JieduTaskHandle/download/', views.jiedutaskhandle.download),#下载报告
    path('JieduTaskHandle/upload/', views.jiedutaskhandle.upload),#上传报告
    path('JieduTaskHandle/review/', views.jiedutaskhandle.review),#审核
    # 项目操作
    path('ProjectHandle/init/',views.projecthandle.init), # 添加项目
    path('ProjectHandle/complement/', views.projecthandle.complement), #补充订单
    path('ProjectHandle/complementhelp/', views.projecthandle.complementhelp), #辅助补充订单
    path('ProjectHandle/cmd/', views.projecthandle.cmd), # 项目cmd
    path('ProjectHandle/view/', views.projecthandle.view), # 项目列表
    # 患者操作
    path('PatientHandle/init/', views.patienthandle.init), # 添加患者
    path('PatientHandle/view/', views.patienthandle.view), # 患者列表
    path('PatientHandle/modify/', views.patienthandle.modify), # 患者列表
    path('PatientHandle/addproject/', views.patienthandle.addproject), # 直接下单
    path('PatientHandle/add2project/', views.patienthandle.add2project), # 添加到项目
    path('PatientHandle/batchadd/',views.patienthandle.batchadd), # 批量导入患者
    # 样本管理
    path('SampleHandle/init/', views.samplehandle.init), # 添加样本
    path('SampleHandle/modify/', views.samplehandle.modify), # 完善或者修改样本信息
    path('SampleHandle/view/', views.samplehandle.view), # 样本列表
    path('SampleHandle/upload/', views.samplehandle.upload), # 批量导入样本
    # 实验室管理的任务操作
    path('LabTaskHandle/cmd/', views.labtaskhandle.cmd), # cmd操作，进行，暂停，终止,重置
    path('LabTaskHandle/order/', views.labtaskhandle.order), # 内部下单
    path('LabTaskHandle/view/', views.labtaskhandle.view), # 任务列表
    # 提取管理
    path('ExtractHandle/upload/', views.extracthandle.upload), # 批量导入数据
    path('ExtractHandle/view/', views.extracthandle.view), # 提取结果列表
    # 建库管理
    path('LibraryHandle/view/', views.libraryhandle.view),  # 提取结果列表
    path('LibraryHandle/upload/', views.libraryhandle.upload),  # 提取结果列表
    # 杂交
    path('HybridHandle/view/', views.hybridhandle.view),  # 提取结果列表
    path('HybridHandle/upload/', views.hybridhandle.upload),  # 提取结果列表
    # 质控
    path('LabQCHandle/view/', views.labqc.view),  # 提取结果列表
    path('LabQCHandle/upload/', views.labqc.upload),  # 提取结果列表
    # 测序
    path('seqhandle/view/', views.seqhandle.view),  # 提取结果列表
    path('seqhandle/upload/', views.seqhandle.upload),  # 提取结果列表

    # 产品操作
    path('ProductHandle/view/',views.producthandle.view), # 产品列表
    path('ProductHandle/add/', views.producthandle.add), # 添加或修改产品
]