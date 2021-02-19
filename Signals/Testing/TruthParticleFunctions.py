#!/usr/bin/env python

import ROOT
from ROOT import *
#import xAODRootAccess.GenerateDVIterators  

import os,sys
import math

## Larry magic
#ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
## Magic end

def readXAODFile(filename) :

  file = TFile(filename)
  t = ROOT.xAOD.MakeTransientTree( file )

  auxDataCode = """
  bool auxdataConstBool( const SG::AuxElement& el, const std::string& name ) {
     return el.auxdata< char >( name );
  }
  """
  ROOT.gInterpreter.Declare(auxDataCode)

  return t

#def estimated0(particle,)

def decaysToSelf(particle) :
  notSelfDecay = True
  for child in particle.decayVtx().outgoingParticleLinks() :
    if ( child.absPdgId() == particle.absPdgId() and child.barcode()!=particle.barcode() and child.barcode() < 100000) :
        notSelfDecay = False
        break
  return not notSelfDecay


def findBSMParticles(truthparticles,PDGID=None) :

  BSM_particles = []
  for iparticle,particle in enumerate(truthparticles):

    # Handed it a PDG ID?
    if PDGID :
      if particle.absPdgId() != PDGID :
        continue

    # Otherwise, interested in SUSY particles only
    elif particle.absPdgId()<999999:
      continue

    # Find stable particles or particle not decaying into itself
    if particle.hasDecayVtx() :
      if not decaysToSelf(particle) :
        BSM_particles.append(particle)
    else :
      BSM_particles.append(particle)

  return BSM_particles

# Just a basic straight-lines based approximation.
# Assume origin is 0,0
def approximated0(particle) :

  # Approach nicked from displaced leptons
  # https://gitlab.cern.ch/atlas-phys-susy-wg/RPVLL/displacedleptons/scripts/-/blob/master/idTracks/AODTracks.py
  vertex_vector = ROOT.TVector3()
  vertex_vector.SetPtEtaPhi(particle.prodVtx().perp(),particle.prodVtx().eta(), particle.prodVtx().phi())
  child_vector = ROOT.TVector3()
  child_vector.SetPtEtaPhi(particle.pt(), particle.eta(), particle.phi())

  r = particle.prodVtx().perp()
  delta_phi = vertex_vector.DeltaPhi(child_vector)
  approx_d0 = r * math.sin(abs(delta_phi))
  return(approx_d0)

# Depth-first search of particle decay paths
# Based on this stackoverflow example:
#https://stackoverflow.com/questions/59132538/counting-the-length-of-each-branch-in-a-binary-tree-and-print-out-the-nodes-trav
def dfs_paths(stack, particle, stable_particles = []): 

    if particle == None: 
        return

    # append this particle ID to the path array 
    stack.append(particle.barcode()) 

    # If this particle is the end of the chain, save it
    if(not particle.hasDecayVtx()): 

        # Check status
        if particle.status() != 1 :
          print("Uh oh! Stable particle has status",particle.status())
          exit(1)

        # Append  
        stable_particles.append(particle)

    # Otherwise try each particle from decay
    else :
      for child in particle.decayVtx().outgoingParticleLinks() :
        dfs_paths(stack, child, stable_particles) 
    
    # Magic
    stack.pop() 

# Only works if you decayed the parent in the generation
# step, or you're running this on a post-simulation xAOD
def findBSMDecayProducts(particle,charged=True) :

  stable_descendents = []
  dfs_paths([],particle,stable_descendents)
  
  # If we want charged only, subdivide
  if charged :
    children = [i for i in stable_descendents if i.isCharged()]
    return children
  else :
    return stable_descendents
