import ROOT
from art.morisot import Morisot

# Initialize painter
myPainter = Morisot()
myPainter.luminosity = None
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation
# 0 Just ATLAS
# 1 "Preliminary"
# 2 "Internal"
# 3 "Simulation Preliminary"
# 4 "Simulation Internal"
# 5 "Simulation"
# 6 "Work in Progress"

# Input files
infiles = {#"dvjets" : "/afs/cern.ch/work/k/kpachal/PhaseIITrack/HTTSim/workspace/rundir_hough_dvjets/hough_lrt_tests.root",
           "singlemu_nopileup" : "/afs/cern.ch/work/k/kpachal/PhaseIITrack/HTTSim/workspace/rundir_hough_displacedsinglemu_bad/hough_lrt_tests.root"}

extralines = {"dvjets" : "DV+jets with pileup",
              "singlemu_nopileup" : "Single displaced muon, no pileup"}

plotdir = "plots_basic/"

for tag,thefile in infiles.items() :

  openfile = ROOT.TFile.Open(thefile,"READ")

  # Three basic histograms; want prompt and lrt
  hist_d0eff_prompt = openfile.Get("TruthMatchHist/RoadHist/EffHist/h_RoadEfficiency_truthmatch_d0")
  hist_pteff_prompt = openfile.Get("TruthMatchHist/RoadHist/EffHist/h_RoadEfficiency_truthmatch_pt")
  hist_nroads_prompt = openfile.Get("GeneralHist/h_nRoads")
  hist_d0eff_lrt = openfile.Get("TruthMatchHistLRT/RoadHist/EffHist/h_RoadEfficiency_truthmatch_d0")
  hist_pteff_lrt = openfile.Get("TruthMatchHistLRT/RoadHist/EffHist/h_RoadEfficiency_truthmatch_pt")
  hist_nroads_lrt = openfile.Get("GeneralHistLRT/h_nRoads")

  # Compare the efficiencies
  myPainter.drawSeveralObservedLimits([hist_d0eff_prompt,hist_d0eff_lrt],["Prompt HT", "LRT HT"],plotdir+"{0}_d0eff".format(tag),"d_{0}".format("{0}"),"Efficiency",-120,120,0,1.3, extraLegendLines = [extralines[tag]], doLogY=False,doLogX=False,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

  myPainter.drawSeveralObservedLimits([hist_pteff_prompt,hist_pteff_lrt],["Prompt HT", "LRT HT"],plotdir+"{0}_pteff".format(tag),"p_{0} [GeV]".format("{T}"),"Efficiency",0,450,0,1.3, extraLegendLines = [extralines[tag]], doLogY=False,doLogX=True,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

  myPainter.drawManyOverlaidHistograms([hist_nroads_prompt,hist_nroads_lrt],["Prompt HT", "LRT HT"],"number of roads/event","Events",plotdir+"{0}_nroads".format(tag),hist_nroads_prompt.FindBin(0),hist_nroads_prompt.FindBin(50),'automatic','automatic',extraLegendLines=[extralines[tag]],doLogX=False,doLogY=False,doErrors=False,doLegend=True)
