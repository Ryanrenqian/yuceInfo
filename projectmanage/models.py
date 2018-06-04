from mongoengine import *

connect('test')
# Create your models here.

# 群组
class Group(Document):
    name=StringField(primary_key=True)
    def __str__(self):
        return self.name

# 用户
class User(Document):
    account=StringField(primary_key=True)
    password=StringField(null=True)
    name = StringField(null=True)
    region=StringField(null=True)
    email=StringField(null=True)
    telephone=StringField(null=True)
    group=ReferenceField(Group,null=True)
    def __str__(self):
        return self.account

# 产品
class Product(Document):
    productid = StringField(primary_key=True)
    productname = StringField(max_length=30)
    book=StringField()
    config = StringField(max_length=30)
    period = IntField()
    normaltype = StringField(default=' ')
    normalsize = StringField(default=' ')
    tumortype = StringField(default=' ')
    tumorsize = StringField(default=' ')
    platform = StringField(default=' ')
    bestuptime=IntField(default=0)
    worstuptime=IntField(default=0)
    chip = StringField(default=' ')
    strategy = StringField(default=' ')
    moletag = StringField(default=' ')
    def __str__(self):
        return self.pk

# 样本
class Sample(Document):
    sampleid=StringField(primary_key=True)
    patient=StringField(null=True)
    tumortype=StringField(null=True)
    tissue=StringField(null=True)
    lane = DictField(null=True)
    type = StringField(null=True)
    description = StringField(null=True)
    create_time=DateTimeField(auto_now=True)
    i5=StringField(null=True)
    i7=StringField(null=True)
    volume=IntField(null=True)
    concentration=StringField(null=True)
    QsepPeak=StringField(null=True)
    qPCRConcentration=StringField(null=True)
    datasize=IntField(null=True)
    read1=StringField(null=True)
    reads=StringField(null=True)
    platform=StringField(null=True)
    datapath=StringField(null=True)
    info=StringField(null=True)
    def __str__(self):
        return self.pk

# 患者
class Patient(Document):
    patientid=StringField(max_length=30,primary_key=True)
    patientname=StringField(max_length=30)
    tumortype = StringField(null=True)
    samples = ListField(ReferenceField(Sample))
    age=IntField()
    gender=StringField()
    infostatus=StringField(default='无',choices=['有','无'])
    samplestatus = StringField(default='无',choices=['有', '无'])
    taskstatus = StringField(default='无',choices=['有', '无'])
    level=StringField(null=True)
    relative=StringField(choices=['未知','否','是'],null=True)
    smoker=StringField(null=True,choices=['未知','不吸烟','轻度','重度'])
    PDL1=StringField(choices=['未知','是','否'],null=True)
    MSIMMR=StringField(choices=['未知','否','是'],null=True)
    sugery=StringField(choices=['未知','否','是'],null=True)
    chemshistory=StringField(null=True,choices=['未知','无','术后辅助','一线','二线','三线'])
    targethistory=StringField(null=True,choices=['未知','无','有'])
    immuhistory=StringField(null=True,choices=['未知','有','无'])
    immudrug=StringField(null=True)
    immutime=DateTimeField(null=True)
    explant=StringField(null=True,choices=['未知','有','无'])
    explanttime=DateTimeField(null=True)
    def __str__(self):
        return self.patientid

# 任务
class Task(Document):
    # 下单部分
    taskid=StringField(primary_key=True)
    product=ReferenceField(Product,null=True)
    patient=ReferenceField(Patient,null=True)
    tumor=StringField(null=True)
    # 下单信息部分
    chip = StringField(null=True)
    strategy = StringField(null=True)
    moletag = StringField(null=True)
    bestuptime=DateTimeField(null=True)
    worstuptime=DateTimeField(null=True)
    normalSampletype = StringField(default='')
    normalSamplesize = StringField(default='')
    tumorSampletype = StringField(default='')
    tumorSamplesize = StringField(default='')
    platform = StringField(null=True)
    # 任务信息部分
    starttime = DateTimeField(null=True)
    deadline=DateTimeField(null=True)
    status = StringField(null=True)
    expstatus = StringField(default='开始')
    anastatus = StringField(default='wait')
    jiedu_status = StringField(default='wait')
    reportstatus = StringField(default='wait')
    info = StringField(default='')
    extrainfo = StringField(default='')
    # 数据分析部分
    samples = ListField(ReferenceField(Sample),null=True)
    config = DictField(null=True)
    analyst= StringField(null=True)
    jiedu=StringField(null=True)
    report=StringField(null=True)
    def __str__(self):
        return str(self.pk)

# 项目
class Project(Document):
    projectid=StringField(primary_key=True)
    tag=StringField(default='检测',null=True)
    products = ListField(ReferenceField(Product))
    patients= ListField(ReferenceField(Patient))
    tumortype=StringField(default='')
    tasks=ListField(ReferenceField(Task),default=[])
    institute=StringField(null=True)
    duty=ReferenceField(User,null=True)
    status=StringField(default='待审查',choice=['待审查','未缴费','已付费/免费','已完成','暂停','已作废'])
    start_time=DateTimeField(null=True)
    deadline = DateTimeField(null=True)
    duration=IntField(null=True)
    finish=DateTimeField(null=True)
    delay = StringField(default='否')
    def __str__(self):
        return self.pk

