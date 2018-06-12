import requests,json,logging
from projectmanage.models import *
import time,datetime
logging.basicConfig(filename='data.url.txt',level=logging.INFO,format='%(message)s')


url='http://192.168.1.186:8000/'

# # 测试前先清理数据
# Project.drop_collection()
# Task.drop_collection()
# Patient.drop_collection()
# Sample.drop_collection()


# Class
class PMclient:
    def __init__(self,url=url):
        self.BaseUrl=url
    def pause(self,data):
        url=self.BaseUrl+'PMTaskHandle/pause/'
        response=requests.post(url,json=data)
        logging.info(response.text)
        return response.text
    def add(self,data):
        url = self.BaseUrl + 'PMTaskHandle/add/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def reset(self,data):
        url = self.BaseUrl + 'PMTaskHandle/reset/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def go(self,data):
        url = self.BaseUrl + 'PMTaskHandle/go/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('json: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def modify(self,data):
        url = self.BaseUrl + 'PMTaskHandle/modify/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def view(self):
        url = self.BaseUrl + 'PMTaskHandle/view/'
        response = requests.get(url)
        logging.info('url: %s'%url)
        logging.info('response: %s'%response.text)
        return response.text
    def stop(self,data):
        url = self.BaseUrl + 'PMTaskHandle/stop/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def cancel(self,data):
        url = self.BaseUrl + 'PMTaskHandle/cancel/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text

class LabTaskHandle:
    def __init__(self,url=url):
        self.BaseUrl=url
    def cmd(self,data):
        url=self.BaseUrl+'LabTaskHandle/cmd/'
        response=requests.post(url,json=data)
        logging.info(url)
        return response.text

    def loadsample(self,data):
        url = self.BaseUrl + 'LabTaskHandle/loadsample/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text

    def view(self):
        url = self.BaseUrl + 'LabTaskHandle/view/'
        response = requests.get(url)
        logging.info('url: %s'%url)
        logging.info('response: %s'%response.text)
        return response.text

    def finish(self,data):
        url = self.BaseUrl + 'LabTaskHandle/finish/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text

class AutoTaskHandle:
    def __init__(self,url=url):
        self.BaseUrl=url
    def get(self,data):
        url=self.BaseUrl+'AutoTaskHandle/pause/'
        response=requests.get(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def post(self,data):
        url = self.BaseUrl + 'AutoTaskHandle/pause/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text

class ProjectHandle:
    def __init__(self,url=url):
        self.BaseUrl=url
    def initget(self):
        url = self.BaseUrl + 'ProjectHandle/init/'
        response = requests.get(url)
        logging.info('url: %s'%url)
        logging.info('response: %s'%response.text)
        return response.text
    def initpost(self,data):
        url=self.BaseUrl+'ProjectHandle/init/'
        response=requests.post(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def stop(self,data):
        url = self.BaseUrl + 'ProjectHandle/stop/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def addpatient(self,data):
        url=self.BaseUrl+'ProjectHandle/addpatient/'
        response=requests.get(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def pay(self,data):
        url = self.BaseUrl + 'ProjectHandle/pay/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def pause(self,data):
        url=self.BaseUrl+'ProjectHandle/pause/'
        response=requests.get(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def reset(self,data):
        url = self.BaseUrl + 'ProjectHandle/reset/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def view(self):
        url = self.BaseUrl + 'ProjectHandle/view/'
        response = requests.get(url)
        logging.info('url: %s'%url)
        logging.info('response: %s'%response.text)
        return response.text

class SampleHandle:
    def __init__(self,url=url):
        self.BaseUrl=url
    def init(self,data):
        url=self.BaseUrl+'SampleHandle/init/'
        response=requests.get(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def add(self,data):
        url = self.BaseUrl + 'SampleHandle/add/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def view(self,data):
        url = self.BaseUrl + 'SampleHandle/view/'
        response = requests.get(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text

class ProductHandle:
    def __init__(self,url=url):
        self.BaseUrl=url
    def init(self,data):
        url=self.BaseUrl+'ProductHandle/init/'
        response=requests.get(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def add(self,data):
        url = self.BaseUrl + 'ProductHandle/add/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def view(self):
        url = self.BaseUrl + 'ProductHandle/view/'
        response = requests.get(url)
        logging.info('url: %s'%url)
        logging.info('response: %s'%response.text)
        return response.text

class PatientHandle:
    def __init__(self,url=url):
        self.BaseUrl=url
    def init(self,data):
        url=self.BaseUrl+'PatientHandle/init/'
        response=requests.post(url,json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def addproject(self,data):
        url = self.BaseUrl + 'PatientHandle/addproject/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def view(self,data):
        url = self.BaseUrl + 'PatientHandle/view/'
        response = requests.get(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text
    def add2project(self,data):
        url = self.BaseUrl + 'PatientHandle/add2project/'
        response = requests.post(url, json=data)
        logging.info('url: %s'%url)
        logging.info('data: %s'%data)
        logging.info('response: %s'%response.text)
        return response.text

# ProductHandle 模块测试
def test_product():
    productclient=ProductHandle(url)
    logging.info('产品管理/产品目录')
    productclient.view()
    logging.info('产品管理/添加产品')
    product={
    'productid':'MT100000',
    'productname':'YuceOne PLus',
    'book':'book',
    'config': 'config',
    'period': 5,
    'normaltype': '血液',
    'normalsize': '5g',
    'tumortype': '组织',
    'tumorsize': '5g',
    'platform': 'NGS',
    'bestuptime': 5,
    'worstuptime': 10,
    'chip': 'chip',
    'strategy': '151bp',
    'moletag': '否',

    }
    productclient.add(product)

# PatientHandle 模块测试
def test_patient():
    patientclient=PatientHandle(url)
    patient1={
    'patientid' : '0000001',
    'patientname' : '1号玩家',
    'tumortype' : '肺癌',
        'age':15,
        'gender':'男'
    }
    logging.info('项目管理/患者管理/添加患者')
    patientclient.init(patient1)
    logging.info('项目管理/患者管理-下单')
    patient1_addproject={
    'products':['MT100000'],
    'tumortype':'肺癌 胃癌',
    'patientid': '0000001',
    'account' : 'renqian',
    'tag': '科研'
    }
    patientclient.addproject(patient1_addproject)
    logging.info('项目管理/患者管理-加入项目')
    data={
        'projectid':Project.objects.first().pk,
        'patientid': Patient.objects.first().pk,
    }
    patientclient.add2project(data)

# PMTaskHandle 模块测试
def test_pmtask():
    pmclient=PMclient(url)
    logging.info('项目管理/任务管理')
    task=json.loads(pmclient.view())[0]
    taskid=task['taskid']
    # pause task
    logging.info('项目管理/任务管理-实验暂停')
    pause_lab={
        'taskid':taskid,
        'cmd': '实验暂停',
        'info': '尚未确定内容'
    }
    pmclient.pause(pause_lab)
    logging.info('项目管理/任务管理-分析暂停')
    pause_ana={
        'taskid':taskid,
        'cmd': '分析暂停',
        'info': '尚未确定内容'
    }
    pmclient.pause(pause_ana)
    logging.info('项目管理/任务管理-解读暂停')
    pause_ana={
        'taskid':taskid,
        'cmd': '解读暂停',
        'info': '尚未确定内容'
    }
    pmclient.pause(pause_ana)
    logging.info('项目管理/任务管理-重置任务')
    data={
        'taskid':taskid,
        'info': '尚未确定内容'
    }
    pmclient.reset(data)
    logging.info('项目管理/任务管理-修改任务')
    pmclient.modify(task)
    logging.info('项目管理/任务管理-终止任务')
    data={
        'taskid':taskid,
        'info': '尚未确定内容'
    }
    pmclient.stop(data)
    logging.info('项目管理/任务管理-取消实验')
    data={
        'taskid':taskid,
        'cmd':'取消实验',
        'info': '尚未确定内容'
    }
    pmclient.cancel(data)
    logging.info('项目管理/任务管理-取消解读')
    data={
        'taskid':taskid,
        'cmd':'取消解读',
        'info': '尚未确定内容'
    }
    pmclient.cancel(data)

# 测试 LabTaskHandle模块
def test_labtask():
    labtaskclient=LabTaskHandle(url)
    logging.info('实验室管理/任务管理-暂停实验')
    data={
        'taskid':Task.objects.first().pk,
        'info':'随便填写原因',
        'cmd':'暂停'
    }
    labtaskclient.cmd(data)
    logging.info('实验室管理/任务管理-重置任务')
    data = {
        'taskid': Task.objects.first().pk,
        'info': '随便填写原因'

    }
    labtaskclient.cmd(data)
    logging.info('实验室管理/任务管理-进行实验')
    data = {
        'taskid': Task.objects.first().pk,
        'cmd':'实验',
        'info': '随便填写原因'
    }
#    labtaskclient.go(data)
#    logging.info('实验室管理/任务管理-上机')
#     data = {
#         'taskid': Task.objects.first().pk,
#         'cmd': '上机',
#         'info': '随便填写原因'
#     }
#     labtaskclient.go(data)

    logging.info('实验室管理/任务管理-终止')
    data = {
        'taskid': Task.objects.first().pk,
        'cmd': '终止',
        'info': '随便填写原因'
    }
    labtaskclient.cmd(data)
    logging.info('实验室管理/任务管理-任务列表')
    labtaskclient.view()
    logging.info('实验室管理/任务列表-上机')
    data={
        'taskid':Task.objects.first().pk,
        'samples':[
            {
                'sampleid':'18A00335XJ03',
                'tumortype':'肺癌',
                'tissue':'血浆',
                'read1':'TACACTCTTTCCCTACACGACGCTCTTCCGATCT',
                'read2':'AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC',
                'platform':'Nextseq',
                'i5':'MID',
                'i7':'I4',
                'volume':5,
                'concentration':'',
                'QsepPeak':'',
                'qPCRConcentration':'',
                'datasize':5,
                'info':''

            },
            {
                'sampleid': '18A00000XY122',
                'tumortype': '肺癌',
                'tissue': '血液',
                'read1': 'TACACTCTTTCCCTACACGACGCTCTTCCGATCT',
                'read2': 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC',
                'platform': 'Nextseq',
                'i5': 'MID',
                'i7': 'I4',
                'volume': 5,
                'concentration': '',
                'QsepPeak': '',
                'qPCRConcentration': '',
                'datasize': 5,
                'info': ''
            }
        ]
    }
    labtaskclient.loadsample(data)

# 测试 ProjectHandle 模块
def test_project():
    projectclient=ProjectHandle(url)
    # check project
    logging.info('项目管理/项目管理')
    projectclient.view()
    logging.info('项目管理/添加项目-获取数据')
    projectclient.initget()
    logging.info('项目管理/添加项目-提交数据')
    project={
        'patients':'0000001 0000002',
        'start_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'deadline': (datetime.datetime.now()+datetime.timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S"),
        'products': ['MT100000'],
        'tumortype': '肺癌',
        'institute': 'yucebio',
        'duty': 'renqian',
        'projectid':'',
        'info': '',
        'tag':'科研'
    }
    projectclient.initpost(project)


Task.drop_collection()
Project.drop_collection()
Sample.drop_collection()
test_product()
test_patient()
test_labtask()
test_project()
# # # test_pmtask()
# data={'patient': 'asdf', 'tumortype': '肺癌', 'flag': '333333333', 'tissue': '血浆', 'type': 'as', 'i5': 'MID', 'i7': 'I4', 'volume': 5, 'concentration': '', 'QsepPeak': '', 'qPCRentration': '', 'datasize': 5, 'read1': 'TACACTCTTTCCCTACACGACGCTCTTCCGATCT', 'read2': 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC', 'platform': 'Nextseq', 'info': '', 'sampleid': '18A00335XJ03'}
# data['patient']=data[]
# sample=Sample.objects(pk=data.pop('sampleid')).first()
# sample.modify(**data)
data={'taskid':'soyirJEYje'}
res=requests.post(url+'AnaTaskHandle/qcview/',json=data)
print(res.text)