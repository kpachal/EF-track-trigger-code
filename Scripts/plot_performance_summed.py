import ROOT
from art.morisot import Morisot
import glob
import os

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

# Filtered DV+jets, full truth
#file_pattern = "/eos/user/k/kpachal/PhaseIITrack/HTTSim_BatchOutputs/filtered_dvjets_fullpileup_MGPy8EG_A14NNPDF23LO_GG_qqn1_2000_1950_rpvLF_1ns/straighttrack_{0}GeVthreshold_doHitFilter{1}_barCodeFrac{2}__00*/hough_lrt_tests.root"
#skip_list = []
#subdir_name = "dvjets_filtered_fulltruth_mu200"

# Unfiltered DV+jets, full truth
#file_pattern = "/eos/user/k/kpachal/PhaseIITrack/HTTSim_BatchOutputs/unfiltered_dvjets_fullpileup_MGPy8EG_A14NNPDF23LO_GG_qqn1_2000_1950_rpvLF_1ns/straighttrack_{0}GeVthreshold_doHitFilter{1}_barCodeFrac{2}__00*/hough_lrt_tests.root"
#skip_list = []
#subdir_name = "dvjets_unfiltered_fulltruth_mu200"

# Unfiltered DV+jets, full truth, zero pileup
#file_pattern = "/eos/user/k/kpachal/PhaseIITrack/HTTSim_BatchOutputs/unfiltered_dvjets_nopileup_MGPy8EG_A14NNPDF23LO_GG_qqn1_2000_1950_rpvLF_1ns/straighttrack_{0}GeVthreshold_doHitFilter{1}_barCodeFrac{2}__00*/hough_lrt_tests.root"
#skip_list = []
#subdir_name = "dvjets_unfiltered_fulltruth_nopileup"

# Plots from v0.4 of the note
# Histogram outputs have been renamed since. 
# See earlier version of code.
#file_pattern = "/eos/user/k/kpachal/PhaseIITrack/HTTSim_BatchOutputs/MGPy8EG_A14NNPDF23LO_GG_qqn1_2000_1950_rpvLF_1ns/straighttrack_{0}GeVthreshold_doHitFilter{1}_barCodeFrac{2}__00*/hough_lrt_tests.root"
#skip_list = ["000086","000394","000259","000762","001107","001109","001260","001516","001526","001605","001613","001703","001729"]
#skip_list = []
#subdir_name = "original"

extralines = ["DV+jets with pileup"]

plotdir = "plots_summed/{0}/".format(subdir_name)
if not os.path.exists(plotdir) :
  os.mkdir(plotdir)

out_hists = {}

for pTthreshold in ["5","10","15"] :
    out_hists[pTthreshold] = {}

    # Two hit filtering options
    for doHitFiltering in [False, True] :
        out_hists[pTthreshold][doHitFiltering] = {}

        # Only used one barcode frac this time
        for barcode_frac in [0.5] :#, 0.7, 0.9] :  

          inner_dict = {}

          infiles = glob.glob(file_pattern.format(pTthreshold,doHitFiltering,int(10*barcode_frac)))
          for thisfile in infiles :

            # Hacky but will work - skip if problematic
            number = thisfile.split("/")[-2].split("_")[-1]
            print number
            if number in skip_list :
              continue

            openfile = ROOT.TFile.Open(thisfile,"READ")
            
            # Three basic histograms; want prompt and lrt. Need both numerator and denominator for eff plots.
            hist_d0eff_prompt_num = openfile.Get("TruthMatchHist/RoadHist/MatchedTrackHist/h_Truth_Track_truthmatch_road_d0")
            hist_z0eff_prompt_num = openfile.Get("TruthMatchHist/RoadHist/MatchedTrackHist/h_Truth_Track_truthmatch_road_z0")
            hist_pteff_prompt_num = openfile.Get("TruthMatchHist/RoadHist/MatchedTrackHist/h_Truth_Track_truthmatch_road_pt")
            hist_d0eff_lrt_num = openfile.Get("TruthMatchHistLRT/RoadHist/MatchedTrackHist/h_Truth_Track_truthmatch_road_d0")
            hist_z0eff_lrt_num = openfile.Get("TruthMatchHistLRT/RoadHist/MatchedTrackHist/h_Truth_Track_truthmatch_road_z0")
            hist_pteff_lrt_num = openfile.Get("TruthMatchHistLRT/RoadHist/MatchedTrackHist/h_Truth_Track_truthmatch_road_pt")
            hist_nroads_prompt = openfile.Get("GeneralHist/h_nRoads")
            hist_nroads_lrt = openfile.Get("GeneralHistLRT/h_nRoads")
            hist_nroadcombos_prompt = openfile.Get("GeneralHist/h_nRoadHitCombos")
            hist_nroadcombos_lrt = openfile.Get("GeneralHistLRT/h_nRoadHitCombos")
            hist_d0eff_denom = openfile.Get("TruthMatchHist/TruthTrackHist/h_Truth_Track_Full_d0")
            hist_z0eff_denom = openfile.Get("TruthMatchHist/TruthTrackHist/h_Truth_Track_Full_z0")
            hist_pteff_denom = openfile.Get("TruthMatchHist/TruthTrackHist/h_Truth_Track_Full_pt")

            # Add them to the quantities in the inner_dict dictionary.
            if inner_dict :
              inner_dict["hist_d0eff_prompt_num"].Add(hist_d0eff_prompt_num)
              inner_dict["hist_z0eff_prompt_num"].Add(hist_z0eff_prompt_num)
              inner_dict["hist_pteff_prompt_num"].Add(hist_pteff_prompt_num)
              inner_dict["hist_d0eff_lrt_num"].Add(hist_d0eff_lrt_num)
              inner_dict["hist_z0eff_lrt_num"].Add(hist_z0eff_lrt_num)
              inner_dict["hist_pteff_lrt_num"].Add(hist_pteff_lrt_num)
              inner_dict["hist_nroads_prompt"].Add(hist_nroads_prompt)
              inner_dict["hist_nroads_lrt"].Add(hist_nroads_lrt)
              inner_dict["hist_nroadcombos_prompt"].Add(hist_nroadcombos_prompt)
              inner_dict["hist_nroadcombos_lrt"].Add(hist_nroadcombos_lrt)
              inner_dict["hist_d0eff_denom"].Add(hist_d0eff_denom)
              inner_dict["hist_z0eff_denom"].Add(hist_z0eff_denom)
              inner_dict["hist_pteff_denom"].Add(hist_pteff_denom)
            else :
              hist_d0eff_prompt_num.SetDirectory(0)
              inner_dict["hist_d0eff_prompt_num"] = hist_d0eff_prompt_num
              hist_z0eff_prompt_num.SetDirectory(0)
              inner_dict["hist_z0eff_prompt_num"] = hist_z0eff_prompt_num
              hist_pteff_prompt_num.SetDirectory(0)
              inner_dict["hist_pteff_prompt_num"] = hist_pteff_prompt_num
              hist_d0eff_lrt_num.SetDirectory(0)
              inner_dict["hist_d0eff_lrt_num"] = hist_d0eff_lrt_num
              hist_z0eff_lrt_num.SetDirectory(0)
              inner_dict["hist_z0eff_lrt_num"] = hist_z0eff_lrt_num
              hist_pteff_lrt_num.SetDirectory(0)
              inner_dict["hist_pteff_lrt_num"] = hist_pteff_lrt_num
              hist_nroads_prompt.SetDirectory(0)      
              inner_dict["hist_nroads_prompt"] = hist_nroads_prompt
              hist_nroads_lrt.SetDirectory(0)
              inner_dict["hist_nroads_lrt"] = hist_nroads_lrt
              hist_nroadcombos_prompt.SetDirectory(0)      
              inner_dict["hist_nroadcombos_prompt"] = hist_nroadcombos_prompt
              hist_nroadcombos_lrt.SetDirectory(0)
              inner_dict["hist_nroadcombos_lrt"] = hist_nroadcombos_lrt              
              hist_d0eff_denom.SetDirectory(0)
              inner_dict["hist_d0eff_denom"] = hist_d0eff_denom
              hist_z0eff_denom.SetDirectory(0)
              inner_dict["hist_z0eff_denom"] = hist_z0eff_denom
              hist_pteff_denom.SetDirectory(0)
              inner_dict["hist_pteff_denom"] = hist_pteff_denom

              # Try closing
              openfile.Close()

          # Outside file loop.

          # d0 needs some rebinning...
          inner_dict["hist_d0eff_prompt_num"].Rebin(2)
          inner_dict["hist_d0eff_lrt_num"].Rebin(2)
          inner_dict["hist_d0eff_denom"].Rebin(2)

          # And number of road and combo histograms need a LOT of rebinning.
          inner_dict["hist_nroads_prompt"].Rebin(50)
          inner_dict["hist_nroadcombos_prompt"].Rebin(50)
          inner_dict["hist_nroads_lrt"].Rebin(50)
          inner_dict["hist_nroadcombos_lrt"].Rebin(50)

          # Make TGraphs.

          eff_d0_prompt = ROOT.TGraphAsymmErrors()
          eff_d0_prompt.Divide(inner_dict["hist_d0eff_prompt_num"],inner_dict["hist_d0eff_denom"])
          inner_dict["eff_d0_prompt"] = eff_d0_prompt

          eff_z0_prompt = ROOT.TGraphAsymmErrors()
          eff_z0_prompt.Divide(inner_dict["hist_z0eff_prompt_num"],inner_dict["hist_z0eff_denom"])
          inner_dict["eff_z0_prompt"] = eff_z0_prompt

          eff_pt_prompt = ROOT.TGraphAsymmErrors()
          eff_pt_prompt.Divide(inner_dict["hist_pteff_prompt_num"],inner_dict["hist_pteff_denom"])
          inner_dict["eff_pt_prompt"] = eff_pt_prompt

          eff_d0_lrt = ROOT.TGraphAsymmErrors()
          eff_d0_lrt.Divide(inner_dict["hist_d0eff_lrt_num"],inner_dict["hist_d0eff_denom"])
          inner_dict["eff_d0_lrt"] = eff_d0_lrt

          eff_z0_lrt = ROOT.TGraphAsymmErrors()
          eff_z0_lrt.Divide(inner_dict["hist_z0eff_lrt_num"],inner_dict["hist_z0eff_denom"])
          inner_dict["eff_z0_lrt"] = eff_z0_lrt

          eff_pt_lrt = ROOT.TGraphAsymmErrors()
          eff_pt_lrt.Divide(inner_dict["hist_pteff_lrt_num"],inner_dict["hist_pteff_denom"])
          inner_dict["eff_pt_lrt"] = eff_pt_lrt

          # Put it into out_hists
          out_hists[pTthreshold][doHitFiltering][barcode_frac] = inner_dict


# Now plot every set of things we want to compare.
for doHitFiltering in [False] : # True
  for barcode_frac in [0.5] : #, 0.7, 0.9] :  

    # Compare prompt to LRT for every option
    for pTthreshold in ["5","10","15"] :

      these_hists = out_hists[pTthreshold][doHitFiltering][barcode_frac]

      out_tag = "pTCut{0}_doHitFilter{1}_barcodefrac{2}".format(pTthreshold,doHitFiltering,int(10*barcode_frac))

      myPainter.drawSeveralObservedLimits([these_hists["eff_d0_prompt"],these_hists["eff_d0_lrt"]],["Prompt HT", "LRT HT"],plotdir+out_tag+"_d0eff".format(pTthreshold),"d_{0}".format("{0}"),"Efficiency",-120,120,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=False,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

      myPainter.drawSeveralObservedLimits([these_hists["eff_z0_prompt"],these_hists["eff_z0_lrt"]],["Prompt HT", "LRT HT"],plotdir+out_tag+"_z0eff".format(pTthreshold),"p_{0} [GeV]".format("{T}"),"Efficiency",-250,250,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=True,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

      myPainter.drawSeveralObservedLimits([these_hists["eff_pt_prompt"],these_hists["eff_pt_lrt"]],["Prompt HT", "LRT HT"],plotdir+out_tag+"_pteff".format(pTthreshold),"p_{0} [GeV]".format("{T}"),"Efficiency",0,450,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=True,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

      myPainter.drawManyOverlaidHistograms([these_hists["hist_nroads_prompt"],these_hists["hist_nroads_lrt"]],["Prompt HT", "LRT HT"],"number of roads/event","Events",plotdir+out_tag+"_nroads".format(pTthreshold),hist_nroads_prompt.FindBin(0),hist_nroads_prompt.FindBin(2000),'automatic','automatic',extraLegendLines=extralines,doLogX=False,doLogY=False,doErrors=False,doLegend=True)

      myPainter.drawManyOverlaidHistograms([these_hists["hist_nroadcombos_prompt"],these_hists["hist_nroadcombos_lrt"]],["Prompt HT", "LRT HT"],"number of combinations/event","Events",plotdir+out_tag+"_nroads".format(pTthreshold),hist_nroads_prompt.FindBin(0),hist_nroads_prompt.FindBin(2000),'automatic','automatic',extraLegendLines=extralines,doLogX=False,doLogY=False,doErrors=False,doLegend=True)

      # And individual road and combination plots
      mean_nroads_prompt = these_hists["hist_nroads_prompt"].GetMean()
      myPainter.drawManyOverlaidHistograms([these_hists["hist_nroads_prompt"]],["Prompt HT"],"number of roads/event".format("{0}"),"Events",plotdir+"nroads_prompt_"+out_tag,'automatic','automatic','automatic','automatic',extraLegendLines=extralines+["Mean {0}".format(mean_nroads_prompt)],doLogY=True,doLogX=False) 
      mean_nroads_lrt = these_hists["hist_nroads_lrt"].GetMean()
      myPainter.drawManyOverlaidHistograms([these_hists["hist_nroads_lrt"]],["LRT HT"],"number of roads/event".format("{0}"),"Events",plotdir+"nroads_lrt_"+out_tag,'automatic','automatic','automatic','automatic',extraLegendLines=extralines+["Mean {0}".format(mean_nroads_lrt)],doLogY=True,doLogX=False) 
      mean_ncombos_prompt = these_hists["hist_nroadcombos_prompt"].GetMean()
      myPainter.drawManyOverlaidHistograms([these_hists["hist_nroadcombos_prompt"]],["Prompt HT"],"number of combinations/event".format("{0}"),"Events",plotdir+"ncombos_prompt_"+out_tag,'automatic','automatic','automatic','automatic',extraLegendLines=extralines+["Mean {0}".format(mean_ncombos_prompt)],doLogY=True,doLogX=False) 
      mean_ncombos_lrt = these_hists["hist_nroadcombos_lrt"].GetMean()
      myPainter.drawManyOverlaidHistograms([these_hists["hist_nroadcombos_lrt"]],["LRT HT"],"number of combinations/event".format("{0}"),"Events",plotdir+"ncombos_lrt_"+out_tag,'automatic','automatic','automatic','automatic',extraLegendLines=extralines+["Mean {0}".format(mean_ncombos_lrt)],doLogY=True,doLogX=False) 

    # Compare pT thresholds within prompt and within LRT for d0 and z0
    label_list = ["p_{0}^{1} 5 GeV".format("{T}","{min}"), "p_{0}^{1} 10 GeV".format("{T}","{min}"), "p_{0}^{1} 15 GeV".format("{T}","{min}")]

    out_tag = "prompt_comparepT_doHitFilter{0}_barcodefrac{1}".format(doHitFiltering,int(10*barcode_frac))

    myPainter.drawSeveralObservedLimits([out_hists["5"][doHitFiltering][barcode_frac]["eff_d0_prompt"],out_hists["10"][doHitFiltering][barcode_frac]["eff_d0_prompt"],out_hists["15"][doHitFiltering][barcode_frac]["eff_d0_prompt"]],label_list,plotdir+out_tag+"_d0eff".format(pTthreshold),"d_{0}".format("{0}"),"Efficiency",-120,120,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=False,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)    
    myPainter.drawSeveralObservedLimits([out_hists["5"][doHitFiltering][barcode_frac]["eff_z0_prompt"],out_hists["10"][doHitFiltering][barcode_frac]["eff_z0_prompt"],out_hists["15"][doHitFiltering][barcode_frac]["eff_z0_prompt"]],label_list,plotdir+out_tag+"_z0eff".format(pTthreshold),"z_{0}".format("{0}"),"Efficiency",-250,250,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=False,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)  

    out_tag = "lrt_comparepT_doHitFilter{0}_barcodefrac{1}".format(doHitFiltering,int(10*barcode_frac))

    myPainter.drawSeveralObservedLimits([out_hists["5"][doHitFiltering][barcode_frac]["eff_d0_lrt"],out_hists["10"][doHitFiltering][barcode_frac]["eff_d0_lrt"],out_hists["15"][doHitFiltering][barcode_frac]["eff_d0_lrt"]],label_list,plotdir+out_tag+"_d0eff".format(pTthreshold),"d_{0}".format("{0}"),"Efficiency",-120,120,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=False,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)  
        
    myPainter.drawSeveralObservedLimits([out_hists["5"][doHitFiltering][barcode_frac]["eff_z0_lrt"],out_hists["10"][doHitFiltering][barcode_frac]["eff_z0_lrt"],out_hists["15"][doHitFiltering][barcode_frac]["eff_z0_lrt"]],label_list,plotdir+out_tag+"_z0eff".format(pTthreshold),"z_{0}".format("{0}"),"Efficiency",-250,250,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=False,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

    # Plot efficiency vs pT for prompt and LRT separately. Don't need pT thresholds.

    out_tag = "prompt_doHitFilter{0}_barcodefrac{1}".format(doHitFiltering,int(10*barcode_frac))
    myPainter.drawSeveralObservedLimits([out_hists["5"][doHitFiltering][barcode_frac]["eff_pt_prompt"]],["Prompt HT"],plotdir+out_tag+"_pteff","p_{0} [GeV]".format("{T}"),"Efficiency",0,450,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=True,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)    

    out_tag = "lrt_doHitFilter{0}_barcodefrac{1}".format(doHitFiltering,barcode_frac)
    myPainter.drawSeveralObservedLimits([out_hists["5"][doHitFiltering][barcode_frac]["eff_pt_lrt"]],["LRT HT"],plotdir+out_tag+"_pteff","p_{0} [GeV]".format("{T}"),"Efficiency",0,450,0,1.5, extraLegendLines = extralines, doLogY=False,doLogX=True,doLegendLocation="Left",ATLASLabelLocation="byLegend",isTomBeingDumb=True,addHorizontalLines=[],pairNeighbouringLines=False)

# Make truth distribution plots: essentially the same, let's just do the 5 GeV cut
truth_pt = out_hists["5"][False][0.5]["hist_pteff_denom"]
truth_d0 = out_hists["5"][False][0.5]["hist_d0eff_denom"]
truth_z0 = out_hists["5"][False][0.5]["hist_z0eff_denom"]

myPainter.drawBasicHistogram(truth_pt,1,truth_pt.GetNbinsX()+1,"p_{0} [GeV]".format("{T}"),"Truth tracks",outputname=plotdir+"truth_pt",doLogY=True,doLogX=True,doErrors=False,fillColour = ROOT.kAzure+5) 
#myPainter.drawManyOverlaidHistograms([truth_pt],["LRT HT"],"number of combinations/event".format("{0}"),"Events",outputname=plotdir+"ncombos_lrt_"+out_tag,'automatic','automatic','automatic','automatic',extraLegendLines=extralines,doLogY=True,doLogX=False)
myPainter.drawBasicHistogram(truth_d0,1,truth_d0.GetNbinsX()+1,"d_{0} [mm]".format("{0}"),"Truth tracks",outputname=plotdir+"truth_d0",doLogY=True,doLogX=False,doErrors=False,fillColour = ROOT.kAzure+5) 
myPainter.drawBasicHistogram(truth_z0,1,truth_z0.GetNbinsX()+1,"z_{0} [GeV]".format("{0}"),"Truth tracks",outputname=plotdir+"truth_z0",doLogY=True,doLogX=False,doErrors=False,fillColour = ROOT.kAzure+5) 