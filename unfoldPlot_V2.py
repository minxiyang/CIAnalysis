import argparse	
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath, gROOT
import ratios
from setTDRStyle import setTDRStyle
gROOT.SetBatch(True)
from helpers import *
from defs import getPlot, Backgrounds, Backgrounds2016, Backgrounds2018, Signals, Signals2016, Signals2016ADD, SignalsADD, Signals2018ADD, Signals2018, Data, Data2016, Data2018, path, plotList, zScale, zScale2016, zScale2018
import math
import os
from copy import copy


def plotDataMC(datahist,mchist,usedata, label1, label2,name,filename):
	

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	if usedata==True:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
                ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
                setTDRStyle()
                plotPad.UseCurrentStyle()
                ratioPad.UseCurrentStyle()
                plotPad.Draw("hist")
                ratioPad.Draw("hist")
                plotPad.cd()
        else:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
                setTDRStyle()
                plotPad.UseCurrentStyle()
                plotPad.Draw()
                plotPad.cd()	
	colors = createMyColors()		
	legend = TLegend(0.55, 0.6, 0.925, 0.925)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	legend.SetTextFont(42)
	legendEta = TLegend(0.45, 0.75, 0.925, 0.925)
	legendEta.SetFillStyle(0)
	legendEta.SetBorderSize(0)
	legendEta.SetTextFont(42)
	legendEta.SetNColumns(2)
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.06)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.045)
	latexCMSExtra.SetNDC(True)	
	legendHists = []
	legendHistData = ROOT.TH1F()
	category = ROOT.TLatex()
	category.SetNDC(True)
	category.SetTextSize(0.04)
	if usedata==True:	
		legend.AddEntry(legendHistData,label1,"pe")	
		legendEta.AddEntry(legendHistData,label1,"pe")	

	#process.label = process.label.replace("#mu^{+}#mu^{-}","e^{+^{*}}e^{-}")
	temphist = ROOT.TH1F()
	if label2=="Generated":
		temphist.SetFillColor(3)
		mchist.SetFillColor(3)
	else:
		temphist.SetFillColor(2)
		mchist.SetFillColor(2)
	legendHists.append(temphist.Clone)
	legend.AddEntry(temphist,label2,"f")
	#legendEta.AddEntry(temphist,process.label,"f")
	
	# Modify plot pad information	
	nEvents=-1

	ROOT.gStyle.SetOptStat(0)
	
	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.045)
	intlumi.SetNDC(True)
	intlumi2 = ROOT.TLatex()
	intlumi2.SetTextAlign(12)
	intlumi2.SetTextSize(0.07)
	intlumi2.SetNDC(True)
	scalelabel = ROOT.TLatex()
	scalelabel.SetTextAlign(12)
	scalelabel.SetTextSize(0.03)
	scalelabel.SetNDC(True)
	metDiffLabel = ROOT.TLatex()
	metDiffLabel.SetTextAlign(12)
	metDiffLabel.SetTextSize(0.03)
	metDiffLabel.SetNDC(True)
	chi2Label = ROOT.TLatex()
	chi2Label.SetTextAlign(12)
	chi2Label.SetTextSize(0.03)
	chi2Label.SetNDC(True)
	hCanvas.SetLogy()


	# Luminosity information	
	plotPad.cd()
	plotPad.SetLogy(0)
	plotPad.SetLogy()
	if usedata==True:
		yMax = datahist.GetBinContent(datahist.GetMaximumBin())*1000
		yMin = 0.00000001
		xMax = datahist.GetXaxis().GetXmax()
		xMin = datahist.GetXaxis().GetXmin()
	else:	
		yMax = mchist.GetBinContent(datahist.GetMaximumBin())
		yMin = 0.00000001
		xMax = mchist.GetXaxis().GetXmax()
		xMin = mchist.GetXaxis().GetXmin()	
		yMax = yMax*10000
	if name.find("dimuon")!=-1:
		plotPad.DrawFrame(xMin,yMin,xMax,yMax,"; m_{#mu#mu}[GeV] ;fb/GeV")
        else:
		plotPad.DrawFrame(xMin,yMin,xMax,yMax,"; m_{ee}[GeV] ;fb/GeV")
	
	
	# Draw signal information
	
	# Draw background from stack
	mchist.Draw("samehist")		

	# Draw data
	datahist.SetMinimum(0.0001)
	if usedata==True:
		datahist.SetMarkerStyle(8)
		datahist.Draw("samepehist")	

	# Draw legend
	legend.Draw()
	plotPad.SetLogx()
	latex.DrawLatex(0.95,0.96,"13 TeV")
	yLabelPos = 0.85
	cmsExtra = "Preliminary"
	if not usedata==True:
		cmsExtra = "#splitline{Preliminary}{Simulation}"
		yLabelPos = 0.82	
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	category.DrawLatex(0.3,0.7,name)
	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	#~ print datahist.Integral()
	if usedata==True:
		try:
			ratioPad.cd()
			ratioPad.SetLogx()
		except AttributeError:
			print ("Plot fails. Look up in errs/failedPlots.txt")
			outFile =open("errs/failedPlots.txt","a")
			outFile.write('%s\n'%plot.filename%("_"+run.label+"_"+dilepton))
			outFile.close()
			#plot.cuts=baseCut
			return 1
		if label2=="Generated":
			ratioGraphs =  ratios.RatioGraph(datahist,mchist, xMin=xMin, xMax=xMax,title="	nokFac/kFac",yMin=0.7,yMax=1.3,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=10000000000000,labelSize=0.125,pull=False)
			ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)

		else:
			ratioGraphs =  ratios.RatioGraph(datahist,mchist, xMin=xMin, xMax=xMax,title="nokFac/kFac",yMin=0.7,yMax=1.3,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=10000000000000,labelSize=0.125,pull=False)
			ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
					

	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	if usedata==True:

		ratioPad.RedrawAxis()
	if not os.path.exists("plots"):
		os.makedirs("plots")	
	hCanvas.Print("plots/%s.pdf"%filename)

					

						
f=ROOT.TFile.Open("RooUnfold/kFacTest.root")
h_mu=f.Get("muon_combine_combine_recoMass_combine")
h_mu_kFac=f.Get("muon_combine_combine_recoMass_combine_kFac")
h_el=f.Get("electron_combine_combine_recoMass_combine")
h_el_kFac=f.Get("electron_combine_combine_recoMass_combine_kFac")


plotDataMC(h_mu_kFac,h_mu,True,"kFac/o","kFac/w","reco dimuon","rec_MukFac")
plotDataMC(h_el_kFac,h_el,True,"kFac/o","kFac/w","reco dielectron","rec_elkFac")




