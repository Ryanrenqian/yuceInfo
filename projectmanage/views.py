from django.shortcuts import HttpResponse,reverse,render,redirect
from django.http import StreamingHttpResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime,json,random,string,logging,os,smtplib,ldap
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

configpath='/mnt/nfs/pipeline/yucemed/modular/config/' # 设置config文件默认目录

# 可复用代码区
def GenerateTask(patient,product,tumortype,configoath=configpath):
    '''
    自动生成task
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
                config=os.path.join(configpath,product.config)
                )
    return task

def handle_uploaded_file(f,tmp):
    '''
    上传的文件处理
    :param f:
    :param tmp:
    :return:
    '''
    file=os.path.join(tmp,f.name)
    with open(file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file

def normalizejson(data):
    '''
    标准化处理不合格的json格式，需要设置对应的workdir
    :param data:
    :return:
    '''
    data_list=[]
    for key in data.keys():
        _data={'key':key}

        for i,value in enumerate(data[key]):
            _data['key'+str(i)]=value
        data_list.append(_data)
    return data_list

# 组件功能部分

# LDAP 数据获取
class Ldapc:
    '''
    从ldap获取用户信息，和分组信息
    '''
    def __init__(self,host):
        self.host=host
        self.con=ldap.initialize(self.host)
    def getGroupUsers(self,group):
        rawdata=self.con.search_s('cn=%s,ou=Roles,DC=nodomain'%group,ldap.SCOPE_SUBTREE,attrlist=['memberUid'])[0][1]['memberUid']
        users=[]
        for item in rawdata:
            users.append(item.decode('utf-8'))
        return users
    def getUsers(self,user):
        rawdata=self.con.search_s('ou=People,DC=nodomain', ldap.SCOPE_SUBTREE, attrlist=['memberUid', 'mail'])
        pass

ldapc=Ldapc('ldap://192.168.1.211:389')

class Handle:
    '''
    处理器父类：提供权限检查和临时文件存储支持
    '''
    def __init__(self, groups, check,ldapc=ldapc,tmp=None,workdir=None):
        '''
        初始化
        :param group:
        :param check:
        :param tmp:
        '''
        self.groups = groups
        self.check = check
        self.ldapc=ldapc
        self.tmp=tmp
        self.workdir=workdir

    def is_valid(self, request):
        if not self.check:
            return True
        else:
            for group in self.groups:
                if group in request.session['groups']:
                    return True
            return False

    @property
    def checktmp(self):
        if not os.path.exists(self.tmp):
            return os.mkdir(self.tmp)
        return True

class Email:
    '''
    发送邮件功能
    '''
    def __init__(self,host,port,account,password):
        self.host=host
        self.port=port
        self.account=account
        self.password=password
        self.smtpobj=smtplib.SMTP()
        self.smtpobj.connect(self.host,self.port)
        self.smtpobj.login(self.account,self.password)
    def send(self,receiver,content=None,file=None):
        message=MIMEMultipart()
        message['From'] = Header(self.account,'utf-8')
        message['To'] = Header(receiver,'utf-8')
        message['Subject']= Header(content['subject'],'utf-8')
        message.attach(MIMEText(content['content'],'plain', 'utf-8'))
        if file:
            att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="%s"'%file.split('/')[-1]
            message.attach(att1)
            try:
                self.smtpobj.sendmail(self.account,receiver,message.as_string())
                return '邮件发送成功'
            except Exception as e:
                return str(e)

# 不同组权限功能部分
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
    def cmd(self,request):
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
                elif data['cmd']=='加急':
                    pass
                elif data['cmd'] =='删除':
                    task.delete()
                    message['success']='删除成功'
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
                    task.modify(status='进行', expstatus='开始', anastatus='等待', jiedu_status='等待', reportstatus='等待',info=info)
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
                # data['starttime']=datetime.datetime.strptime(data['starttime'], '%Y-%m-%d %H:%M:%S')
                # data['deadline'] = datetime.datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S')
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
                # task_list = [task for task in task_list if task.get('starttime')]
                for task in task_list:
                    patient=Patient.objects(pk=task.get('patient')).first()
                    product = Product.objects(pk=task.get('product')).first()
                    task['productname']=product.productname
                    task['taskid'] = task.pop('_id')
                    task['patientname'] = patient.patientname
                    task['age']=patient.age
                    task['gender'] = patient.gender
                    task['deadline'] = datetime.datetime.fromtimestamp(task['deadline']['$date'] / 1000).strftime(
                        '%Y-%m-%d %H:%M:%S')
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
                                jiedu_status='终止',
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
                        task.modify(jiedu_status='无', reportstatus='无')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 任务分配
    def allocate(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task=Task.objects(pk=data['taskid']).first()
                task.modify(**data)
                message['success']='任务分配成功'
            elif request.method == 'GET':
                data={}
                data['analyst']=self.ldapc.getGroupUsers('Analyst')
                data['parser']=self.ldapc.getGroupUsers('Interpreter')
                return HttpResponse(json.dumps(data,ensure_ascii=False))
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
                    for sample in task.samples:
                        experiment=Experiment.objects(pk=sample).first()
                        experiment.modify(status='暂停')
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
                    task.modify(
                        starttime=starttime, deadline=deadline,
                        bestuptime=bestuptime, worstuptime=worstuptime,
                        status='开始', expstatus='开始')
                    message['success'] = '实验重启成功'
                elif cmd=='完成':
                    task.modify(expstatus='完成',anastatus='开始',**data)
                    message['success']='已完成'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def order(self, request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                for task in data:
                    experiments=[]
                    lanes=task['lane'].split(',')
                    for key,lane in zip(['normal','tumor','extra'],lanes):
                        if lane !='':
                            expid=task[key]+lane

                            exp=Experiment(
                                pk=expid,task=task['task'],
                                sampleid=task[key],lane=lane,
                                point=task['point'])
                            experiments.append(exp)
                            exp.save()
                            if task['point'] =='提取':
                                if Extraction.objects(pk=exp.sampleid).first() == None:
                                    Extraction(pk=exp.sampleid).save()
                            elif task['point'] =='建库':
                                if Library.objects(pk=exp.sampleid).first() == None:
                                    Library(pk=exp.sampleid).save()
                            elif task['point'] == '杂交':
                                if Hybridization.objects(pk=exp.pk).first() == None:
                                    Hybridization(pk=exp.pk).save()
                            elif task['point'] == '上机':
                                if Sequencing.objects(pk=exp.pk).first() == None:
                                    Sequencing(pk=exp.pk).save()
                            exp.modify(status='进行')
                    task=Task.objects(pk=task['task']).first()
                    task.modify(status='进行',expstatus='进行',anastatus='待投递',experiments=experiments)
                    message['success']='下单成功'
                return HttpResponse(json.dumps(message, ensure_ascii=False))
            elif request.method == 'GET':
                data={}
                task_list=[]
                for task in Task.objects(expstatus='开始').all():
                    item={}
                    item['task']=task.pk
                    item['patient']=str(task.patient)
                    item['lane']=task.product.lane
                    item['normal']=''
                    item['tumor']=''
                    item['extra']=''
                    item['samples']=[str(i) for i in task.patient.samples]
                    item['point']=''
                    task_list.append(item)
                points=['提取','建库','杂交','质控','上机']
                data['task_list']=task_list
                data['points']=points
                return HttpResponse(json.dumps(data,ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def download(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
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
            if request.method == 'POST':
                task_list = json.loads(Task.objects().all().to_json(ensure_ascii=False))
                for task in task_list:
                    task['taskid']=task.pop('_id')
                    task['samples']=','.join(task.get('samples',[]))
                return HttpResponse(json.dumps(task_list,ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    # 暂停分析
    # def pause(self,request):
    #     message = {}
    #     if self.is_valid(request):
    #         if request.method == 'POST':
    #             data = json.loads(request.body.decode('utf-8'))
    #             task=Task.objects(pk=data['taskid']).first()
    #             data['info']=data.get('info','')+task.info
    #             try:
    #                 task.modify(**data)
    #                 message['success']='暂停成功'
    #             except Exception as e:
    #                 logging.debug(e)
    #                 message['error']=str(e)
    #     else:
    #         message['warning'] = '对不起，您没有权限'
    #     return HttpResponse(json.dumps(message, ensure_ascii=False))
    def qcview(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task=Task.objects(pk=data['taskid']).first()
                data = {}
                workdir = os.path.join(self.workdir, task.pk)
                qcpath = os.path.join(workdir, 'qc')
                if os.path.exists(qcpath):
                    for root, dirs, files in os.walk(qcpath):
                        for file in files:
                            if file.endswith('fqcheck.json'):
                                data['fqcheck'] = json.loads(open(os.path.join(root, file), 'r').read())
                                data['fqcheck'] = normalizejson(data['fqcheck'])
                            elif file.endswith('qualimm.json'):
                                data['qualimm'] = json.loads(open(os.path.join(root, file)).read())
                                data['qualimm'] = normalizejson(data['qualimm'])
                smpath = os.path.join(workdir, 'somatic/pairs_qc')
                if os.path.exists(smpath):
                    for root, dirs, files in os.walk(smpath):
                        for file in files:
                            if file.endswith('.pairs.txt'):
                                lines = {}
                                with open(os.path.join(root, file), 'r') as f:
                                    for i, line in enumerate(f.readlines()):
                                        lines[i] = line.split('\t')
                                        if i == 2:
                                            break
                                data['pairqc'] = lines
                                data['pairqc'] = normalizejson(data['pairqc'])
                ascpath = os.path.join(workdir, 'somatic/ascatngs')
                if os.path.exists(ascpath):
                    ascat={}
                    for root, dirs, files in os.walk(ascpath):
                        for file in files:
                            if file.endswith('.png'):
                                imgpath = os.path.join(root, file)
                                data['ascat'].setdefault('imgs', []).append(
                                    reverse('YuceInfo:imageview', args=[imgpath]))
                            if file.endswith('.samplestatistics.txt'):
                                ascat['file'] = {}
                                lines = {}
                                with open(os.path.join(root, file), 'r') as f:
                                    for i, line in enumerate(f.readlines()):
                                        lines[i] = line.split()
                                ascat['file'] = normalizejson(lines)
                    data['ascat'] = ascat
                mutpath=os.path.join(workdir,'somatic/overlap')
                if os.path.exists(mutpath):
                    for root, dirs, files in os.walk(mutpath):
                        for file in files:
                            if file.endswith('.snv.sindel.AAchange.xls'):
                                tablepath = os.path.join(root,file)
                                data['mutation']=reverse('YuceInfo:tableview',args=[tablepath])
                                break
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def modify(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task=Task.objects(pk=data['taskid']).first()
                task.modify(anastatus='待投递',**data)
                message['success']='修改成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def review(self, request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                task = Task.objects(pk=data['taskid']).first()
                if data['cmd']=='暂停':
                    task.modify(anastatus='暂停',status='暂停')
                    message['success']='暂停成功'
                if data['cmd']== '通过':
                    task.modify(anastatus='完成',jiedu_status='开始')
                    message['success'] = '暂停成功'
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

class JieduTaskHandle(TaskHandle):

    def view(self, request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                task_list = json.loads(Task.objects().all().to_json(ensure_ascii=False))
                for task in task_list:
                    task['taskid'] = task.pop('_id')
                    task['samples'] = ','.join(task.get('samples', []))
                return HttpResponse(json.dumps(task_list, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def detailview(self,request):
        message = {}
        if self.is_valid(request):
                if request.method == 'POST':
                    data = json.loads(request.body.decode('utf-8'))
                    task = Task.objects(pk=data['taskid']).first()
                    mutpath = os.path.join(workdir, 'somatic/overlap')
                    data = {}
                    if os.path.exists(mutpath):
                        for root, dirs, files in os.walk(mutpath):
                            for file in files:
                                if file.endswith('.snv.sindel.AAchange.xls '):
                                    tablepath = os.path.join(root, file)
                                    data['mutation'] = reverse('YuceInfo:tableview', args=[tablepath])
                                    break
                    return HttpResponse(json.dumps(data,ensure_ascii=False))
                else:
                    message['error']='POST method please～'
        else:
            message['error']='对不起，您没有权限～'
        return HttpResponse(json.dumps(message,ensure_ascii=False))

    def upload(self,request):
        message={}
        if self.is_valid(request):
            if request.method == 'POST':
                data=json.loads(request.body.decode('utf-8'))
                taskid=data['taskid']
                checher=data['checker']
                f = handle_uploaded_file(request.FILES['file'],os.path.join(self.workdir,taskid))
                if os.path.getsize(f) == request.FILES['file'].size:
                    task=Task.objects(pk=taskid).first()
                    task.modify(report=f)
                    message['success']='上传成功'
                else:
                    message['error']='上传失败，请重试'
            elif request.method=='GET':
                data={}
                data['checker']=self.ldapc.getGroupUsers('InInterpreter')
                return HttpResponse(json.dumps(data,ensure_ascii=False))
        else:
            message['error']='对不起，你没有权限操作～'
        return HttpResponse(json.dumps(message,ensure_ascii=False))

    def download(self,request):
        def file_iterator(file_name, chunk_size=512):
            with open(file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                taskid = json.loads(request.body.decode('utf-8'))['taskid']
                task=Task.objects(pk=taskid).first
                response = StreamingHttpResponse(file_iterator(task.report))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(task.report)
                return response
        else:
            message['error'] = '对不起，你没有权限操作～'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def review(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                taskid=data['taskid']
                task = Task.objects(pk=taskid).first()
                if data['cmd'] == '通过':
                    task.modify(reportstatus = '通过审核')
                    message['success'] = '通过审核'
        else:
            message['error'] = '对不起，你没有权限操作～'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def cmd(self,request):
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
                if data['cmd']=='完成':
                    try:
                        task.modify(status='完成', jiedu_status='完成', reportstatus='完成',info=info)
                        message['success'] = '实验暂停成功'
                    except Exception as e:
                        message['error'] = str(e)
                        logging.debug(e)
        else:
            message['warning']='对不起，您没有权限'
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
                if not data.get('projectid',None):
                    project=GenerateID(Project)
                    project=Project.objects(pk=project).first()
                else:
                    project=Project(pk=data['projectid'],tag=data['tag'],duty=data['duty'],)
                    project.save()
                start_time = datetime.datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
                deadline = datetime.datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S')
                patients=[]
                products=[]
                tasks=[]
                for taski in data['task_list']:
                    patient=Patient.objects(patientid=taski['patientid']).first()
                    patient.modify(taskstatus='有')
                    patients.append(patient)
                    for product in taski['product']:
                        task = GenerateTask(patient,product,taski['tumortype'])
                        tasks.append(task)
                        product=Product.objects(pk=product).first()
                        products.append(product)
                project.modify(start_time=start_time,deadline=deadline,tasks=tasks,patients=list(set(patients)),products=products)
                message['success'] = '项目添加成功'
            else:
                data = {}
                patients=json.loads(Patient.objects().all().to_json(ensure_ascii=False))
                items=[]
                for patient in patients:
                    for tumortype in patient['tumortype'].split(';'):
                        items.append({'patientid':patient['_id'],'patientname':patient['patientname'],'tumortype':patient['tumortype'],'product':[]})
                products=[]
                product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
                for product in product_list:
                    products.append(product.pop('_id'))
                user_list=self.ldapc.getGroupUsers('Analyst')
                data['product_list'] = products
                data['user_list'] = user_list
                data['items']=items
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def complement(self,request):
        '''添加订单'''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                warning = []
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['projectid']).first()
                for taski in data['task_list']:
                    for product in taski['product']:
                        patient=Patient.objects(patientid=taski['patientid']).first()
                        patient.modify(taskstatus='有')
                        project.patients.append(patient)
                        task = GenerateTask(patient,product,taski['tumortype'])
                        project.tasks.append(task)
                        product=Product.objects(pk=product).first()
                        if product not in project.products:
                            project.products.append(product)
                project.save()
                message['success'] = '保存成功'
                if len(warning) != 0:
                    message['warning'] = '以下患者出现问题，可能不存在：%s' % (','.join(set(warning)))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def complementhelp(self,request):
        '''
        辅助下单
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data=json.loads(request.body.decode('utf-8'))
                project=Project.objects(pk=data['projectid']).first()
                patients=project.patients
                items = []
                for patient in patients:
                    for tumortype in patient.tumortype.split(';'):
                        items.append({'patientid': patient.pk,
                                      'patientname': patient.patientname,
                                      'tumortype': patient.tumortype,
                                      'product':[]})
                products = []
                product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
                for product in product_list:
                    products.append(product.pop('_id'))
                response={}
                response['items']=items
                response['product_list']=products
                response['projectid']=data['projectid']
                return HttpResponse(json.dumps(response, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def cmd(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                project = Project.objects(pk=data['projectid']).first()
                if data['cmd']=='审核':
                    project.modify(status='审核通过')
                    for task in project.tasks:
                        if task.status in ['终止','暂停','进行']:
                            continue
                        starttime = datetime.datetime.now()
                        bestuptime = datetime.datetime.now() + datetime.timedelta(days=task.product.bestuptime)
                        worstuptime = datetime.datetime.now() + datetime.timedelta(days=task.product.worstuptime)
                        task.modify(status='进行',
                                    expstatus='开始',
                                    anastatus='等待',
                                    jiedu_status='等待',
                                    starttime=starttime,
                                    bestuptime=bestuptime,
                                    worstuptime=worstuptime)
                    message['success'] = '成功下单'
                elif data['cmd']=='暂停':
                    for task in project.tasks:
                        if task.status=='终止':
                            continue
                        task.modify(status='暂停', jiedu_status='暂停', expstatus='暂停', anastatus='暂停')
                    project.modify(status = '暂停')
                    message['success']='项目及其子项目暂停成功'
                elif data['cmd']=='重置':
                    for task in project.tasks:
                        task.modify(status='等待', jiedu_status='等待', expstatus='等待', anastatus='等待')
                    project.modify(status = '待审核')
                    message['success']='项目及其子项目暂停成功'
                elif data['cmd']=='终止':
                    project.modify(status='终止')
                    for task in project.tasks:
                        task.modify(status='终止',
                                    expstatus='终止',
                                    anastatus='终止',
                                    jiedu_status='终止',
                                    reportstatus='终止')
                    message['success'] = '成功下单'
                elif data['cmd'] == '取消实验':
                    try:
                        for task in project.tasks:
                            task.modify(expstatus='无', anastatus='等待')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
                elif data['cmd'] == '取消解读':
                    try:
                        for task in project.tasks:
                            task.modify(jiedu_status='无',reportstatus='无')
                        message['success'] = '取消实验操作成功'
                    except Exception as e:
                        logging.debug(e)
                        message['error'] = str(e)
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
                        patient['patientid']=patient.pop('_id')
                        patient_list.append(patient)
                    for product in project.get('products', []):
                        product = json.loads(Product.objects(pk=product).first().to_json(ensure_ascii=False))

                        product_list.append(product)
                    for task in project.get('tasks', []):
                        task = json.loads(Task.objects(pk=task).first().to_json(ensure_ascii=False))
                        task['projectid']=project['projectid']
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
                    samples = [i.pk for i in Sample.objects(patient=patient['patientid']).all()]
                    patient['samples'] = ','.join(samples)
                return HttpResponse(json.dumps({'data': patient_list}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def init(self,request):
        '''
        生成患者
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if len(Patient.objects(**data)) == 0:
                    try:
                        patient = Patient(**data)
                        patient.save()
                        message['success'] = '保存成功'
                    except Exception as e:
                        message['error'] = str(e)
                else:
                    message['warning'] = '该患者编号已存在'
            if request.method == 'GET':
                data = {}
                data['sale'] = self.ldapc.getGroupUsers('Salesman')
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def modify(self,request):
        '''
        修改患者
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                patient=Patient.objects(pk=data.pop('patientid')).first()
                try:
                    patient.modify(infostatus='有',**data)
                    message['success'] = '修改成功'
                except Exception as e:
                    message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def batchadd(self,request):
        '''
        批量导入患者
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'],self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    try:
                        fail = []
                        warn = []
                        if f.endswith('.xlsx'):
                            data = pd.read_excel(f, header=0, sheet_name=0, dtype=str)
                        elif f.endswith('.csv'):
                            data = pd.read_csv(f, header=0, dtype=str)
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
                        if len(warn)>0 or len(fail)>0:
                            message['warning'] = '以下患者编号已存在：%s' % ' '.join(warn)
                            message['error'] = '以下患者保存失败：%s' % ' '.join(fail)
                        else:
                            message['success']='完全导入成功'
                    except Exception as e:
                        message['error'] = str(e)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def addproject(self,request):
        '''
        添加项目
        :param request:
        :return:
        '''
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
                    for tumortype in data['tumortype']:
                        task = GenerateTask(patient,product,tumortype)
                        _product = Product.objects(pk=product).first()
                        deadline = starttime + datetime.timedelta(days=_product.worstuptime)
                        prodeadline = max(deadline, prodeadline)
                        products.append(_product)
                        tasks.append(task)
                logging.debug(tasks)
                project=Project.objects(pk=data['projectid']).first()
                duty=data['account']
                project.modify(
                                  patients=[patient],
                                  products=products,
                                  tasks=tasks,
                                  status='已付费',
                                  duty=duty,
                                  start_time=starttime,
                                  deadline=prodeadline,
                                  tag=data['tag'],

                                  )
                project.save()
                message['success'] = '保存成功'
                patient.modify(taskstatus='有')
            elif request.method == "GET":
                data = {}
                product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
                for product in product_list:
                    product['productid'] = product.pop('_id')
                user_list = self.ldapc.getGroupUsers('Analyst')
                data['product_list'] = product_list
                data['user_list'] = user_list
                return HttpResponse(json.dumps({'data': data}, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def add2project(self,request):
        '''
        添加到项目
        :param request:
        :return:
        '''
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
                if len(Sample.objects(pk=data['sampleid'])) == 0:
                    sample=Sample(**data)
                    sample.save()
                    patient=Patient.objects(pk=sample.patient).first()
                    patient.samples.append(sample)
                    patient.save()
                    patient.modify(samplestatus='有')
                    message['success']='添加成功'
                else:
                    message['error']='保存失败'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self,request):
        '''
        补充样本，好像没啥用
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    fail = []
                    warn = []
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheet_name=0)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        if len(Sample.objects(pk=row['sampleid'])) == 0:
                            try:
                                sample = Sample(**row)
                                sample.save()
                                patient = Patient.objects(pk=row['patient']).first()
                                patient.samples.append(sample)
                                patient.save()
                                patient.modify(samplestatus='有')
                            except Exception as e:
                                message['error'] = e
                                fail.append(row['patientid'] + row['patientname'])
                        else:
                            warn.append(row['patientid'])
                    message['warning'] = '以下患者编号已存在：%s' % ' '.join(warn)
                    message['error'] = '以下患者保存失败：%s' % ' '.join(fail)
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def modify(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.info(str(data))
                Sample(**data).save()
                message['success']='修改成功'
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
                sample_list = json.loads(Sample.objects().all().to_json(ensure_ascii=False))
                for sample in sample_list:
                    sample['sampleid']=sample.pop('_id')
                    sample['recievetime']=int(sample['recievetime']['$date']/1000)
                return HttpResponse(json.dumps(sample_list,ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class ExperimentHandle(Handle):
    def view(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                data=json.loads(Experiment.objects.all().to_json(ensure_ascii=False))
                for i in data:
                    i['expid']=i.pop('_id')
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def cmd(self, request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.info('cmd: %s'%request.body.decode('utf-8'))
                exp = Experiment.objects(pk=data['expid']).first()
                cmd=data.pop('cmd')
                if cmd=='暂停':
                    exp.modify(status='暂停')
                    message['success'] = '暂停成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def modify(self,request):
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                logging.info(str(data))
                Sample(**data).save()
                message['success'] = '修改成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class ExtractHandle(Handle):

    def view(self,request):
        message = {}
        if self.is_valid(request):
            items=[]
            experiments = Experiment.objects().all()
            for exp in experiments:
                extract = json.loads(Extraction.objects(pk=exp.sampleid).first().to_json(ensure_ascii=False))
                if exp.point=='提取'and extract['status']=='完成':
                    exp.modify(point='建库')
                extract['sampleid']=extract.pop('_id')
                item={}
                item['expid']=exp.pk
                item['task']=exp.task.pk
                item['point']=exp.point
                item['expstatus']=exp.status
                item.update(extract)
                items.append(item)
            logging.info(str(items))
            return HttpResponse(json.dumps(items, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self,request):
        '''
        上传数据
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheetname=0, dtype=str)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        Extraction(status='完成',**row).save()
                message['success'] = '保存成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def download(self,request):
        '''下载数据'''
        message = {}
        if self.is_valid(request):
            data=[]
            for i in Extraction.objects(status='开始').all():
                item=json.loads(i.to_json(ensure_ascii=False))
                item['sampleid']=item.pop('_id')
                item.pop('status')
                logging.info(item)
                data.append(item)
            return HttpResponse(json.dumps(data, ensure_ascii=False))
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

class LibraryHandle(Handle):

    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                experiments = Experiment.objects().all()
                items=[]
                for exp in experiments:
                    library=Library.objects(pk=exp.sampleid).first()
                    if library == None and exp.point=='建库':
                        library = Library(pk=exp.sampleid)
                        library.save()
                    if library==None:
                        continue
                    library = json.loads(library.to_json(ensure_ascii=False))
                    if library['status'] == '完成' and exp.point=='建库':
                        exp.modify(point='杂交')
                    item = {}
                    item['expid']= exp.pk
                    item['task'] = exp.task.pk
                    item['point'] = exp.point
                    item['expstatus'] = exp.status
                    item['sampleid'] = exp.sampleid
                    item.update(library)
                    items.append(item)
                return HttpResponse(json.dumps(items, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self,request):
        '''
        补充样本，好像没啥用
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheet_name=0, dtype=str)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        Library(status='完成',**row).save()
                message['success'] = '保存成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def download(self,request):
        '''下载数据'''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data=[]
                for i in Library.objects(status='开始').all():
                    item = json.loads(i.to_json(ensure_ascii=False))
                    item['sampleid']=item.pop('_id')
                    item.pop('status')
                    data.append(item)
                return HttpResponse(json.dumps(data, ensure_ascii=False))

        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class HybridHandle(Handle):

    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                experiments = Experiment.objects().all()
                items=[]
                for exp in experiments:
                    hybrid=Hybridization.objects(pk=exp.sampleid).first()
                    if hybrid == None and exp.point=='杂交':
                        hybrid = Hybridization(pk=exp.sampleid)
                        hybrid.save()
                    if hybrid==None:
                        continue
                    hybrid = json.loads(hybrid.to_json(ensure_ascii=False))
                    hybrid['expid']=hybrid.pop('_id')
                    if hybrid['status'] == '完成':
                        exp.modify(point='质控')
                    # item = {}
                    # item['expid']= exp.pk
                    # item['task'] = exp.task.pk
                    # item['point'] = exp.point
                    # item['expstatus'] = exp.status
                    # item['sampleid'] = exp.sampleid
                    # # item.update(hybrid)
                    # items.append(item)
                    items.append(hybrid)
                return HttpResponse(json.dumps(items, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self,request):
        '''
        补充样本，好像没啥用
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheet_name=0, dtype=str)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        Hybridization(status='完成',**row).save()
                message['success'] = '保存成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def download(self,request):
        '''下载数据'''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data=[]
                for i in Hybridization.objects(status='开始').all():
                    item = json.loads(i.to_json(ensure_ascii=False))
                    item['expid']=item.pop('_id')
                    item.pop('status')
                    data.append(item)
                return HttpResponse(json.dumps(data, ensure_ascii=False))

        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class LabQCHandle(Handle):

    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                experiments = Experiment.objects().all()
                items=[]
                for exp in experiments:
                    qc=QualityControl.objects(pk=exp.pk).first()
                    if qc == None and exp.point=='质控':
                        qc = QualityControl(pk=exp.pk)
                        qc.save()
                    if qc==None:
                        continue
                    qc = json.loads(qc.to_json(ensure_ascii=False))
                    if qc['status'] == '完成':
                        exp.modify(point='测序')
                    item = {}
                    item['expid']= exp.pk
                    item['task'] = exp.task.pk
                    item['point'] = exp.point
                    item['expstatus'] = exp.status
                    item['sampleid'] = exp.sampleid
                    item.update(qc)
                    items.append(item)
                return HttpResponse(json.dumps(items, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self,request):
        '''
        补充样本，好像没啥用
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheet_name=0, dtype=str)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        QualityControl(status='完成',**row).save()
                message['success']='保存成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def download(self,request):
        '''下载数据'''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data=[]
                for i in QualityControl.objects(status='开始').all():
                    item = json.loads(i.to_json(ensure_ascii=False))
                    item['expid']=item.pop('_id')
                    item.pop('status')
                    data.append(item)
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class SeqHandle(Handle):

    def view(self,request):
        '''
        视图函数
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'GET':
                experiments = Experiment.objects().all()
                items=[]
                for exp in experiments:
                    seq=Sequencing.objects(pk=exp.pk).first()
                    if seq == None and exp.point=='测序':
                        seq = Sequencing(pk=exp.pk)
                        seq.save()
                    if seq ==None:
                        continue
                    seq = json.loads(seq.to_json(ensure_ascii=False))
                    seq['expid']=seq.pop('_id')
                    if seq['status'] == '完成':
                        exp.modify(point='完成')
                    # item = {}
                    # # item['expid']= exp.pk
                    # # item['task'] = exp.task.pk
                    # # item['point'] = exp.point
                    # # item['expstatus'] = exp.status
                    # # item['sample'] = exp.sampleid
                    # item.update(seq)
                    # items.append(item)
                    items.append(seq)
                return HttpResponse(json.dumps(items, ensure_ascii=False))
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def upload(self, request):
        '''
        上传
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheet_name=0, dtype=str)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        Sequencing(status='完成',**row).save()
                message['success']='保存成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

    def download(self,request):
        '''下载数据'''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                data=[]
                for i in Sequencing.objects(status='开始').all():
                    item = json.loads(i.to_json(ensure_ascii=False))
                    item['expid'] = item.pop('_id')
                    item.pop('status')
                    data.append(item)
                return HttpResponse(json.dumps(data, ensure_ascii=False))

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
                    message['success'] = '产品保存/修改成功'
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

    def batchadd(self, request):
        '''
        批量导入患者
        :param request:
        :return:
        '''
        message = {}
        if self.is_valid(request):
            if request.method == 'POST':
                f = handle_uploaded_file(request.FILES['file'], self.tmp)
                if os.path.getsize(f) == request.FILES['file'].size:
                    if f.endswith('.xlsx'):
                        data = pd.read_excel(f, header=0, sheet_name=0, dtype=str)
                    elif f.endswith('.csv'):
                        data = pd.read_csv(f, header=0, dtype=str)
                    for i in data.index:
                        row = data.loc[i].to_dict()
                        product = Product(**row)
                        product.save()
                message['success']='产品导入成功'
        else:
            message['warning'] = '对不起，您没有权限'
        return HttpResponse(json.dumps(message, ensure_ascii=False))

class FileView:
    '''
    自动化投递任务的结果展示
    '''
    def __init__(self,workdir):
        self.workdir=workdir
    def tableview(self,request,path):
        table=pd.read_table(path)
        data=table.to_json(orient='records',force_ascii=False)
        return HttpResponse(data)

    def imageview(self,request,path):
        message={}
        # filepath=os.path.join(self.workdir,path)
        if os.path.exists(path):
            return HttpResponse(open(path, 'rb').read(), content_type='image/png')
        else:
            message['error']='文件不存在'
            return HttpResponse(json.dumps(message,ensure_ascii=False))

def index(request):
    return redirect('templates/report/production/home.html')


# 启动或关闭权限
check=False

# 实验室管理部分
group=['Lab']
tmp='tmp' # 临时文件存放点
samplehandle=SampleHandle(group,check,tmp=tmp)
labtaskhandle=LabTaskHandle(group,check,tmp=tmp)
experimenthandle=ExperimentHandle(group,check,tmp=tmp)
extracthandle=ExtractHandle(group,check,tmp=tmp)
libraryhandle=LibraryHandle(group,check,tmp=tmp)
hybridhandle=HybridHandle(group,check,tmp=tmp)
labqc=LabQCHandle(group,check,tmp=tmp)
seqhandle=SeqHandle(group,check,tmp=tmp)
# 项目管理部分
group=['ProjectManager']
projecthandle=ProjectHandle(group,check)
pmtaskhandle=PMTaskHandle(group,check)


# 项目管理，实验室共同管理部分
group = ['ProjectManager','Lab']

tmp='tmp' # 设置临时上传文件存放点
patienthandle=PatientHandle(group,check,tmp=tmp)
producthandle=ProductHandle(group,check,tmp=tmp)
# 分析师管理部分
group = ['Analyst']
workdir='tmp' #设置分析目录
workdir=os.path.abspath(workdir)
anataskhandle=AanaTaskHandle(group,check,workdir=workdir)
fileview=FileView(workdir=workdir)

reportdir='tmp' # 设置报告存放地址
jiedutaskhandle=JieduTaskHandle(group,check,workdir=reportdir)