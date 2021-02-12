#!/usr/bin/env python

import ROOT
from ROOT import *
import xAODRootAccess.GenerateDVIterators  
import itertools
from collections import OrderedDict
import os,sys
import glob

from TruthParticleFunctions import *

# User settings
inputfile_form = "/eos/user/k/kpachal/PhaseIITrack/TruthDerivations/{0}_*/DAOD_TRUTH1.*.root"

# Print progress
verbose = True

# Which samples should we look at, and what should we do with them?
samples = {
   "slep" : {
      "doChildren" : False,
      "pdgID" : None
   },
   "rhadron" : {
      "doChildren" : True,
      "pdgID" : None
   },
   "higgsportal" : {
      "doChildren" : True,
      "pdgID" : 35
   }

}
# No slep, this is decay products only
run_on = ["rhadron"]

# Test every cut combo and save tracks passing
cuts = OrderedDict([
  ("d0_min" , [3,5,10]),
  ("d0_max" , [300]),#[100,300],
  ("pT_min" , [2,4,5,10])
])

# Standard for considering this to be triggered on
nTracksPassing = 5

## Larry magic
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
## Magic end

### Begin actual execution
for sample in run_on :

  print "Looking for",inputfile_form.format(sample),"..."
  file_list = glob.glob(inputfile_form.format(sample))
  print "Got file list",file_list
  for inputfile in file_list :

    t = readXAODFile(inputfile)

    outputFile = TFile("outputFiles/"+inputfile.replace(".root","_output.root").split("/")[-1],"RECREATE")

    if "rhadron" in sample :
      binning = (100,10000)
    else :
      binning = (50,50)

    # Histograms with one per cut combo
    histos = {}
    for d0min in cuts["d0_min"] :
      histos[d0min] = {}
      for d0max in cuts["d0_max"] :
        histos[d0min][d0max] = {}
        for pTmin in cuts["pT_min"] :
          # Want number of passing tracks per event
          title_ntracks = "h_nTracksPassing_d0min{0}_d0max{1}_pTmin{2}".format(d0min,d0max,pTmin)
          title_cutflow = "h_trackCutflow_d0min{0}_d0max{1}_pTmin{2}".format(d0min,d0max,pTmin)
          cutflow = TH1D(title_cutflow,title_cutflow,4,-0.5,3.5)
          nTracksPass = TH1D(title_ntracks,title_ntracks,binning[0],-0.5,binning[1]-0.5)
          histos[d0min][d0max][pTmin] = {"nTracks" : nTracksPass,
                                         "cutflow" : cutflow}
          # Add more here as I think of them

    # Single histograms
    nStableDecayProducts = TH1D("h_nStableDecayPerLLP","h_nStableDecayPerLLP",binning[0],-0.5,binning[1]-0.5)

    for entry in xrange( t.GetEntries() ):
      t.GetEntry( entry )

      # Collect links to interesting particles.
      pdgID = samples[sample]["pdgID"]
      doChildren = samples[sample]["doChildren"]
      myBSM = findBSMParticles(t.TruthParticles,pdgID,doChildren)

      if verbose :
        print "#"*100+"\n"+"#"*100
        print "Run: %d Event: %d -----------------------------------"%(t.EventInfo.runNumber(), t.EventInfo.eventNumber() )
        print "BSM particles:"
        for particle in myBSM :
          print particle.pdgId(),particle.status(),particle.m(),particle.p4().Pt(),particle.p4().Eta(),particle.p4().Phi()

      # Now I have useful event contents. Get relevant quantities and fill my hists.
      stable_particles = []
      for particle in myBSM :

        # Do we have a situation where the BSM particles decay? If so, let's check out their decays.
        if not doChildren : continue

        # Collect all the stable charged particles from the BSM decay
        decayProducts = findBSMDecayProducts(particle,charged=True)
        stable_particles += decayProducts

      nStableDecayProducts.Fill(len(stable_particles))

      # Now test them all according to each set of cuts.
      for cutcombo in list(itertools.product(cuts["d0_min"],cuts["d0_max"],cuts["pT_min"])):
        nTracksPass = 0
        histos[cutcombo[0]][cutcombo[1]][cutcombo[2]]["cutflow"].Fill(0)

        for track in stable_particles :
          appx_d0 = approximated0(track)
          pT = track.pt()/1000.
          if appx_d0 > cutcombo[0] :
            histos[cutcombo[0]][cutcombo[1]][cutcombo[2]]["cutflow"].Fill(1)
            if appx_d0 < cutcombo[1] :
              histos[cutcombo[0]][cutcombo[1]][cutcombo[2]]["cutflow"].Fill(2)
              if pT > cutcombo[2] :
                histos[cutcombo[0]][cutcombo[1]][cutcombo[2]]["cutflow"].Fill(3)
                nTracksPass+=1

        # Fill histos
        print "Got nTracks",nTracksPass
        histos[cutcombo[0]][cutcombo[1]][cutcombo[2]]["nTracks"].Fill(nTracksPass)

      #break

    outputFile.cd()
    # Write histograms
    for d0min in cuts["d0_min"] :
      for d0max in cuts["d0_max"] :
        for pTmin in cuts["pT_min"] :    
          hists = histos[d0min][d0max][pTmin].values()
          for hist in hists : hist.Write()
    nStableDecayProducts.Write()
    outputFile.Close()
    print "Created file",outputFile
