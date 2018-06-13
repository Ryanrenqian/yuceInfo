from mongoengine import *

connect('test')
# Create your models here.


class Product(Document):
    productid = StringField(primary_key=True)
    productname = StringField(max_length=30)
    book=StringField(default='')
    config = StringField(max_length=30)
    period = IntField(default=5)
    normaltype = StringField(default='')
    normalsize = StringField(default='')
    tumortype = StringField(default='')
    tumorsize = StringField(default='')
    platform = StringField(default='')
    bestuptime=IntField(default=0)
    worstuptime=IntField(default=0)
    chip = StringField(default='')
    strategy = StringField(default='')
    moletag = StringField(default='')
    def __str__(self):
        return self.pk

# 样本
class Sample(Document):
    sampleid=StringField(primary_key=True)# 样本编号
    patient=StringField(default='') # 患者编号
    tumortype=StringField(default='') # 肿瘤类型
    flag=StringField(default='') # 标记
    tissue=StringField(default='') # 组织类型
    type = StringField(default='') #
    create_time=DateTimeField(auto_now=True)
    i5=StringField(default='') #
    i7=StringField(default='')
    volume=IntField(default=0)
    concentration=StringField(default='')
    QsepPeak=StringField(default='') #
    qPCRConcentration=StringField(default='')#qPCR浓度
    datasize=IntField(default=0) #测序数据量
    read1=StringField(default='')
    read2=StringField(default='')
    platform=StringField(default='') # 测序平台
    info=StringField(default='') # 备注
    def __str__(self):
        return self.pk

# 患者
class Patient(Document):
    patientid=StringField(max_length=30,primary_key=True)
    patientname=StringField(max_length=30)
    tumortype = StringField(default='')
    samples = ListField(ReferenceField(Sample))
    age=IntField(default=0)
    gender=StringField(default='')
    infostatus=StringField(default='无')
    samplestatus = StringField(default='无')
    taskstatus = StringField(default='无')
    level=StringField(default='')
    relative=StringField(default='')
    smoker=StringField(default='')
    PDL1=StringField(default='')
    MSIMMR=StringField(default='')
    sugery=StringField(default='')
    chemshistory=StringField(default='')
    targethistory=StringField(default='')
    immuhistory=StringField(default='')
    immudrug=StringField(default='')
    immutime=DateTimeField(null=True)
    explant=StringField(default='')
    explanttime=DateTimeField(null=True)
    def __str__(self):
        return self.patientid

# 任务
class Task(Document):
    # 下单部分
    taskid=StringField(primary_key=True)
    product=ReferenceField(Product,null=True)
    patient=ReferenceField(Patient,null=True)
    tumor=StringField(default='')
    # 下单信息部分
    chip = StringField(default='')
    strategy = StringField(default='')
    moletag = StringField(default='')
    bestuptime=DateTimeField(null=True)
    worstuptime=DateTimeField(null=True)
    normaltype = StringField(default='')
    normalsize = StringField(default='')
    tumortype = StringField(default='')
    tumorsize = StringField(default='')
    platform = StringField(default='')
    # 任务信息部分
    starttime = DateTimeField(null=True)
    deadline=DateTimeField(null=True)
    status = StringField(default='')
    expstatus = StringField(default='开始')
    anastatus = StringField(default='wait')
    jiedu_status = StringField(default='wait')
    reportstatus = StringField(default='wait')
    info = StringField(default='')
    extrainfo = StringField(default='')
    # 数据分析部分
    samples = ListField(ReferenceField(Sample),null=True)
    config = StringField(default='')
    analyst= StringField(default='')
    parser=StringField(default='')
    checker=StringField(default='')
    report=StringField(default='')
    def __str__(self):
        return str(self.pk)

# 项目
class Project(Document):
    projectid=StringField(primary_key=True)
    tag=StringField(default='检测')
    products = ListField(ReferenceField(Product))
    patients= ListField(ReferenceField(Patient))
    tumortype=StringField(default='')
    tasks=ListField(ReferenceField(Task))
    institute=StringField(default='')
    duty=StringField(null=True)
    status=StringField(default='待审查',choice=['待审查','未缴费','已付费/免费','已完成','暂停','已作废'])
    start_time=DateTimeField(null=True)
    deadline = DateTimeField(null=True)
    duration=IntField(null=True)
    finish=DateTimeField(null=True)
    delay = StringField(default='否')
    info=StringField(default='')
    def __str__(self):
        return self.pk

