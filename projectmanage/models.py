from mongoengine import *

connect('test')
# Create your models here.
# 产品
class Product(Document):
    productid = StringField(primary_key=True)
    productname = StringField(default='')
    book=StringField(default='')
    config = StringField(default='')
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
    type=StringField(default='') # 样品类型
    recievetime=DateTimeField()# 收样时间
    def __str__(self):
        return self.pk
# 患者
class Patient(Document):
    patientid=StringField(max_length=30,primary_key=True)
    patientname=StringField(default='')
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
    explant=StringField(default='')
    hospital=StringField(default='')
    sales=StringField(default='')
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
    status = StringField(default='wait')
    expstatus = StringField(default='wait')
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
    tasks=ListField(ReferenceField(Task))
    duty=StringField(null=True)
    status=StringField(default='待审查',choice=['待审查','未缴费','已付费/免费','已完成','暂停','已作废'])
    start_time=DateTimeField(null=True)
    deadline = DateTimeField(null=True)
    remain=IntField(null=True)
    finish=DateTimeField(null=True)
    delay = StringField(default='否')
    def __str__(self):
        return self.pk
# 实验编号
class Experiment(Document):
    expid=StringField(primary_key=True)
    patient=ReferenceField(Patient)
    product=ReferenceField(Product)
    samples=ListField(ReferenceField(Sample))
    def __str__(self):
        return self.pk
# 提取
class Extraction(Document):
    sampleid=StringField(primary_key=True)
    type=StringField(default='')
    extraction_volume=FloatField(default=0)
    s260280=StringField(default='')
    s260230=StringField(default='')
    take3=StringField(default='')
    QB=StringField(default='')
    mass=StringField(default='')
    RQN=StringField(default='')
    DV200=StringField(default='')
    s2818=StringField(default='')
    qualify=StringField(default='')
    operator1=StringField(default='')
    operator2=StringField(default='')
    remaining_mass=StringField(default='')
    reagent=StringField(default='')
    lot=StringField(default='')
    location=StringField(default='')
    time=DateTimeField(auto_now=True)
    remarks=StringField(default='')
    def __str__(self):
        return self.pk
# 建库
class Library(Document):
    sampleid=StringField(primary_key=True)
    I5=StringField(default='')
    I7=StringField(default='')
    DNA_volume=StringField(default='')
    complement_volume=StringField(default='')
    input_mass=StringField(default='')
    second_strand_QB=StringField(default='')
    second_strand_mass=StringField(default='')
    postligation_QB=StringField(default='')
    postligation_mass=StringField(default='')
    Pre_PCR_cycle=StringField(default='')
    library_volume=StringField(default='')
    library_QB=StringField(default='')
    library_mass=StringField(default='')
    amplify_ratio=StringField(default='')
    qseqpeak=StringField(default='')
    qualify=StringField(default='')
    reagent=StringField(default='')
    lot=StringField(default='')
    operator1=StringField(default='')
    operator2=StringField(default='')
    remaining_mass=StringField(default='')
    location=StringField(default='')
    time1=StringField(default='')
    time2=StringField(default='')
    info=StringField(default='')
    def __str__(self):
        return self.pk
# 杂交
class Hybridization(Document):
    expid=StringField(primary_key=True)
    experiment_panel=StringField(default='')
    datasize=StringField(default='')
    lot=StringField(default='')
    input_volume=StringField(default='')
    input_mass=StringField(default='')
    postPCR_cycle=StringField(default='')
    postPCRQB=StringField(default='')
    postPCRvolume=StringField(default='')
    amplify_ratio=StringField(default='')
    qualify=StringField(default='')
    operator1=StringField(default='')
    operator2=StringField(default='')
    location=StringField(default='')
    time1=StringField(default='')
    time2=StringField(default='')
    remarks=StringField(default='')
    def __str__(self):
        return self.pk
# 质控
class QualityControl(Document):
    expid=StringField(primary_key=True)
    postid=StringField(default='')
    Qseppeak=StringField(default='')
    qPCR_concentration=StringField(default='')
    qPCRQB=StringField(default='')
    qPCRreagent=StringField(default='')
    lot=StringField(default='')
    qualify=StringField(default='')
    operator1=StringField(default='')
    operator2=StringField(default='')
    location=StringField(default='')
    remarks=StringField(default='')
    time=StringField(default='')
    def __str__(self):
        return self.pk
# 测序
class Sequencing(Document):
    expid=StringField(primary_key=True)
    dilutionRatio=StringField(default='')
    postdilutionConcentration=StringField(default='')
    def __str__(self):
        return self.pk

