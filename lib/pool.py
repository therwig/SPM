import os, sys
from glob import glob
from functions import *
from init import *

class Package():
    def __init__(self, master, name, importdir = None):
        self.master     = master
        self.base       = self.master.pooldir
        self.name       = name
        self.importdir  = importdir.rstrip("/") if importdir else importdir
        self.state      = True
        self.dir        = self.base +"/"+ self.name
        self.cardsdir   = self.dir  +"/cards"
        self.filesdir   = self.dir  +"/files"
        self.load()
    def create(self):
        if not self.importdir: self.master.error("I cannot load detail of the package '"+self.name+"'")
        mkdir(self.master, self.dir     )
        mkdir(self.master, self.cardsdir)
        mkdir(self.master, self.filesdir)
        self.importMe()
        self.register()
    def importMe(self):
        if os.path.exists(self.dir +"/init"): return
        if not self.importdir: return
        m = self.importdir.split("/")[-1]
        ##m = m.replace("_0p1","").replace("_0p2","").replace("_0p3","").replace("_0p4","").replace("_0p5","").replace("_0p6","").replace("_0p7","").replace("_0p8","").replace("_0p9","")
        self.points = []
        if os.path.exists(self.importdir+"/mps"): 
            points_dir = self.importdir+"/mps"
        else: points_dir = self.importdir
        for point in [l.strip("\n") for l in os.listdir(points_dir)]:
            point_dir=points_dir+"/"+point
            if not os.path.isdir(point_dir): continue
            # naming convention depends on details, so simply infer it
            # e.g. "{}/sig_{}_{}/SR.card.txt".format(point_dir,m,point)
            glist = glob("{}/sig_{}_{}/*.card.txt".format(point_dir,m,point))
            if len(glist)==0: continue
            if len(glist)>1: print 'SR inference failed: multiple matches',glist
            cardfile = glist[0]
            SRname = cardfile.split('/')[-1].split('.')[0]
            shapefile = "{}/sig_{}_{}/{}.input.root".format(point_dir,m,point,SRname)
            dest_card = self.cardsdir+"/"+point+".txt"
            dest_shape= self.filesdir+"/"+point+".root"
            cp(self.master, cardfile , dest_card )
            cp(self.master, shapefile, dest_shape)
            replaceInFile(dest_card, SRname+".input.root", dest_shape)
            self.points.append(point)

    def load(self):
        if not os.path.exists(self.dir +"/init"): 
            self.create()
        if hasattr(self, "init"): return
        self.init = Init(self, self.dir +"/init")
    def register(self):
        if not self.importdir: return
        sid = self.importdir.split("/")
        self.init = Init(self, self.dir +"/init")
        self.init.write({"model":sid[-1], "lumi": sid[-2], "region": sid[-3], "importbase": self.master.options.inputdir, "importdir": self.importdir, "points+": ",".join([p for p in self.points])})
        print 'Registered',len(self.points),'points'
        #self.importdir = None

class PoolHandler():
    def __init__(self, master):
        self.master   = master
        self.pooldir  = self.master.pooldir
        self.packages = []
        self.loadPool()
        self.collectPackages()
        if self.master.options.view: self.view()
    def loadPool(self):
        for pname in os.listdir(self.pooldir):
            if not os.path.isdir(self.pooldir+"/"+pname): continue
            self.packages.append(Package(self.master, pname))
        self.master.talkPool(self)
    def collectPackages(self):
        if not self.master.options.inputdir: return
        self.master.talkImport()
        importdir = self.master.options.inputdir.rstrip("/")
        if not importdir: return
        for p in os.listdir(importdir):
            if not os.path.isdir(importdir+"/"+p): continue
            for l in os.listdir(importdir+"/"+p):
                if not os.path.isdir(importdir+"/"+p+"/"+l): continue
                for m in os.listdir(importdir+"/"+p+"/"+l):
                    if not m in [self.master.model.name]: continue
                    print "Importing from",importdir+"/"+p+"/"+l+"/"+m
                    exists = self.findPackageByImportDir(importdir+"/"+p+"/"+l+"/"+m)
                    if not self.master.options.forceImport and exists: continue
                    if     self.master.options.forceImport and exists: self.deletePackage(exists)
                    pname = timestamp(False)
                    self.packages.append(Package(self.master, pname, importdir+"/"+p+"/"+l+"/"+m))
    def deletePackage(self, package):
        rm(self.master, self.pooldir+"/"+package.name)
        if package in self.packages: self.packages.remove(package)
        del package
    def deletePackageByName(self, pname):
        found = self.findPackageByName(pname)
        if not found: return
        self.deletePackage(found)
    def findPackageByName(self, pname):
        pnames = [p.name for p in self.packages]
        if pname in pnames:
            return self.packages[pnames.index(pname)]
        return None
    def findPackageByImportDir(self, importdir):
        thedir = [p.importdir for p in self.packages]
        if importdir in thedir:
            return self.packages[thedir.index(importdir)]
        return None
    def getListOfPackages(self):
        buffer         = []
        listOfPackages = []
        for p in self.packages:
            if p.model == self.master.model.name: 
                listOfPackages.append(p)
        if self.master.options.indironly:
            listOfPackages = self.getPackageList(listOfPackages, lambda p:     p.importbase == self.master.options.inputdir)
        if self.master.options.poolonly:
            listOfPackages = self.getPackageList(listOfPackages, lambda p: not p.importbase == self.master.options.inputdir)
        if len(self.master.options.lumis)>0:
            listOfPackages = self.getPackageList(listOfPackages, lambda p: p.lumi   in self.master.options.lumis   )
        if len(self.master.options.regions)>0:
            listOfPackages = self.getPackageList(listOfPackages, lambda p: p.region in self.master.options.regions )
        if len(self.master.options.packages)>0:
            listOfPackages = self.getPackageList(listOfPackages, lambda p: p.name   in self.master.options.packages)
        return listOfPackages
    def getPackage(self, pname):
        names = [p.name for p in self.packages]
        if not pname in names: return None
        return self.packages[names.index(pname)]
    def getPackageList(self, theList, condition):
        newList = []
        for p in theList:
            if condition(p):
                newList.append(p)
        return newList
    def view(self, packages = [], showText = True, showDiff = False):
        if len(packages)==0: packages = self.getListOfPackages() 
        if len(packages)==0: return
        if showText: self.master.talk("Viewing content of the pool:")
        self.master.addToTalk("ID : Name               : Model                : Region               : Lumi       : Importdir")
        for i,p in enumerate(packages):
            if not p: continue
            self.master.addToTalk("%s : %s : %s : %s : %s : %s"%(idString(i,2,True),p.name,idString(p.model,20),idString(p.region,20),idString(p.lumi,10),p.importdir))
        if not showDiff: return
        remaining = filter(lambda p: p not in packages, self.packages)
        if len(remaining)==0: return
        self.master.talk("Following packages are also in the pool, but cannot be used:")
        self.master.addToTalk(", ".join([p.name for p in remaining]))
        if askForInput("Do you want to remove these faulty packages?", ["y", "n"])=="y":
            theNames = [p.name for p in remaining]
            del remaining # delete any list that contains the pointer before deleting the object
            for name in theNames:
                self.deletePackageByName(name)

