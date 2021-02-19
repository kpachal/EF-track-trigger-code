#!/usr/bin/env python

import ROOT
from ROOT import *
import xAODRootAccess.GenerateDVIterators  

import os,sys
import glob

from TruthParticleFunctions import *

# User settings
inputfile_form = "/eos/user/k/kpachal/PhaseIITrack/TruthDerivations/fromJahred/DAOD_TRUTH1.*.root"

# Print progress
verbose = True

# Which particles are we looking for?
# This code assumes that these particles are produced
# at a potentially displaced vertex and will make plots accordingly
pdgID = 13
label = "muons"

## Larry magic
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
## Magic end

### Begin actual execution
print "Looking for",inputfile_form,"..."
file_list = glob.glob(inputfile_form)
print "Got file list",file_list
for inputfile in file_list :

  t = readXAODFile(inputfile)

  outputFile = TFile("outputFiles/"+inputfile.replace(".root","_output.root").split("/")[-1],"RECREATE")

  # Histograms
  h_vertex_eta = TH1D("h_prodvertex_eta","h_prodvertex_eta", 70, -3.5 ,3.5) 
  h_vertex_phi = TH1D("h_prodvertex_phi","h_prodvertex_phi", 64, -3.2 ,3.2) 
  h_particle_prodRadius = TH1D("h_distance_to_prodvertex","h_distance_to_prodvertex", 100, 0, 300) 

  h_stableparticle_PID = TH1D("h_stableparticle_PID","h_stableparticle_PID", 20, 0 ,20) 
  h_stableparticle_eta = TH1D("h_stableparticle_eta","h_stableparticle_eta", 70, -3.5 ,3.5)
  h_stableparticle_phi = TH1D("h_stableparticle_phi","h_stableparticle_phi", 64, -3.2 ,3.2)
  h_stableparticle_pT = TH1D("h_stableparticle_pT","h_stableparticle_pT", 200, 0, 1000)
  h_stableparticle_d0 = TH1D("h_stableparticle_d0","h_stableparticle_d0", 100, 0 ,300)
  h_nParticles = TH1D("h_nParticles_event","h_nParticles_event",10,0,10)

  for entry in xrange( t.GetEntries() ):
    t.GetEntry( entry )

    # Collect links to particles.
    myparticles = findBSMParticles(t.TruthParticles,pdgID)

    vertices = t.TruthVertices

    if verbose :
      print "#"*100+"\n"+"#"*100
      print "Run: %d Event: %d -----------------------------------"%(t.EventInfo.runNumber(), t.EventInfo.eventNumber() )
      print "My interesting particles:"
      for particle in myparticles :
        print particle.pdgId(),particle.status(),particle.m(),particle.p4().Pt(),particle.p4().Eta(),particle.p4().Phi()

    # Now I have useful event contents. Get relevant quantities and fill my hists.
    h_nParticles.Fill(len(myparticles))
    for particle in myparticles :

      # Particles' production vertex
      prodVertex = particle.prodVtx() 
      h_vertex_eta.Fill(prodVertex.eta())
      h_vertex_phi.Fill(prodVertex.phi())
      h_particle_prodRadius.Fill(prodVertex.perp())

      # Now the particles themselves
      h_stableparticle_PID.Fill(abs(particle.pdgId()))
      h_stableparticle_eta.Fill(particle.eta())
      h_stableparticle_phi.Fill(particle.phi())
      h_stableparticle_pT.Fill(particle.pt()/1000.)
      h_stableparticle_d0.Fill(approximated0(particle))
    
    #break

  outputFile.cd()
  # Write histograms
  h_vertex_eta.Write()
  h_vertex_phi.Write()
  h_particle_prodRadius.Write()
  h_stableparticle_PID.Write()
  h_stableparticle_eta.Write()
  h_stableparticle_phi.Write()
  h_stableparticle_pT.Write()
  h_stableparticle_d0.Write()
  h_nParticles.Write()
  outputFile.Close()
  print "Created file",outputFile
