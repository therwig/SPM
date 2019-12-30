import ROOT, math
from array import *
## code largely taken from: https://github.com/rpatelCERN/SUSY2015SMS/tree/master/PlotsSMS

histopath   = "[HISTO]" 
smearpath   = "[SMEAR]" 
plotpath    = "[PLOT]" 
spmpath      = "[SPMDIR]"
exts        = "[EXTS]"   
preliminary = "[PRELIMINARY]"
lumis       = [ [LUMIS] ]
energy      = "[ENERGY]"

## global variables for CMS lumi
cmsText               = "CMS";
cmsTextFont           = 61  
writeExtraText        = (preliminary!="")
extraText             = preliminary
extraTextFont         = 52 
lumiTextSize          = 0.6
lumiTextOffset        = 0.2
cmsTextSize           = 0.75
cmsTextOffset         = 0.1
relPosX               = 0.045
relPosY               = 0.035
relExtraDY            = 1.2
extraOverCmsTextSize  = 0.56 #0.76
allTheLumis           = list(set(lumis))
lumi_13TeV            = "%s fb^{-1}" % (", ".join([l.replace("p",".").replace("fb","") for l in allTheLumis]))
lumi_8TeV             = "19.7 fb^{-1}" 
lumi_7TeV             = "5.1 fb^{-1}"
lumi_sqrtS            = "%s TeV" % (energy)
drawLogo              = False

## CMS lumi: copy-pasted from https://ghm.web.cern.ch/ghm/plots/
def CMS_lumi(pad,  iPeriod,  iPosX, aLittleExtra = 0.09):
    outOfFrame    = False
    if(iPosX/10==0 ): outOfFrame = True
    alignY_=3
    alignX_=2
    if( iPosX/10==0 ): alignX_=1
    if( iPosX==0    ): alignY_=1
    if( iPosX/10==1 ): alignX_=1
    if( iPosX/10==2 ): alignX_=2
    if( iPosX/10==3 ): alignX_=3
    align_ = 10*alignX_ + alignY_
    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    e = 0.025
    pad.cd()
    lumiText = ""
    if( iPeriod==1 ):
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
    elif ( iPeriod==2 ):
        lumiText += lumi_8TeV
        lumiText += " (8 TeV)"
    elif( iPeriod==3 ):      
        lumiText = lumi_8TeV 
        lumiText += " (8 TeV)"
        lumiText += " + "
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
    elif ( iPeriod==4 ):
        lumiText += lumi_13TeV
        lumiText += " (13 TeV)"
    elif ( iPeriod==7 ):
        if( outOfFrame ):lumiText += "#scale[0.85]{"
        lumiText += lumi_13TeV 
        lumiText += " (13 TeV)"
        lumiText += " + "
        lumiText += lumi_8TeV 
        lumiText += " (8 TeV)"
        lumiText += " + "
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
        if( outOfFrame): lumiText += "}"
    elif ( iPeriod==12 ):
        lumiText += "8 TeV"
    elif ( iPeriod==0 ):
        lumiText += lumi_sqrtS
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)    
    extraTextSize = extraOverCmsTextSize*cmsTextSize
    latex.SetTextFont(42)
    latex.SetTextAlign(31) 
    latex.SetTextSize(lumiTextSize*t)    
    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
    if( outOfFrame ):
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11) 
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11) 
        latex.SetTextSize(cmsTextSize*t)    
        latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
    pad.cd()
    posX_ = 0
    if( iPosX%10<=1 ):
        posX_ =   l + relPosX*(1-l-r)
    elif( iPosX%10==2 ):
        posX_ =  l + 0.5*(1-l-r)
    elif( iPosX%10==3 ):
        posX_ =  1-r - relPosX*(1-l-r)
    posY_ = 1-t - relPosY*(1-t-b)
    if( not outOfFrame ):
        if( drawLogo ):
            posX_ =   l + 0.045*(1-l-r)*W/H
            posY_ = 1-t - 0.045*(1-t-b)
            xl_0 = posX_
            yl_0 = posY_ - 0.15
            xl_1 = posX_ + 0.15*H/W
            yl_1 = posY_
            CMS_logo = ROOT.TASImage("CMS-BW-label.png")
            pad_logo = ROOT.TPad("logo","logo", xl_0, yl_0, xl_1, yl_1 )
            pad_logo.Draw()
            pad_logo.cd()
            CMS_logo.Draw("X")
            pad_logo.Modified()
            pad.cd()          
        else:
            latex.SetTextFont(cmsTextFont)
            latex.SetTextSize(cmsTextSize*t)
            latex.SetTextAlign(align_)
            latex.DrawLatex(posX_, posY_, cmsText)
            if( writeExtraText ) :
                latex.SetTextFont(extraTextFont)
                latex.SetTextAlign(align_)
                latex.SetTextSize(extraTextSize*t)
                latex.DrawLatex(posX_, posY_- relExtraDY*cmsTextSize*t, extraText)
    elif( writeExtraText ):
        if( iPosX==0):
            posX_ =   l +  relPosX*(1+l-r) + aLittleExtra
            posY_ =   1-t+lumiTextOffset*t
        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize*t)
        latex.SetTextAlign(align_)
        latex.DrawLatex(posX_, posY_, extraText)      
    pad.Update()

def userToNDC(coord, isX = False):
    isLog = ROOT.gPad.GetLogy()
    begin = ROOT.gPad.GetY1()
    dist  = ROOT.gPad.GetY2()-ROOT.gPad.GetY1()
    if isX:
        isLog = ROOT.gPad.GetLogx()
        begin = ROOT.gPad.GetX1() 
        dist  = ROOT.gPad.GetX2()-ROOT.gPad.GetX1()
    return math.log((coord-begin)/dist, 10) if isLog else (coord-begin)/dist # FIXME: test it!

def NDCtoUser(coord, isX = False):
    isLog = ROOT.gPad.GetLogy()
    begin = ROOT.gPad.GetY1()
    dist  = ROOT.gPad.GetY2()-ROOT.gPad.GetY1()
    if isX:
        isLog = ROOT.gPad.GetLogx()
        begin = ROOT.gPad.GetX1() 
        dist  = ROOT.gPad.GetX2()-ROOT.gPad.GetX1()
    return math.pow(10, dist*coord+begin) if isLog else dist*coord+begin

def relSize(length, isX=False):
    dist  = ROOT.gPad.GetY2()-ROOT.gPad.GetY1()
    if isX:
        dist  = ROOT.gPad.GetX2()-ROOT.gPad.GetX1()
    return length/dist

def color(colorname):
    return eval("ROOT."+colorname)

def createGraph(histo2d):
    h1d    = histo2d.ProjectionX()
    bins   = [b for b in range(1, h1d.GetXaxis().GetNbins()+1) if h1d.GetBinContent(b)>0]
    masses = [h1d.GetBinCenter (b) for b in bins]
    limits = [h1d.GetBinContent(b) for b in bins]
    graph  = ROOT.TGraph(len(masses), array('d', masses), array('d', limits))
    return graph

def createSigmaBand(plus, minus):
    ## build one graph summing the + and - 1 sigma
    if not plus or not minus: return None
    nP = plus .GetN()
    nM = minus.GetN()
    sigmaBandX = []
    sigmaBandY = []
    for i in range(0,nP):
        sigmaBandX.append(ROOT.Double(0.))
        sigmaBandY.append(ROOT.Double(0.))
        plus.GetPoint(i, sigmaBandX[i], sigmaBandY[i])
    for i in range(0,nM):
        sigmaBandX.append(ROOT.Double(0.))
        sigmaBandY.append(ROOT.Double(0.))
    for i in range(0,nM):
        minus.GetPoint(i, sigmaBandX[nP+nM-i-1], sigmaBandY[nP+nM-i-1])
    theGraph = ROOT.TGraph(nP+nM, array('d', sigmaBandX), array('d', sigmaBandY))
    theGraph.SetFillStyle(1001)
    #theGraph.SetFillStyle(3001)
    return theGraph

def getBinning(binning):
    if "[" in binning:
        b1 = [float(b) for b in binning.rstrip("]").lstrip("[").split(",")]
    else:
        s  = [float(b) for b in binning.split(",")]
        d  = (s[2]-s[1])/s[0]
        b1 = [s[1]+d*i for i in range(int(s[0]))] + [s[2]]
    return b1

def getDiagPos(model, diag, hist):
    xpos = [0, 200000]
    ypos = [0, 200000]
    if hasattr(diag, "xmin"):
        xpos[0] = float(diag.xmin)
    if hasattr(diag, "xmax"):
        xpos[1] = float(diag.xmax)
    if hasattr(diag, "ymin"):
        ypos[0] = float(diag.ymin)
    if hasattr(diag, "ymax"):
        ypos[1] = float(diag.ymax)
    if hasattr(diag, "xminmass"):
        xpos[0] = hist.GetBinCenter(hist.FindBin(float(diag.xminmass)))
    if hasattr(diag, "xmaxmass"):
        xpos[1] = hist.GetBinCenter(hist.FindBin(float(diag.xmaxmass)))
    if hasattr(diag, "yminmass"):
        ypos[0] = hist.GetBinCenter(hist.FindBin(float(diag.yminmass)))
    if hasattr(diag, "ymaxmass"):
        ypos[1] = hist.GetBinCenter(hist.FindBin(float(diag.ymaxmass)))
    if hasattr(diag, "offset"):
        xpos[0] = model.rangeX[0]
        xpos[1] = model.rangeX[1]
        ypos[0] = xpos[0] - float(diag.offset)
        ypos[1] = xpos[1] - float(diag.offset)
    return array('d',xpos), array('d',ypos)

def getGraphsMax(theGraph):
    theMax = 0
    if theGraph.nominal and max(getYs(theGraph.nominal)) > theMax: theMax = max(getYs(theGraph.nominal))
    if theGraph.plus    and max(getYs(theGraph.plus   )) > theMax: theMax = max(getYs(theGraph.plus   ))
    if theGraph.minus   and max(getYs(theGraph.minus  )) > theMax: theMax = max(getYs(theGraph.minus  ))
    if theGraph.plus2   and max(getYs(theGraph.plus2  )) > theMax: theMax = max(getYs(theGraph.plus2  ))
    if theGraph.minus2  and max(getYs(theGraph.minus2 )) > theMax: theMax = max(getYs(theGraph.minus2 ))
    return theMax

def getGraphsMin(theGraph):
    theMin = 9999999999
    if theGraph.nominal and min(getYs(theGraph.nominal)) < theMin: theMin = min(getYs(theGraph.nominal))
    if theGraph.plus    and min(getYs(theGraph.plus   )) < theMin: theMin = min(getYs(theGraph.plus   ))
    if theGraph.minus   and min(getYs(theGraph.minus  )) < theMin: theMin = min(getYs(theGraph.minus  ))
    if theGraph.plus2   and min(getYs(theGraph.plus2  )) < theMin: theMin = min(getYs(theGraph.plus2  ))
    if theGraph.minus2  and min(getYs(theGraph.minus2 )) < theMin: theMin = min(getYs(theGraph.minus2 ))
    return theMin

def getYs(tGraph):
    bare = [float(tGraph.GetY()[i]) for i in range(tGraph.GetN())]
    return [b if b > 0.00000000001 and b < 9999999999 else 0. for b in bare]

class Entry():
    def __init__(self, line):
        line = line.strip()
        sl   = line.split()
        if len(line)==0 or len(sl)==0: return
        for el in sl:
            e = el.split("=")
            setattr(self, e[0], e[1])

class Graph():
    def __init__(self, tfile, nominal, plus, minus, linecolor=ROOT.kBlack, areacolor=ROOT.kBlack, plus2 = None, minus2 = None, create = False):
        self.linecolor = linecolor
        self.areacolor = areacolor
        if create: 
            self.create(tfile, nominal, plus, minus, plus2, minus2)
            return
        self.nominal   = tfile.Get(nominal)##; self.nominal.SetDirectory(0)
        self.plus      = tfile.Get(plus   )##; self.plus   .SetDirectory(0)
        self.minus     = tfile.Get(minus  )##; self.minus  .SetDirectory(0)
        self.plus2     = tfile.Get(plus2  ) if plus2  else None
        self.minus2    = tfile.Get(minus2 ) if minus2 else None
    def create(self, tfile, nominal, plus, minus, plus2, minus2):
        ## in case there is a histogram that first needs to extract a TGraph
        self.nominal = createGraph(tfile.Get(nominal))
        self.plus    = createGraph(tfile.Get(plus   ))
        self.minus   = createGraph(tfile.Get(minus  ))
        self.plus2   = createGraph(tfile.Get(plus2  )) if plus2  else None
        self.minus2  = createGraph(tfile.Get(minus2 )) if minus2 else None
    def drawAll(self):
        if self.nominal: self.nominal.Draw() 
        if self.plus   : self.plus   .Draw() 
        if self.minus  : self.minus  .Draw() 
        if self.plus2  : self.plus2  .Draw() 
        if self.minus2 : self.minus2 .Draw() 
        

class Model():
    def __init__(self):
        self.name       = "[MODEL:name]"
        self.xsecpath   = spmpath+"/[MODEL:xsecfile]"
        self.brcorr       = eval("[MODEL:brcorr]")
        self.mode       = "[PLOTMODE]"
        self.plane      = "[MODEL:plane]"
        self.deltaM     = float("[MODEL:deltaM]") if "[MODEL:deltaM]" else 1
        self.isNloNll   = ("[MODEL:noNllNlo]"!="True")
        self.posY       = [float(f) for f in "[MODEL:posY]".split(",")] if "[MODEL:posY]" else []
        self.binningX   = "[MODEL:binningX]"
        self.binningY   = "[MODEL:binningY]"
        self.rangeX     = [float(f) for f in "[MODEL:rangeX]".split(",")]
        self.rangeY     = [float(f) for f in "[MODEL:rangeY]".split(",")]
        self.rangeZ     = [float(f) for f in "[MODEL:rangeZ]".split(",")]
        self.legendX    = "[MODEL:legendX]"
        self.legendY    = "[MODEL:legendY]"
        self.nDivX      = int("[MODEL:nDivX]")
        self.nDivY      = int("[MODEL:nDivY]")
        self.logX       = True if "[MODEL:logX]"=="True" else False
        self.logY       = True if "[MODEL:logY]"=="True" else False
        self.text       = [[MODEL:text]]
        self.diag       = [[MODEL:diag]]
        self.smoothCont = ("[MODEL:smoothCont]"=="True")
    def setGraphs(self):
        add = ""
        if self.smoothCont: add = "_smoothed"
        self.gr_obs     = "[MODEL:gr_obs]"  if "[MODEL:gr_obs]"  else "gr_obs" +add
        self.gr_op1s    = "[MODEL:gr_op1s]" if "[MODEL:gr_op1s]" else "gr_op1s"+add
        self.gr_om1s    = "[MODEL:gr_om1s]" if "[MODEL:gr_om1s]" else "gr_om1s"+add
        self.gr_exp     = "[MODEL:gr_exp]"  if "[MODEL:gr_exp]"  else "gr_exp" +add
        self.gr_ep1s    = "[MODEL:gr_ep1s]" if "[MODEL:gr_ep1s]" else "gr_ep1s"+add
        self.gr_em1s    = "[MODEL:gr_em1s]" if "[MODEL:gr_em1s]" else "gr_em1s"+add

class XSlist():
    def __init__(self, model):
        xslist      = [l.rstrip("\n").split(":") for l in open(model.xsecpath, "r").readlines()]
        xslist      = [[float(m.strip()),float(xs.strip()),float(err.strip())] for [m,xs,err] in xslist ]
        self.mass   = [p[0] for p in xslist]
        self.xs     = [p[1] for p in xslist]
        self.err    = [p[2] for p in xslist]
        self.brcorr = float(model.brcorr)
    def getBin(self, mass):
        lowerbin = int(round(mass / 25)) * 25
        if not lowerbin in self.mass: return -1
        return self.mass.index(lowerbin)    
    def getErr(self, mass):
        bin = self.getBin(mass)
        if bin == -1: return 0
        return self.err[bin]*self.brcorr
    def getXS(self, mass):
        bin = self.getBin(mass)
        if bin == -1: return 0
        return self.xs[bin]*self.brcorr

class ThePlot():
    def __init__(self, model, histopath, smearpath, plotpath, exts):
        self.plotpath    = plotpath
        self.exts        = exts
        self.model       = model
        #self.c           = ROOT.TCanvas(self.model.name, self.model.name, 600, 600)
        self.c           = ROOT.TCanvas(self.model.name, self.model.name, 800, 600)
        b1, b2 = self.model.rangeX, self.model.rangeY
        self.xmax = float(b1[-1]); self.xmin = float(b1[0])
        self.ymax = float(b2[-1]); self.ymin = float(b2[0])
        if   self.model.mode == "xsec": self.plot = XSecPlot(self, model, histopath, smearpath)
        elif self.model.mode == "sens": self.plot = SensPlot(self, model, histopath, smearpath)
        elif self.model.mode == "braz": self.plot = BrazPlot(self, model, histopath, smearpath)
    def prepare(self):
        self.plot.histo.Draw()
        if hasattr(self.plot, "xsec"):
            self.plot.xsec .GetXaxis().SetRangeUser(self.model.rangeX[0], self.model.rangeX[1])
            self.plot.xsec .GetYaxis().SetRangeUser(self.model.rangeY[0], self.model.rangeY[1])
            self.plot.xsec.Draw("colzsame")
        self.setStyle()
        self.plot.setStyle()
    def draw(self):
        self.plot.draw()
    def drawHalfArea(self):
        halfarea = ROOT.TGraph(4)
        halfarea.SetName("halfarea")
        halfarea.SetFillColor(ROOT.kWhite)
        halfarea.SetFillStyle(1001)
        halfarea.SetLineColor(ROOT.kWhite)
        halfarea.SetLineStyle(1)
        halfarea.SetPoint(0, self.xmin, self.xmin-self.model.deltaM)
        halfarea.SetPoint(1, self.xmax, self.xmax-self.model.deltaM)
        halfarea.SetPoint(2, self.xmin, self.xmax-self.model.deltaM)
        halfarea.SetPoint(3, self.xmin, self.xmin-self.model.deltaM)
        halfarea.Draw("FSAME")
        halfarea.Draw("LSAME")
        self.c.halfarea = halfarea
    def drawDiagonals(self):
        if not hasattr(self.model, "diag") or len(self.model.diag)==0: return
        for i,diag in enumerate(self.model.diag):
            self.drawDiagonal(Entry(diag),i)
    def drawDiagonal(self, diag, num):
        xpos, ypos = getDiagPos(self.model, diag, self.plot.histo)
        diagonal = ROOT.TGraph(2, xpos, ypos)
        diagonal.SetName("diagonal"+str(num))
        diagonal.SetFillColor(ROOT.kWhite)
        diagonal.SetLineColor(getattr(diag, "color", ROOT.kGray))
        diagonal.SetLineStyle(getattr(diag, "style", 2         ))
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        setattr(self.c, "diagonal"+str(num), diagonal)
    def drawText(self, corr = 1.0):
        nText  = len(self.model.text)
        nLeg   = self.plot.nLegend
        xRange = self.xmax-self.xmin
        yRange = self.ymax-self.ymin
        self.c.RedrawAxis()
        # white background
        if nText+nLeg > 0:
            graphWhite = ROOT.TGraph(5)
            graphWhite.SetName("white")
            graphWhite.SetTitle("white")
            graphWhite.SetFillColor(ROOT.kWhite)
            graphWhite.SetFillStyle(1001)
            graphWhite.SetLineColor(ROOT.kBlack)
            graphWhite.SetLineStyle(1)
            graphWhite.SetLineWidth(3)
            if self.c.GetLogy():
                #graphWhite.SetPoint(0, self.xmin, self.ymax)
                #graphWhite.SetPoint(1, self.xmax, self.ymax)
                #graphWhite.SetPoint(2, self.xmax, 400)
                #graphWhite.SetPoint(3, self.xmin, 400)
                #graphWhite.SetPoint(4, self.xmin, self.ymax)
                #graphWhite.SetPoint(0, self.xmin, self.ymax)
                #graphWhite.SetPoint(1, self.xmax, self.ymax)
                #graphWhite.SetPoint(2, self.xmax, self.ymax/(corr*10*(nText+nLeg-1)))
                #graphWhite.SetPoint(3, self.xmin, self.ymax/(corr*10*(nText+nLeg-1)))
                #graphWhite.SetPoint(4, self.xmin, self.ymax)
                graphWhite.SetPoint(0, self.xmin, NDCtoUser(0.92))
                graphWhite.SetPoint(1, self.xmax, NDCtoUser(0.92))
                graphWhite.SetPoint(2, self.xmax, NDCtoUser(0.92-0.08*(nText+nLeg)))
                graphWhite.SetPoint(3, self.xmin, NDCtoUser(0.92-0.08*(nText+nLeg)))
                graphWhite.SetPoint(4, self.xmin, NDCtoUser(0.92))
            else:
                graphWhite.SetPoint(0, self.xmin, self.ymax)
                graphWhite.SetPoint(1, self.xmax, self.ymax)
                graphWhite.SetPoint(2, self.xmax, self.ymax*(0.97-corr*0.07*(nText+nLeg)))
                graphWhite.SetPoint(3, self.xmin, self.ymax*(0.97-corr*0.07*(nText+nLeg)))
                graphWhite.SetPoint(4, self.xmin, self.ymax)
            graphWhite.Draw("FSAME")
            graphWhite.Draw("LSAME")
            self.c.graphWhite = graphWhite
        CMS_lumi(self.c, 4, 0, 0.05)
        #CMS_lumi(self.c, 4, 0, 0.09/corr)
        text      = []
        textSizes = []
        nominal   = 0.143446295867*corr
        for i,line in enumerate(self.model.text):
            if self.model.mode=="braz": ##FIXME
                text.append(ROOT.TLatex(0.16, 0.89, line))
                text[i].SetNDC()
            else:
                text.append(ROOT.TLatex(self.xmin+3*xRange/100, self.ymax-(0.15+corr*0.75*i)*yRange/100*10, line))
            text[i].SetTextAlign(13)
            text[i].SetTextFont(42)
            text[i].SetTextSize(0.038)
            textSizes.append(text[i].GetYsize())
        for i,line in enumerate(self.model.text):
            if self.model.mode == "braz":
                text[i].SetY(0.89-sum([0.05+relSize(ts-nominal)/2 for ts in textSizes[0:i]])+relSize(textSizes[0]-nominal)/2)
            text[i].Draw()
            setattr(self.c, "text"+str(i), text[i])
        self.textCorr = sum([0.05+relSize(ts-nominal)/2 for ts in textSizes[0:nText]])-relSize(textSizes[0]-nominal)/2
        if self.model.isNloNll:
            if self.model.mode=="braz": ##FIXME
                textNLL = ROOT.TLatex(0.63, 0.89-corr*self.textCorr-0.02, "NLO-NLL excl.")
                textNLL.SetNDC()
            else:
                textNLL = ROOT.TLatex(self.xmin+66*xRange/100, self.ymax-(0.35+corr*0.75*nText)*yRange/100*10, "NLO-NLL excl.")
            textNLL.SetTextAlign(13)
            textNLL.SetTextFont(42)
            textNLL.SetTextSize(0.038)
            textNLL.Draw()
            self.c.textNLL = textNLL
    def save(self):
        for ext in self.exts.split(","):
            self.c.SaveAs(self.plotpath+"."+ext)
    def setStyle(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)        
        self.c.SetLogz()
        self.c.SetTickx(1)
        self.c.SetTicky(1)
        self.c.SetRightMargin (0.19)
        self.c.SetTopMargin   (0.08)
        self.c.SetLeftMargin  (0.14)
        self.c.SetBottomMargin(0.14)
        self.plot.histo.GetXaxis().SetNdivisions(self.model.nDivX)
        self.plot.histo.GetXaxis().SetLabelFont(42)
        self.plot.histo.GetXaxis().SetLabelSize(0.035)
        self.plot.histo.GetXaxis().SetTitleFont(42)
        self.plot.histo.GetXaxis().SetTitleSize(0.05)
        self.plot.histo.GetXaxis().SetTitleOffset(1.2)
        self.plot.histo.GetXaxis().SetTitle(self.model.legendX)
        self.plot.histo.GetYaxis().SetNdivisions(self.model.nDivY)
        self.plot.histo.GetYaxis().SetLabelFont(42)
        self.plot.histo.GetYaxis().SetLabelSize(0.035)
        self.plot.histo.GetYaxis().SetTitleFont(42)
        self.plot.histo.GetYaxis().SetTitleSize(0.05)
        self.plot.histo.GetYaxis().SetTitleOffset(1.30)
        self.plot.histo.GetYaxis().SetTitle(self.model.legendY)
        #self.emptyHisto.GetXaxis().CenterTitle(True)
        #self.emptyHisto.GetYaxis().CenterTitle(True)

class XSecPlot():
    def __init__(self, parent, model, histopath, smearpath):
        self.nLegend = 2 # entries of the legend (needed for white box size)
        self.parent  = parent
        self.model   = model
        self.c       = self.parent.c
        fin          = ROOT.TFile(histopath, "READ")
        self.xsec    = fin.Get(self.model.plane)
        self.xsec .SetDirectory(0)
        fin.Close()
        self.histo   = ROOT.TH2F("axis", "axis", 1, self.model.rangeX[0], self.model.rangeX[1], 1, self.model.rangeY[0], self.model.rangeY[1])
        fin          = ROOT.TFile(smearpath, "READ")
        self.exp     = Graph(fin, self.model.gr_exp, self.model.gr_ep1s, self.model.gr_em1s, ROOT.kRed  , ROOT.kOrange)
        self.obs     = Graph(fin, self.model.gr_obs, self.model.gr_op1s, self.model.gr_om1s, ROOT.kBlack, ROOT.kGray  )
        self.exp.drawAll()
        self.obs.drawAll()
        self.c.Clear()
        fin.Close()
    def setStyle(self):
        self.histo.GetZaxis().SetLabelFont(42)
        self.histo.GetZaxis().SetTitleFont(42)
        self.histo.GetZaxis().SetLabelSize(0.035)
        self.histo.GetZaxis().SetTitleSize(0.035)
        self.xsec.SetMinimum(self.model.rangeZ[0])
        self.xsec.SetMaximum(self.model.rangeZ[1])
        NRGBs = 5
        NCont = 255
        stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
        red   = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
        green = array("d",[0.50, 1.00, 1.00, 0.60, 0.50])
        blue  = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
        ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
        ROOT.gStyle.SetNumberContours(NCont)
        self.c.cd()
        self.xsec.Draw("colz")
        ROOT.gPad.Update()
        palette = self.xsec.GetListOfFunctions().FindObject("palette")
        palette.SetX1NDC(1.-0.18)
        palette.SetY1NDC(0.14)
        palette.SetX2NDC(1.-0.13)
        palette.SetY2NDC(1.-0.08)
        palette.SetLabelFont(42)
        palette.SetLabelSize(0.035)
    def draw(self):
        self.drawHisto()
        self.drawContours()
        self.parent.drawHalfArea()
        self.parent.drawDiagonals()
        self.parent.drawText() 
        self.drawLegend() 
    def drawContours(self):
        # observed
        if self.obs.nominal:
            self.obs.nominal.SetLineColor(self.obs.linecolor)
            self.obs.nominal.SetLineStyle(1)
            self.obs.nominal.SetLineWidth(4)
        # observed + 1sigma
        if self.obs.plus:
            self.obs.plus.SetLineColor(self.obs.linecolor)
            self.obs.plus.SetLineStyle(1)
            self.obs.plus.SetLineWidth(2)
        # observed - 1sigma
        if self.obs.minus:
            self.obs.minus.SetLineColor(self.obs.linecolor)
            self.obs.minus.SetLineStyle(1)
            self.obs.minus.SetLineWidth(2)
        # expected
        if self.exp.nominal:
            self.exp.nominal.SetLineColor(self.exp.linecolor)
            self.exp.nominal.SetLineStyle(7)
            self.exp.nominal.SetLineWidth(4)
        # expected + 1sigma
        if self.exp.plus:
            self.exp.plus.SetLineColor(self.exp.linecolor)
            self.exp.plus.SetLineStyle(7)
            self.exp.plus.SetLineWidth(2)
        # expected - 1sigma
        if self.exp.minus:
            self.exp.minus.SetLineColor(self.exp.linecolor)
            self.exp.minus.SetLineStyle(7)
            self.exp.minus.SetLineWidth(2)
        # DRAW LINES
        if self.exp.nominal: self.exp.nominal.Draw("LSAME")
        if self.exp.plus   : self.exp.plus   .Draw("LSAME")
        if self.exp.minus  : self.exp.minus  .Draw("LSAME")
        if self.obs.nominal: self.obs.nominal.Draw("LSAME")
        if self.obs.plus   : self.obs.plus   .Draw("LSAME")
        if self.obs.minus  : self.obs.minus  .Draw("LSAME")
    def drawHisto(self):
        self.histo.Draw() 
        self.xsec .Draw("COLZSAME") 
        textCOLZ = ROOT.TLatex(0.98, 0.15, "95% CL upper limit on cross section [pb]")
        textCOLZ.SetNDC()
        #textCOLZ.SetTextAlign(13)
        textCOLZ.SetTextFont(42)
        textCOLZ.SetTextSize(0.045)
        textCOLZ.SetTextAngle(90)
        textCOLZ.Draw()
        self.c.textCOLZ = textCOLZ
    def drawLegend(self):
        nText=len(self.model.text)
        xRange = self.parent.xmax-self.parent.xmin
        yRange = self.parent.ymax-self.parent.ymin
        LObsP = ROOT.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        LObsP.SetLineColor(self.obs.linecolor)
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0, self.parent.xmin+3 *xRange/100, self.parent.ymax-(0.35+0.75*nText)*yRange/100*10)
        LObsP.SetPoint(1, self.parent.xmin+10*xRange/100, self.parent.ymax-(0.35+0.75*nText)*yRange/100*10)
        LObs = ROOT.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(self.obs.linecolor)
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0, self.parent.xmin+3 *xRange/100, self.parent.ymax-(0.50+0.75*nText)*yRange/100*10)
        LObs.SetPoint(1, self.parent.xmin+10*xRange/100, self.parent.ymax-(0.50+0.75*nText)*yRange/100*10)
        LObsM = ROOT.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        LObsM.SetLineColor(self.obs.linecolor)
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0, self.parent.xmin+3 *xRange/100, self.parent.ymax-(0.65+0.75*nText)*yRange/100*10)
        LObsM.SetPoint(1, self.parent.xmin+10*xRange/100, self.parent.ymax-(0.65+0.75*nText)*yRange/100*10)
        textObs = ROOT.TLatex(self.parent.xmin+11*xRange/100, self.parent.ymax-(0.65+0.75*nText)*yRange/100*10, "Observed #pm 1 #sigma_{theory}")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs
        LExpP = ROOT.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(self.exp.linecolor)
        LExpP.SetLineStyle(7)
        LExpP.SetLineWidth(2)
        LExpP.SetPoint(0, self.parent.xmin+3 *xRange/100, self.parent.ymax-(1.00+0.75*nText)*yRange/100*10)
        LExpP.SetPoint(1, self.parent.xmin+10*xRange/100, self.parent.ymax-(1.00+0.75*nText)*yRange/100*10)
        LExp = ROOT.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(self.exp.linecolor)
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0, self.parent.xmin+3 *xRange/100, self.parent.ymax-(1.15+0.75*nText)*yRange/100*10)
        LExp.SetPoint(1, self.parent.xmin+10*xRange/100, self.parent.ymax-(1.15+0.75*nText)*yRange/100*10)
        LExpM = ROOT.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(self.exp.linecolor)
        LExpM.SetLineStyle(7)
        LExpM.SetLineWidth(2)
        LExpM.SetPoint(0, self.parent.xmin+3 *xRange/100, self.parent.ymax-(1.30+0.75*nText)*yRange/100*10)
        LExpM.SetPoint(1, self.parent.xmin+10*xRange/100, self.parent.ymax-(1.30+0.75*nText)*yRange/100*10)
        textExp = ROOT.TLatex(self.parent.xmin+11*xRange/100, self.parent.ymax-(1.30+0.75*nText)*yRange/100*10, "Expected #pm 1 #sigma_{experiment}")
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp
        LObs .Draw("LSAME")
        LObsM.Draw("LSAME")
        LObsP.Draw("LSAME")
        LExp .Draw("LSAME")
        LExpM.Draw("LSAME")
        LExpP.Draw("LSAME")
        self.c.LObs  = LObs
        self.c.LObsM = LObsM
        self.c.LObsP = LObsP
        self.c.LExp  = LExp
        self.c.LExpM = LExpM
        self.c.LExpP = LExpP

class SensPlot():
    def __init__(self, parent, model, histopath, smearpath):
        self.nLegend = 0 # entries of the legend (needed for white box size)
        self.parent  = parent
        self.model   = model
        self.model.isNloNll = False
        self.c       = self.parent.c
        fin          = ROOT.TFile(histopath, "READ")
        self.xsec    = fin.Get(self.model.plane)
        self.xsec .SetDirectory(0)
        fin.Close()
        self.histo   = ROOT.TH2F("axis", "axis", 1, self.model.rangeX[0], self.model.rangeX[1], 1, self.model.rangeY[0], self.model.rangeY[1])
    def setStyle(self):
        self.c.SetLogz(0)
        self.histo.GetZaxis().SetLabelFont(42)
        self.histo.GetZaxis().SetTitleFont(42)
        self.histo.GetZaxis().SetLabelSize(0.035)
        self.histo.GetZaxis().SetTitleSize(0.035)
        self.xsec.SetMinimum(self.model.rangeZ[0])
        self.xsec.SetMaximum(self.model.rangeZ[1])
        NRGBs = 5
        NCont = 255
        stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
        red   = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
        green = array("d",[0.50, 1.00, 1.00, 0.60, 0.50])
        blue  = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
        ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
        ROOT.gStyle.SetNumberContours(NCont)
        self.c.cd()
        self.xsec.Draw("colz")
        ROOT.gPad.Update()
        palette = self.xsec.GetListOfFunctions().FindObject("palette")
        palette.SetX1NDC(1.-0.18)
        palette.SetY1NDC(0.14)
        palette.SetX2NDC(1.-0.13)
        palette.SetY2NDC(1.-0.08)
        palette.SetLabelFont(42)
        palette.SetLabelSize(0.035)
    def draw(self):
        self.drawHisto()
        self.parent.drawHalfArea()
        self.parent.drawDiagonals()
        self.parent.drawText() 
    def drawHisto(self):
        self.histo.Draw() 
        self.xsec .Draw("COLZSAME") 
        textCOLZ = ROOT.TLatex(0.98, 0.15, "observed significance [#sigma]")
        textCOLZ.SetNDC()
        #textCOLZ.SetTextAlign(13)
        textCOLZ.SetTextFont(42)
        textCOLZ.SetTextSize(0.045)
        textCOLZ.SetTextAngle(90)
        textCOLZ.Draw()
        self.c.textCOLZ = textCOLZ


class BrazPlot():
    def __init__(self, parent, model, histopath, smearpath):
        self.nLegend = 2 # entries of the legend (needed for white box size)
        self.parent  = parent
        self.model   = model
        self.model.isNloNll = False
        self.xslist  = XSlist(model)
        self.c       = self.parent.c
        self.c.SetWindowSize(800,600)
        self.c.SetLogy()
        self.c.Update()
        fin          = ROOT.TFile(histopath, "READ")
        self.exp     = Graph(fin, "exp_xs0", "ep1s_xs0", "em1s_xs0", plus2="ep2s_xs0", minus2="em2s_xs0", create=True)
        self.obs     = Graph(fin, "obs_xs0", "op1s_xs0", "om1s_xs0", create=True)
        fin.Close()
        self.histo   = ROOT.TH2F("axis", "axis", 1, self.model.rangeX[0], self.model.rangeX[1], 1, self.model.rangeY[0], self.model.rangeY[1])
        self.parent.ymax = self.histo.GetYaxis().GetXmax()
        self.parent.ymin = self.histo.GetYaxis().GetXmin()
        self.setTheoGraph()
    def setTheoGraph(self):
        ordered   = [(float(m), self.xslist.getXS(m), self.xslist.getErr(m)) for m in range(int(self.model.rangeX[0]),int(self.model.rangeX[1]),25)]
        self.theo   = ROOT.TGraph()
        self.theo1p = ROOT.TGraph()
        self.theo1m = ROOT.TGraph()
        for i,od in enumerate(ordered):
            self.theo  .SetPoint(i, float(od[0]), float(od[1])             )
            self.theo1p.SetPoint(i, float(od[0]), float(od[1])+float(od[2]))
            self.theo1m.SetPoint(i, float(od[0]), float(od[1])-float(od[2]))
        self.theo  .SetLineColor(ROOT.kRed+1)
        self.theo  .SetLineStyle(1)
        self.theo  .SetLineWidth(2)
        self.theo1p.SetLineColor(ROOT.kRed+1)
        self.theo1p.SetLineStyle(2)
        self.theo1p.SetLineWidth(1)
        self.theo1m.SetLineColor(ROOT.kRed+1)
        self.theo1m.SetLineStyle(2)
        self.theo1m.SetLineWidth(1)
    def setStyle(self):
        self.histo.GetYaxis().SetTitle(self.model.legendY if self.model.legendY else "cross section [pb]")
        #self.histo.GetYaxis().SetTitle(self.model.legendY if self.model.legendY else "95% CL upper limit on cross section [pb]")
        self.c.SetLeftMargin(0.12)
        self.c.SetRightMargin(0.08)
        self.histo.GetYaxis().SetTitleOffset(1.10)
        self.c.cd()
        self.histo.Draw()
        ROOT.gPad.Update()
    def draw(self):
        self.drawHisto()
        self.drawContours()
        self.theo  .Draw("same")
        self.theo1p.Draw("same")
        self.theo1m.Draw("same")
        self.parent.drawText(8./6) 
        self.drawLegendNew() 
    def drawContours(self):
        # observed
        if self.obs.nominal:
            self.obs.nominal.SetLineColor(self.obs.linecolor)
            self.obs.nominal.SetLineStyle(1)
            self.obs.nominal.SetLineWidth(4)
        # observed + 1sigma
        if self.obs.plus:
            self.obs.plus.SetLineColor(self.obs.linecolor)
            self.obs.plus.SetLineStyle(1)
            self.obs.plus.SetLineWidth(2)
        # observed - 1sigma
        if self.obs.minus:
            self.obs.minus.SetLineColor(self.obs.linecolor)
            self.obs.minus.SetLineStyle(1)
            self.obs.minus.SetLineWidth(2)
        # expected
        if self.exp.nominal:
            self.exp.nominal.SetLineColor(self.exp.linecolor)
            self.exp.nominal.SetLineStyle(2)
            self.exp.nominal.SetLineWidth(4)
        self.band1s = createSigmaBand(self.exp.plus , self.exp.minus )
        self.band2s = createSigmaBand(self.exp.plus2, self.exp.minus2)
        self.band2s.SetFillColor(ROOT.kYellow) # FIXME: configurable?
        self.band1s.SetFillColor(ROOT.kGreen )
        # DRAW LINES
        if self.band2s     : self.band2s     .Draw("FSAME")
        if self.band1s     : self.band1s     .Draw("FSAME")
        if self.exp.nominal: self.exp.nominal.Draw("LSAME")
        if self.obs.nominal: self.obs.nominal.Draw("LSAME")
        #if self.obs.plus   : self.obs.plus   .Draw("LSAME")
        #if self.obs.minus  : self.obs.minus  .Draw("LSAME")
    def drawHisto(self):
        self.histo.SetMaximum(self.parent.ymax)
        self.histo.SetMinimum(self.parent.ymin)
        if self.model.logX: self.c.SetLogx()
        if self.model.logY: self.c.SetLogy()
        self.histo.Draw() 
    def drawLegend(self):
        nText=len(self.model.text)
        xRange = self.parent.xmax-self.parent.xmin
        yRange = self.parent.ymax-self.parent.ymin
        LObsP = ROOT.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        LObsP.SetLineColor(self.obs.linecolor)
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr+0.02-0.04))
        LObsP.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr+0.02-0.04))
        LObs = ROOT.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(self.obs.linecolor)
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr+0.01-0.04))
        LObs.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr+0.01-0.04))
        LObsM = ROOT.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        LObsM.SetLineColor(self.obs.linecolor)
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr-0.04))
        LObsM.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr-0.04))
        textObs = ROOT.TLatex(0.23, 0.89-self.parent.textCorr-0.04, "Observed #pm 1 #sigma_{theory}") # -0.04 cause text is too large
        textObs.SetNDC()
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs
        LExp = ROOT.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(self.exp.linecolor)
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr+0.015-0.06-0.04))
        LExp.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr+0.015-0.06-0.04))
        LExp1S = ROOT.TGraph(4)
        LExp1S.SetName("LExp1S")  
        LExp1S.SetTitle("LExp1S")  
        LExp1S.SetFillColor(ROOT.kGreen) ## FIXME: configurable?
        LExp1S.SetLineStyle(3)
        LExp1S.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr+0.025-0.06-0.04))
        LExp1S.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr+0.025-0.06-0.04))
        LExp1S.SetPoint(2, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr+0.005-0.06-0.04))
        LExp1S.SetPoint(3, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr+0.005-0.06-0.04))
        LExp2S = ROOT.TGraph(4)
        LExp2S.SetName("LExp2S")  
        LExp2S.SetTitle("LExp2S")  
        LExp2S.SetFillColor(ROOT.kYellow) ## FIXME: configurable?
        LExp2S.SetLineStyle(3)
        LExp2S.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr+0.03-0.06-0.04))
        LExp2S.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr+0.03-0.06-0.04))
        LExp2S.SetPoint(2, NDCtoUser(0.22, True), NDCtoUser(0.89-self.parent.textCorr     -0.06-0.04))
        LExp2S.SetPoint(3, NDCtoUser(0.16, True), NDCtoUser(0.89-self.parent.textCorr     -0.06-0.04))
        textExp = ROOT.TLatex(0.23, 0.89-self.parent.textCorr-0.06-0.04, "Expected #pm 1(2) #sigma_{experiment}")
        textExp.SetNDC()
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp
        LObs  .Draw("LSAME")
        LObsM .Draw("LSAME")
        LObsP .Draw("LSAME")
        LExp2S.Draw("FSAME")
        LExp1S.Draw("FSAME")
        LExp  .Draw("LSAME")
        self.c.LObs   = LObs
        self.c.LObsM  = LObsM
        self.c.LObsP  = LObsP
        self.c.LExp   = LExp
        self.c.LExp1S = LExp1S
        self.c.LExp2S = LExp2S
    def drawLegendNew(self):
        corr   = 7./6
        nText  = len(self.model.text)
        xRange = self.parent.xmax-self.parent.xmin
        yRange = self.parent.ymax-self.parent.ymin
        LTheoP = ROOT.TGraph(2)
        LTheoP.SetName("LTheoP")
        LTheoP.SetTitle("LTheoP")
        LTheoP.SetLineColor(ROOT.kRed+1)
        LTheoP.SetLineStyle(2)
        LTheoP.SetLineWidth(1)
        LTheoP.SetMarkerStyle(20)
        LTheoP.SetPoint(0, NDCtoUser(0.56, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.025-0.04))
        LTheoP.SetPoint(1, NDCtoUser(0.62, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.025-0.04))
        LTheo = ROOT.TGraph(2)
        LTheo.SetName("LTheo")
        LTheo.SetTitle("LTheo")
        LTheo.SetLineColor(ROOT.kRed+1)
        LTheo.SetLineStyle(1)
        LTheo.SetLineWidth(4)
        LTheo.SetMarkerStyle(20)
        LTheo.SetPoint(0, NDCtoUser(0.56, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.014-0.04))
        LTheo.SetPoint(1, NDCtoUser(0.62, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.014-0.04))
        LTheoM = ROOT.TGraph(2)
        LTheoM.SetName("LTheoM")
        LTheoM.SetTitle("LTheoM")
        LTheoM.SetLineColor(ROOT.kRed+1)
        LTheoM.SetLineStyle(2)
        LTheoM.SetLineWidth(1)
        LTheoM.SetMarkerStyle(20)
        LTheoM.SetPoint(0, NDCtoUser(0.56, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.005-0.04))
        LTheoM.SetPoint(1, NDCtoUser(0.62, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.005-0.04))
        textTheo = ROOT.TLatex(0.63, 0.89-corr*self.parent.textCorr-0.04, "NLO+NLL #pm 1 #sigma_{theory}") # -0.04 cause text is too large
        textTheo.SetNDC()
        textTheo.SetTextFont(42)
        textTheo.SetTextSize(0.040)
        textTheo.Draw()
        self.c.textTheo = textTheo
        LObs = ROOT.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(self.obs.linecolor)
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0, NDCtoUser(0.56, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.015-0.04-0.06))
        LObs.SetPoint(1, NDCtoUser(0.62, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.015-0.04-0.06))
        textObs = ROOT.TLatex(0.63, 0.89-corr*self.parent.textCorr-0.06-0.04, "Observed") # -0.04 cause text is too large
        textObs.SetNDC()
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs
        LExp = ROOT.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(self.exp.linecolor)
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.014-0.04))
        LExp.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.014-0.04))
        LExp1S = ROOT.TGraph(4)
        LExp1S.SetName("LExp1S")  
        LExp1S.SetTitle("LExp1S")  
        LExp1S.SetFillColor(ROOT.kGreen) ## FIXME: configurable?
        LExp1S.SetLineStyle(1)
        LExp1S.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.025-0.04))
        LExp1S.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.025-0.04))
        LExp1S.SetPoint(2, NDCtoUser(0.22, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.005-0.04))
        LExp1S.SetPoint(3, NDCtoUser(0.16, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.005-0.04))
        textExp = ROOT.TLatex(0.23, 0.89-corr*self.parent.textCorr-0.04, "Expected #pm 1 #sigma_{experiment}")
        textExp.SetNDC()
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp
        LExp2 = ROOT.TGraph(2)
        LExp2.SetName("LExp2")
        LExp2.SetTitle("LExp2")
        LExp2.SetLineColor(self.exp.linecolor)
        LExp2.SetLineStyle(7)
        LExp2.SetLineWidth(4)
        LExp2.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.015-0.06-0.04))
        LExp2.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.015-0.06-0.04))
        LExp2S = ROOT.TGraph(4)
        LExp2S.SetName("LExp2S")  
        LExp2S.SetTitle("LExp2S")  
        LExp2S.SetFillColor(ROOT.kYellow) ## FIXME: configurable?
        LExp2S.SetLineStyle(1)
        LExp2S.SetPoint(0, NDCtoUser(0.16, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.03-0.06-0.04))
        LExp2S.SetPoint(1, NDCtoUser(0.22, True), NDCtoUser(0.89-corr*self.parent.textCorr+0.03-0.06-0.04))
        LExp2S.SetPoint(2, NDCtoUser(0.22, True), NDCtoUser(0.89-corr*self.parent.textCorr     -0.06-0.04))
        LExp2S.SetPoint(3, NDCtoUser(0.16, True), NDCtoUser(0.89-corr*self.parent.textCorr     -0.06-0.04))
        textExp2 = ROOT.TLatex(0.23, 0.89-corr*self.parent.textCorr-0.06-0.04, "Expected #pm 2 #sigma_{experiment}")
        textExp2.SetNDC()
        textExp2.SetTextFont(42)
        textExp2.SetTextSize(0.040)
        textExp2.Draw()
        self.c.textExp2 = textExp2
        LTheo .Draw("LSAME")
        LTheoP.Draw("LSAME")
        LTheoM.Draw("LSAME")
        LObs  .Draw("LSAME")
        LExp2S.Draw("FSAME")
        LExp2 .Draw("LSAME")
        LExp1S.Draw("FSAME")
        LExp  .Draw("LSAME")
        self.c.LExp   = LExp
        self.c.LExp1S = LExp1S
        self.c.LExp2  = LExp2  
        self.c.LExp2S = LExp2S
        self.c.LTheo  = LTheo
        self.c.LTheoP = LTheoP
        self.c.LTheoM = LTheoM
        self.c.LObs   = LObs




## run the whole damn thing
model = Model()
model.setGraphs()
plot  = ThePlot(model, histopath+"/histo_HADD.root", smearpath+"/smear_HADD.root", plotpath+"/plot", exts)
plot.prepare()
plot.draw()
plot.save()


