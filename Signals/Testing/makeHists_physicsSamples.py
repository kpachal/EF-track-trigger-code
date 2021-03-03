#!/usr/bin/env python

import ROOT
from ROOT import *
import xAODRootAccess.GenerateDVIterators  

import os,sys
import glob

from TruthParticleFunctions import *

# User settings
inputfile_form = "/eos/user/k/kpachal/PhaseIITrack/TruthDerivations/{0}_*/DAOD_TRUTH1.*.root"

# Print progress
verbose = True

# Apply 5 GeV pT cut?
doPtCut = True

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
run_on = ["higgsportal","rhadron"] 

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

    outputFileName = "outputFiles/"+inputfile.replace(".root","_output.root").split("/")[-1]
    if doPtCut :
      outputFileName = outputFileName.replace("output.root","pTcut5_output.root")
    outputFile = TFile(outputFileName,"RECREATE")

    # Histograms: BSM particles, and only tackle the decay products if possible.
    h_BSM_eta = TH1D("h_BSM_eta","h_BSM_eta", 70, -3.5 ,3.5) 
    h_BSM_phi = TH1D("h_BSM_phi","h_BSM_phi", 64, -3.2 ,3.2) 
    h_BSM_pT = TH1D("h_BSM_pT","h_BSM_pT", 200, 0, 1000)
    h_nBSM = TH1D("h_nBSM_event","h_nBSM_event",10,0,10)

    # Possible when BSM particle has decayed in sample
    h_BSM_decayRadius = TH1D("h_BSM_decayRadius","h_BSM_decayRadius", 100, 0, 300) 
    h_stableparticle_PID = TH1D("h_stableparticle_PID","h_stableparticle_PID", 400, 0 ,400) 
    h_stableparticle_eta = TH1D("h_stableparticle_eta","h_stableparticle_eta", 70, -4.0 ,4.0)
    h_stableparticle_phi = TH1D("h_stableparticle_phi","h_stableparticle_phi", 64, -3.2 ,3.2)
    h_stableparticle_pT = TH1D("h_stableparticle_pT","h_stableparticle_pT", 200, 0, 1000)
    h_stableparticle_d0 = TH1D("h_stableparticle_d0","h_stableparticle_d0", 200, -300, 300)
    h_stableparticle_z0 = TH1D("h_stableparticle_z0","h_stableparticle_z0", 200, -800, 800)

    # 2D histograms
    h_stableparticle_eta_d0 = TH2D("h_stableparticle_eta_vs_d0","h_stableparticle_eta_vs_d0", 70, -3.5, 3.5, 200, -300 ,300)  
    h_stableparticle_eta_z0 = TH2D("h_stableparticle_eta_vs_z0","h_stableparticle_eta_vs_z0", 70, -3.5, 3.5, 200, -800 ,800)   
    h_stableparticle_d0_z0 = TH2D("h_stableparticle_d0_vs_z0","h_stableparticle_do_vs_z0", 200, -300 ,300, 200, -800 ,800)

    for entry in xrange( t.GetEntries() ):
      t.GetEntry( entry )

      # Collect links to interesting particles.
      pdgID = samples[sample]["pdgID"]
      doChildren = samples[sample]["doChildren"]
      myBSM = findBSMParticles(t.TruthParticles,pdgID)

      vertices = t.TruthVertices
      #for vertex in vertices :
        #print vertex.id(), vertex.barcode(), vertex.perp(), vertex.eta(), vertex.phi()

      if verbose :
        print "#"*100+"\n"+"#"*100
        print "Run: %d Event: %d -----------------------------------"%(t.EventInfo.runNumber(), t.EventInfo.eventNumber() )
        print "BSM particles:"
        for particle in myBSM :
          print particle.pdgId(),particle.status(),particle.m(),particle.p4().Pt(),particle.p4().Eta(),particle.p4().Phi()

      # Now I have useful event contents. Get relevant quantities and fill my hists.
      h_nBSM.Fill(len(myBSM))
      for particle in myBSM :
        h_BSM_eta.Fill(particle.eta())
        h_BSM_phi.Fill(particle.phi())
        h_BSM_pT.Fill(particle.pt()/1000.)

        # Do we have a situation where the BSM particles decay? If so, let's check out their decays.
        if (doChildren) :

          # BSM particle decay vertex radius
          h_BSM_decayRadius.Fill(particle.decayVtx().perp())

          # Collect all the stable charged particles from the BSM decay
          decayProducts = findBSMDecayProducts(particle,charged=True)

          # Plot 'em
          for child in decayProducts :

            # TEST: consider only children with pT > 5 GeV
            if doPtCut :
              if (child.pt()/1000. < 5.) : continue

            h_stableparticle_PID.Fill(child.pdgId())
            h_stableparticle_eta.Fill(child.eta())
            h_stableparticle_phi.Fill(child.phi())
            h_stableparticle_pT.Fill(child.pt()/1000.)
            h_stableparticle_d0.Fill(approximated0(child))
            h_stableparticle_z0.Fill(approximatez0(child))

            h_stableparticle_eta_d0.Fill(child.eta(),approximated0(child))
            h_stableparticle_eta_z0.Fill(child.eta(),approximatez0(child))
            h_stableparticle_d0_z0.Fill(approximated0(child),approximatez0(child))
      
      #break

    outputFile.cd()
    # Write histograms
    h_nBSM.Write()
    h_BSM_eta.Write()
    h_BSM_phi.Write()
    h_BSM_pT.Write()
    if doChildren :
      h_BSM_decayRadius.Write()
      h_stableparticle_PID.Write()
      h_stableparticle_eta.Write()
      h_stableparticle_phi.Write()
      h_stableparticle_pT.Write()
      h_stableparticle_d0.Write()
      h_stableparticle_z0.Write()
      h_stableparticle_eta_d0.Write()
      h_stableparticle_eta_z0.Write()
      h_stableparticle_d0_z0.Write()
    outputFile.Close()
    print "Created file",outputFile
