#!/mnt/cfs/med18b/med/renqian/env//anaconda3/bin/python
###################################################################
# File Name: autosample.py
# Author: renqian
# mail: renqian@yucebio.com
# Created Time: Tue 05 Jun 2018 10:46:20 AM CST
#=============================================================
import json,os,sys,time
from mongoengine import *
import pymongo
from projectmanage.models import *
from config import *
#connect database
conn = pymongo.MongoClient("127.0.0.1",27017)
connect('test')
# Create your models here.
db = conn.bclmon
col = db["samples"]
colrun = db["sequencing"]
db = conn.pipeline
projects = db["Projects"]

def taskhandle(workdir,task):
    with open(task.config,'r')as f:
        jsonobj=json.loads(f)
    jsonobj["project"]["name"] = task.taskid
    jsonobj["project"]["workdir"] = workdir+'/'+task.taskid
    try:
        os.makedirs(jsonobj["project"]["workdir"])
    except:
        pass
    jsonobj["sample"] = {}
    samplelist = []
    ctype = {}
    for sample in task.samples:
        ctype[str(sample)]=sample.tumortype
        samplelist.append(str(sample),"")
    currentrun = colrun.find({"status": {"$ne": "end"}}).sort("_id",-1).limit(1)
    for item in samplelist:
        sample = item[0]
        run = item[1]
        if run:
            if currentrun and run == currentrun[0]["name"]:
                outlist = [sample, run, "wait_data"]
            else:
                ret = col.find({"name": sample, "runname": run}).count()
                if ret:
                    outlist = [sample, run, "finished"]
                else:
                    outlist = [sample, run, "not_found"]
        else:
            if currentrun:
                outlist = [sample, currentrun[0]["name"], "wait_data"]
            else:
                ret = col.find({"name": sample}).sort("_id", -1).limit(1)
                if ret:
                    run = ret[0]["runname"]
                    outlist = [sample, run, "finished"]
                else:
                    outlist = [sample, "unknown", "not_found"]
        print("\t".join(outlist))

# insert jsonobj
    for item in samplelist:
        sample = item[0]
        jsonobj["sample"][sample] = {}
        jsonobj["sample"][sample]["description"] = sample
        jsonobj["sample"][sample]["type"] = 'raw'
        jsonobj["sample"][sample]["ctype"] = ctype[sample]
        jsonobj["sample"][sample]["lane"] = {}
        jsonobj["sample"][sample]["lane"][sample] = {}
        jsonobj["sample"][sample]["lane"][sample]["path"] = []
        sampleobj = Sample.objects(pk=sample).first()
        jsonobj["sample"][sample]["lane"][sample]["adapter"] =[sampleobj.read1,sampleobj.read2]
    gender='XX'
    if task.patient.gender=='男':
        gender='XY'
    samples=list(task.samples)
    if len(task.samples)==3:
        pairname=samples.pop(0)
    else:
        pairname=samples[1] + "-VS-" + samples[0]
        jsonobj["somatic"][pairname]={}
    jsonobj["somatic"][pairname]["description"] = ""
    jsonobj["somatic"][pairname]["normal"] = samples[0]
    jsonobj["somatic"][pairname]["tumor"] = samples[1]
    jsonobj["somatic"][pairname]["gender"] = samples[2]
    projectobj = projects.find_one({"Name" : jsonobj["project"]["name"]})
    projectnew = {
        "Name" : jsonobj["project"]["name"],
        "Project" : jsonobj["project"]["submit_project"],
        "Queue" : jsonobj["project"]["submit_queue"],
        "State" : "waitdata",
        "RootPath" : rootpath,
        "Workdir" : jsonobj["project"]["workdir"],
        "GlobalConfig" : rootpath + '/config/global',
        "DatabaseConfig" : rootpath + '/config/empty',
        "UserConfig" : rootpath + '/config/empty',
        "Priority" : 1,
        "Owner" : os.getlogin(),
        "Ownerid" : os.getuid(),
        "JSON" : json.dumps(jsonobj),
        "SampleList": samplelist
    }
    if projectobj == None:
        projects.insert(projectnew)
    else:
        if projectobj["Ownerid"] != os.getuid():
            print("This project is owned by %s. You can not modify." % projectobj["Owner"])
            sys.exit(1)
        projects.update({"_id" : projectobj["_id"]}, projectnew)

# jsonobj: json configure; projectitem: project info; projectobj: project table
    projectitem = db["Projects"].find_one({"Name" : jsonobj["project"]["name"]})
    projectobj = db[jsonobj["project"]["name"]]
    projectobj.drop()

    scriptobj = {
        "Name" : "importprj" + "_" + jsonobj["project"]["name"],
        "Program" : "template/genproject.sh",
        "Input" : '',
        "Output" : '',
        "Sample" : '',
        "Param" : jsonobj["project"]["name"],
        "Info": 'importprj',
        "Dependent" : [],
    }
    objid = projectobj.insert(scriptobj)
    return task.modify(anastatus='已自动投递')
if __name__=='__main__':
    workdir=''
    jsondir=''
    while True:
        for task in Task.objects(expstatus='上机',anastatus='wait')
            taskhandle(workdir,jsondir,task)
