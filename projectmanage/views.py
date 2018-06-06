from django.shortcuts import HttpResponse
import datetime,json,random,string,logging,os
import pandas as pd
from .models import *



logging.basicConfig(level=logging.DEBUG,filename='log.txt',format='%(asctime)s: %(message)s')
# Create your views here.
# 生成uniq ID debug
def GenerateID(database):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    while True:
        if len(database.objects(pk=ran_str))==0:
            obj=database(pk=ran_str)
            obj.save()
            break
        else:
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return ran_str

configpath='config'
def GenerateTask(patient,product,tumortype,configoath=configpath):
    '''

    :param patient: Patient Object
    :param product:  str Product
    :param tumortype:  str Tumortype
    :return:
    '''
    taskid=GenerateID(Task)
    task=Task.objects(pk=taskid).first()
    product=Product.objects(productid=product).first()
    starttime = datetime.datetime.now()
    bestuptime = starttime + datetime.timedelta(days=product.bestuptime)
    worstuptime = starttime + datetime.timedelta(days=product.worstuptime)
    deadline = starttime + datetime.timedelta(days=product.worstuptime)
    logging.debug('add task: %s %s %s %s' % (taskid, patient, product, tumortype))
    task.modify(status='开始',
                tumor=tumortype,
                product=product,
                patient=patient,
                starttime=starttime,
                bestuptime=bestuptime,
                worstuptime=worstuptime,
                deadline=deadline,
                chip=product.chip,
                strategy=product.strategy,
                moletag=product.moletag,
                normaltype = product.normaltype,
                normalsize = product.normalsize,
                platform = product.platform,
                tumortype = product.tumortype,
                tumorsize = product.tumorsize,
                config=configpath+'/'+product.config
                )
    return task

def handle_uploaded_file(f,tmp):
    file=tmp+f.name
    with open(file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file

def index(request):
    return HttpResponse('index')

class Handle:
    '''
    处理器父类：提供权限检查和临时文件存储支持
    '''
    def __init__(self, group, check,tmp=None):
        '''
        初始化
        :param group:
        :param check:
        :param tmp:
        '''
        self.group = group
        self.check = check
        self.tmp=tmp

    def is_valid(self, request):
        if not self.check:
            return True
        else:
            user = request.session['user']
            user = User.objects(pk=user).first()
            return user.group in self.group

    @property
    def checktmp(self):
        if not os.path.exists(self.tmp):
            return os.mkdir(self.tmp)
        return True

class TaskHandle(Handle):
    '''
    任务处理类： 模板设计
    '''
    def pause(self,request):
        '''

        :param request:
        :return: message
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def add(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def reset(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def go(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def modify(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def view(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def stop(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def cancel(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class PMTaskHandle(TaskHandle):
    '''
    项目管理：任务处理器
    '''
    def pause(self,request):
        '''
        通过post传递暂停命令：
        cmd调控暂停的内容
        :param request:
        :return: message
        '''
        message={}
        if self.is_valid(request):
            if request.method =='POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.debug(data)
                task = Task.objects(pk=data['taskid']).first()
                if task.info:
                    info = task.info + data['info']
                else:
                    info=data['info']
                if data['cmd']=='实验暂停':
                    try:
                        task.modify(status='暂停', expstatus='暂停', info=info)
                        message['success'] = '实验暂停成功'
                    except Exception as e:
                        message['error'] = str(e)
                        logging.debug(e)
                elif data['cmd']=='分析暂停':
                    try:
                        task.modify(status='暂停', anastatus='暂停', info=info)
                        message['success'] = '分析暂停成功'
                    except Exception as e:
                        message['error'] = str(e)
                        logging.debug(e)
                elif data['cmd']=='解读暂停':
                    try:
                        task.modify(status='暂停', jiedu_status='暂停', info=info)
                        message['success'] = '解读暂停成功'
                    except Exception as e:
                        message['error'] = str(e)
                        logging.debug(e)
        else:
            message['warning']='对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def add(self,request):
        '''
        添加任务（暂不需要）
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def reset(self,request):
        '''
        重置任务，与实验室的重置不一样
        :param request:
        :return: message
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task = Task.objects(pk=data['taskid']).first()
                info = str(task.info)
                info = str(info) + str(data['info'])
                try:
                    task.modify(status='进行', expstatus='开始', anastatus='wait', jiedu_status='wait', reportstatus='wait',info=info)
                    message['success'] = '重置成功'
                except Exception as e:
                    message['error'] = str(e)
                    logging.debug(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message,ensure_ascii=False))

    def go(self,request):
        '''
        操作
        :param request:
        :return: message
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def modify(self,request):
        '''
        修改
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.debug(data)
                task = Task.objects(pk=data['taskid']).first()
                try:
                    task.modify(**data)
                    message['success']='任务修改成功'
                except Exception as e:
                    logging.debug(e)
                    message['error']=str(e)
        else:
            message['warning']='对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # views
    def view(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                task_list = json.loads(Task.objects().all().to_json(ensure_ascii=False))
                task_list = [task for task in task_list if task.get('starttime')]
                for task in task_list:
                    task['taskid'] = task.pop('_id')
                    task['patientname'] = Patient.objects(pk=task.get('patient')).first().patientname
                    task['starttime'] = datetime.datetime.fromtimestamp(task['starttime']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    task['bestuptime'] = datetime.datetime.fromtimestamp(task['bestuptime']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    task['worstuptime'] = datetime.datetime.fromtimestamp(task['worstuptime']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
                return HttpResponse(json.dumps({'data':task_list},ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 终止
    def stop(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task = Task.objects(pk=data['taskid']).first()
                data['info'] = data['info'] + task.info
                try:
                    task = Task.objects(pk=data['taskid']).first()
                    task.modify(status='终止',
                                expstatus='终止',
                                anastatus='终止',
                                jiedustatus='终止',
                                reportstatus='终止',
                                info=data['info'])
                    message['success'] = '终止成功'
                except Exception as e:
                    message['error'] = '操作失败'
                    logging.debug(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 取消
    def cancel(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task = Task.objects(pk=data['taskid']).first()
                if data['cmd'] == '取消实验':
                    try:
                        task.modify(expstatus='无', anastatus='开始')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
                if data['cmd'] == '取消解读':
                    try:
                        task.modify(expstatus='无', anastatus='开始')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class LabTaskHandle(TaskHandle):
    '''
    实验管理：任务处理器
    '''
    def cmd(self, request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.info('cmd: %s'%request.body.decode('utf-8'))
                task = Task.objects(pk=data['taskid']).first()
                data['info'] = data.get('info','')+ task.info
                cmd=data.pop('cmd')
                task = Task.objects(pk=data['taskid']).first()
                if cmd=='暂停':
                    task.modify(status='暂停', expstatus='暂停', **data)
                    message['success'] = '暂停成功'
                elif cmd=='终止':
                    task.modify(status='终止',
                                expstatus='终止',
                                anastatus='终止',
                                jiedu_status='终止',
                                reportstatus='终止',
                                **data)
                    message['success']='终止成功'
                elif cmd=='重置':
                    starttime = datetime.datetime.now()
                    deadline = datetime.datetime.now() + datetime.timedelta(days=task.product.period)
                    bestuptime = datetime.datetime.now() + datetime.timedelta(days=task.product.bestuptime)
                    worstuptime = datetime.datetime.now() + datetime.timedelta(days=task.product.worstuptime)
                    try:
                        task.modify(
                            starttime=starttime, deadline=deadline,
                            bestuptime=bestuptime, worstuptime=worstuptime,
                            status='开始', expstatus='开始')
                        message['success'] = '实验重启成功'
                    except Exception as e:
                        message['error']=str(e)
                elif cmd=='完成':
                    task.modify(expstatus='完成',**data)
                    message['success']='已完成'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))


    def loadsample(self, request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.info(str(data))
                task = Task.objects(pk=data['taskid']).first()
                samples=[]
                for sample in data['samples']:
                    sample=Sample(**sample)
                    sample.save()
                    samples.append(sample)
                try:
                    task.modify(expstatus='上机',samples=samples)
                    message['success']='上样成功～'
                except Exception as e:
                    message['error'] = str(e)
                    logging.debug(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def view(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                task_list = json.loads(Task.objects().all().to_json(ensure_ascii=False))
                task_list = [task for task in task_list if task.get('starttime')]
                for task in task_list:
                    task['taskid'] = task.pop('_id')
                    task['patientname'] = Patient.objects(pk=task.get('patient')).first().patientname
                    task['starttime'] = datetime.datetime.fromtimestamp(task['starttime']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    task['bestuptime'] = datetime.datetime.fromtimestamp(task['bestuptime']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    task['worstuptime'] = datetime.datetime.fromtimestamp(task['worstuptime']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
                return HttpResponse(json.dumps(task_list, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))


    def finish(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task= Task.objects(pk=data['taskid']).first()
                sample_list=data['samples']
                samples=[]
                for sample in sample_list:
                    sample=Sample(**sample)
                    sample.save()
                    samples.append(sample)
                try:
                    task.modify(expstatus='完成',samples=samples,anastatus='开始')
                    patient=task.patient
                    patient.samples=patient.samples+samples
                    patient.save()
                    message['success']='操作成功'
                except Exception as e:
                    logging.debug(e)
                    message['error']=str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class AutoTaskHandle(Handle):
    '''
    本打算留作自动化投递任务的接口的，现在不需要了，也许以后会用得上
    '''
    def GET(self,request):
        pass
    def POST(self,request):
        pass

class AanaTaskHandle(TaskHandle):
    '''
    分析师：任务处理器，提供相关操作
    '''
    def view(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                task_list = Task.objects().all().to_json(ensure_ascii=False)
                for task in task_list:
                    task['taskid']=task.pop('_id')
                return HttpResponse(json.dumps(task_list,ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 暂停分析
    def pause(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task=Task.objects(pk=data['taskid']).first()
                data['info']=data.get('info','')+task.info
                try:
                    task.modify(**data)
                    message['success']='暂停成功'
                except Exception as e:
                    logging.debug(e)
                    message['error']=str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def tmp(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class ProjectHandle(Handle):
    '''
    项目管理：项目处理器
    '''
    def init(self,request):
        '''
        生成新的项目
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                warning = []
                patients = set(data['patients'].split())
                for patient in data['patients'].split():
                    if len(Patient.objects(pk=patient)) == 0:
                        warning.append(patient)
                        patients.remove(patient)
                data['patients'] = list(patients)
                tumortypes = data.get('tumortype').split()
                data['start_time'] = datetime.datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")
                data['deadline'] = datetime.datetime.strptime(data['deadline'], "%Y-%m-%d %H:%M:%S")
                if not data.get('projectid',None):
                    data['projectid']=GenerateID(Project)
                # info=data.pop('info')
                project = Project(**data)
                project.save()
                logging.debug(data)
                tasks = []
                for product in data['products']:
                    for patient in data['patients']:
                        if tumortypes:
                            for tumortype in tumortypes:
                                patient=Patient.objects(patientid=patient).first()
                                patient.modify(taskstatus='有')
                                task = GenerateTask(patient,product,tumortype)
                                tasks.append(task)
                        else:
                            Patient.objects(pk=patient).first().modify(taskstatus='有')
                            task = GenerateTask(patient, product, '')
                            tasks.append(task)
                data['tasks']=tasks
                project.modify(tasks=tasks)
                message['success'] = '保存成功'
                if len(warning) != 0:
                    message['warning'] = '以下患者出现问题，可能不存在：%s' % (','.join(set(warning)))
                return HttpResponse(json.dumps(message, ensure_ascii=False))
            else:
                data = {}
                product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
                for product in product_list:
                    product['productid'] = product.pop('_id')
                user_list = json.loads(User.objects().all().to_json(ensure_ascii=False))
                for user in user_list:
                    user['account'] = user.pop('_id')
                data['product_list'] = product_list
                data['user_list'] = user_list
                return HttpResponse(json.dumps({'data': [data]}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 终止项目及子任务
    def stop(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(projectid=data['project']).first()
                for task in project.tasks:
                    task.modify(status='终止', expstatus='终止', anastatus='终止', jiedu_status='终止')
                project.modify(status='终止')
                message['success'] = '该项目已终止'
                return HttpResponse(json.dumps(message, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 为项目添加患者（将采取同样的下单方式）
    def addpatient(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                warning = []
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['projectid']).first()
                tumortypes = project.tumortype.split()
                patients = set(data['patients'].split())
                for patient in data['patients'].split():
                    if len(Patient.objects(pk=patient)) == 0:
                        warning.append(patient)
                        patients.remove(patient)
                data['patients'] = list(patients)
                for product in project.products:
                    for patient in data['patients']:
                        if len(tumortypes) != 0:
                            for tumortype in tumortypes:
                                patient=Patient.objects(pk=patient).first()
                                task=GenerateTask(patient,product,tumortype)
                                patient.modify(taskstatus='有')
                                project.patients.append(patient)
                                project.tasks.append(task)
                        else:
                            patient = Patient.objects(pk=patient).first()
                            task = GenerateTask(patient,product,'')
                            patient.modify(taskstatus='有')
                            project.patients.append(patient)
                            project.tasks.append(task)
                project.save()
                message['success'] = '保存成功'
                if len(warning) != 0:
                    message['warning'] = '以下患者出现问题，可能不存在：%s' % (','.join(set(warning)))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def pay(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['projectid']).first()
                try:
                    project.modify(status='已付费/免费')
                    for task in project.tasks:
                        starttime = datetime.datetime.now()
                        bestuptime = datetime.datetime.now() + datetime.timedelta(days=task.product.bestuptime)
                        worstuptime = datetime.datetime.now() + datetime.timedelta(days=task.product.worstuptime)
                        task.modify(status='进行',
                                    expstatus='开始',
                                    anastatus='wait',
                                    jiedu_status='wait',
                                    starttime=starttime,
                                    bestuptime=bestuptime,
                                    worstuptime=worstuptime)
                    message['success'] = '缴费并成功下单'
                except Exception as e:
                    message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def pause(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['project']).first()
                try:
                    for task in project.tasks:
                        task.modify(status='暂停', jiedu_status='暂停', expstatus='暂停', anastatus='暂停')
                    project.status = '暂停'
                    message['success']='项目及其子项目暂停成功'
                except Exception as e:
                    message['error'] = e
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def reset(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def view(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                message = {}
                project_list = Project.objects().all()
                for project in project_list:
                    if project.status not in ['提交', '暂停']:
                        try:
                            project.duration = (project.deadline - datetime.datetime.now()).days
                            if project.duration < 0:
                                project.delay = '是'
                            project.save()
                        except Exception as e:
                            message['error'] = e
                project_list = json.loads(project_list.to_json(ensure_ascii=False))
                new_project_list = []
                for project in project_list:
                    project['projectid'] = project.pop('_id')
                    if project.get('tag', None):
                        new_project_list.append(project)
                for project in new_project_list:
                    patient_list = []
                    product_list = []
                    task_list = []
                    for patient in project.get('patients', []):
                        patient = json.loads(Patient.objects(pk=patient).first().to_json(ensure_ascii=False))
                        patient_list.append(patient)
                    for product in project.get('products', []):
                        product = json.loads(Product.objects(pk=product).first().to_json(ensure_ascii=False))

                        product_list.append(product)
                    for task in project.get('tasks', []):
                        task = json.loads(Task.objects(pk=task).first().to_json(ensure_ascii=False))
                        task['taskid'] = task.pop('_id')
                        task['patientname'] = Task.objects(pk=task['taskid']).first().patient.patientname
                        task_list.append(task)
                    project['patient_list'] = patient_list
                    project['product_list'] = product_list
                    project['task_list'] = task_list
                # return render(request,'ProjectManager/project/project.html',locals())
                return HttpResponse(json.dumps({'data': new_project_list}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def tmp(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                pass
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def cancel(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['project']).first()
                if data['cmd'] == '取消实验':
                    try:
                        for task in project.tasks:
                            task.modify(expstatus='无', anastatus='开始')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
                if data['cmd'] == '取消解读':
                    try:
                        for task in project.tasks:
                            task.modify(expstatus='无', anastatus='开始')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class PatientHandle(Handle):
    '''
    患者处理器
    '''
    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                patient_list = Patient.objects().all()
                patient_list = json.loads(patient_list.to_json(ensure_ascii=False))
                for patient in patient_list:
                    patient['patientid'] = patient.pop('_id')
                    samples = json.loads(Sample.objects(patient=patient['patientid']).all().to_json(ensure_ascii=False))
                    patient['samples'] = samples
                return HttpResponse(json.dumps({'data': patient_list}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
# 生成患者
    def init(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if len(Patient.objects(**data)) == 0:
                    try:
                        patient = Patient(**data)
                        patient.save()
                        message['success'] = '保存成功'
                        # return redirect(reverse('projectmanager:patient_detail',args=[patient]))
                    except Exception as e:
                        message['error'] = str(e)
                else:
                    message['warning'] = '该患者编号已存在'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
# 导入患者
    def batchadd(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'],self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    try:
                        fail = []
                        warn = []
                        data = pd.read_excel(f, header=0, sheetname=0, dtype=str)
                        for i in data.index:
                            row = data.loc[i].to_dict()
                            if len(Patient.objects(patientid=row['patientid'])) == 0:
                                try:
                                    patient = Patient(**row)
                                    patient.save()
                                except Exception as e:
                                    message['error'] = e
                                    fail.append(row['patientid'] + row['patientname'])
                            else:
                                warn.append(row['patientid'])
                        message['warning'] = '以下患者编号已存在：%s' % ' '.join(warn)
                        message['error'] = '以下患者保存失败：%s' % ' '.join(fail)
                    except Exception as e:
                        message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
# 添加项目
    def addproject(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                patient = Patient.objects(pk=data['patientid']).first()
                data['projectid']=GenerateID(Project)
                tasks = []
                starttime = datetime.datetime.now()
                prodeadline = starttime
                products=[]
                for product in data['products']:
                    for tumortype in data['tumortype'].split():
                        task = GenerateTask(patient,product,tumortype)
                        _product = Product.objects(pk=product).first()
                        deadline = starttime + datetime.timedelta(days=_product.worstuptime)
                        prodeadline = max(deadline, prodeadline)
                        products.append(_product)
                        tasks.append(task)
                logging.debug(tasks)
                project=Project.objects(pk=data['projectid']).first()
                duty=User.objects(pk=data['account']).first()
                project.modify(
                    # pk=data['projectid'],
                                  patients=[patient],
                                  products=products,
                                  tasks=tasks,
                                  status='已付费',
                                  duty=duty,
                                  start_time=starttime,
                                  deadline=prodeadline,
                                  tag=data['tag']
                                  )
                project.save()
                message['success'] = '保存成功'
                patient.modify(taskstatus='有')

            elif request.method == "GET":
                data = {}
                product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
                for product in product_list:
                    product['productid'] = product.pop('_id')
                user_list = json.loads(User.objects().all().to_json(ensure_ascii=False))
                for user in user_list:
                    user['account'] = user.pop('_id')
                data['product_list'] = product_list
                data['user_list'] = user_list
                return HttpResponse(json.dumps({'data': data}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
# 添加到项目
    def add2project(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['projectid']).first()
                patient = Patient.objects(pk=data['patientid']).first()
                project.patients.append(patient)
                tumortypes=project.tumortype.split()
                for product in project.products:
                    if len(tumortypes) !=0:
                        for tumortype in tumortypes:
                            try:
                                task = GenerateTask(patient,str(product),tumortype)
                                task = Task.objects(pk=task).first()
                                project.tasks.append(task)
                            except Exception as e:
                                logging.debug(e)
                                message['error'] = str(e)
                    else:
                        try:
                            task = GenerateTask(patient, str(product), '')
                            task = Task.objects(pk=task).first()
                            project.tasks.append(task)
                        except Exception as e:
                            logging.debug(e)
                            message['error'] = str(e)
                project.save()
                message['success'] = '添加患者到项目中成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class SampleHandle(Handle):
    '''样本处理器'''
    def init(self,request):
        '''
        添加样本
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            warning=[]
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if len(Patient.objects(pk=data['patient']['patientid'])) == 0:
                    patient = Patient(**data['patient']).save()
                    for sample in data['samples']:
                        if len(Sample.objects(pk=sample['sampleid'])) == 0:
                            sample['patient'] = patient
                            Sample(**sample).save()
                        else:
                            warning.append(sample['sampleid'])
                    message['warning'] = "以下样本编号已存在： %s" % ','.join(warning)
                else:
                    message['error'] = '该患者编号已存在'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def add(self,request):
        '''
        补充样本，好像没啥用
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                patient= Patient.objects(data['patientid']).first()
                try:
                    pass
                except Exception as e:
                    logging.debug(e)
                    message['error']=str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def complete(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                try:
                    sample = Sample(**data)
                    sample.save()
                    message['success']='保存成功'
                except Exception as e:
                    logging.debug(e)
                    message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                sample_list = Sample.objects().all().to_json(ensure_ascii=False)
                return HttpResponse(sample_list)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class ProductHandle(Handle):
    '''产品处理器'''
    def add(self,request):
        '''
        添加或者修改产品
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                try:
                    product = Product(**data)
                    product.save()
                    message['sucess'] = '产品保存/修改成功'
                except Exception as e:
                    logging.debug(e)
                    message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
                for product in product_list:
                    product['productid'] = product.pop('_id')
                return HttpResponse(json.dumps({'data': product_list}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))


groups=['项目管理','实验室管理','信息分析师']
for group in groups:
    Group(name=group).save()

check=False
# autotaskhandle=AutoTaskHandle()

group=['实验室管理']
samplehandle=SampleHandle(group,check)
labtaskhandle=LabTaskHandle(group,check)

group=['项目管理']
projecthandle=ProjectHandle(group,check)
pmtaskhandle=PMTaskHandle(group,check)
producthandle=ProductHandle(group,check)
group = ['项目管理','实验室管理']
tmp='tmp'
patienthandle=PatientHandle(group,check,tmp)
group = ['信息分析师']
anataskhandle=AanaTaskHandle(group,check)