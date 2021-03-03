from art.morisot import Morisot
import glob
import ROOT
import os

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

# Turn off CME and luminosity labels
myPainter.luminosity = -1000
myPainter.CME = -100

# 0 Just ATLAS    
# 1 "Preliminary"
# 2 "Internal"
# 3 "Simulation Preliminary"
# 4 "Simulation Internal"
# 5 "Simulation"
# 6 "Work in Progress"

# Dir in which to look for files
file_dir = "outputFiles"                     

doSamples = ["etaFlat0103","etaFlat0709","etaFlat1214","etaFlat3234"]

sum2DHists = {"h_stableparticle_eta_vs_d0" : None,
              "h_stableparticle_eta_vs_z0" : None,
              "h_stableparticle_d0_vs_z0" : None}

for sample in doSamples :

  ## Collect histograms
  files = glob.glob(file_dir+"/DAOD_TRUTH1.*{0}*output.root".format(sample))
  print "Files to plot:",files

  # Get and plot histos
  for filename in files :

   namestring = filename.split("/")[-1].split(".")[3]
   print namestring
   plotdir = "plots/{0}".format(namestring)
   if not os.path.exists(plotdir) :
     os.mkdir(plotdir)

   openfile = ROOT.TFile.Open(filename,"READ")

   # Production info
   h_r_decay = openfile.Get("h_distance_to_prodvertex")
   h_r_decay.SetDirectory(0)
   myPainter.drawBasicHistogram(h_r_decay,1,h_r_decay.FindBin(300),"Production radius [mm]","Muons",plotdir+"/distance_to_prodvertex",True,True,False,False,ROOT.kAzure+7)
      
   # Vertex locations
   h_vertex_eta = openfile.Get("h_prodvertex_eta")
   h_vertex_eta.SetDirectory(0)
   myPainter.drawBasicHistogram(h_vertex_eta,1,h_vertex_eta.GetNbinsX(),"Origin #eta","Muons",plotdir+"/vertex_eta",True,False,False,False,ROOT.kAzure+7)
   h_vertex_phi = openfile.Get("h_prodvertex_phi")
   h_vertex_phi.SetDirectory(0)
   myPainter.drawBasicHistogram(h_vertex_phi,1,h_vertex_phi.GetNbinsX(),"Origin #phi","Muons",plotdir+"/vertex_phi",True,False,False,False,ROOT.kAzure+7)

   # Muons themselves 
   h_particle_eta = openfile.Get("h_stableparticle_eta")
   h_particle_eta.SetDirectory(0)
   myPainter.drawBasicHistogram(h_particle_eta,1,h_particle_eta.GetNbinsX(),"#eta","Muon",plotdir+"/stableparticle_eta",True,False,False,False,ROOT.kAzure+7)
   h_particle_phi = openfile.Get("h_stableparticle_phi")
   h_particle_phi.SetDirectory(0)
   myPainter.drawBasicHistogram(h_particle_phi,1,h_particle_phi.GetNbinsX(),"#phi","Muon",plotdir+"/stableparticle_phi",True,False,False,False,ROOT.kAzure+7)
   h_particle_pT = openfile.Get("h_stableparticle_pT")
   h_particle_pT.SetDirectory(0)
   myPainter.drawBasicHistogram(h_particle_pT,1,h_particle_pT.FindBin(100),"p_{T} [GeV]","Muon",plotdir+"/stableparticle_pT",True,True,False,False,ROOT.kAzure+7)      
   h_particle_d0 = openfile.Get("h_stableparticle_d0")
   h_particle_d0.SetDirectory(0)
   myPainter.drawBasicHistogram(h_particle_d0,1,h_particle_d0.FindBin(300),"Approximate d_{0}","Muon",plotdir+"/stableparticle_d0",True,True,False,False,ROOT.kAzure+7)     
   h_particle_z0 = openfile.Get("h_stableparticle_z0")
   h_particle_z0.SetDirectory(0)
   myPainter.drawBasicHistogram(h_particle_z0,h_particle_z0.FindBin(-300),h_particle_z0.FindBin(300),"Approximate z_{0}","Muon",plotdir+"/stableparticle_z0",True,True,False,False,ROOT.kAzure+7)  

   # 2D hists
   h_particle_eta_d0 = openfile.Get("h_stableparticle_eta_vs_d0")
   h_particle_eta_d0.SetDirectory(0)
   myPainter.draw2DHist(h_particle_eta_d0,plotdir+"/stableparticle_eta_vs_d0","#eta","Approximate d_{0}","Muons",-4.0,4.0,-200,200)
   if not sum2DHists["h_stableparticle_eta_vs_d0"] :
     sum2DHists["h_stableparticle_eta_vs_d0"] = h_particle_eta_d0
   else :
     sum2DHists["h_stableparticle_eta_vs_d0"].Add(h_particle_eta_d0)

   h_particle_eta_z0 = openfile.Get("h_stableparticle_eta_vs_z0")
   h_particle_eta_z0.SetDirectory(0)
   myPainter.draw2DHist(h_particle_eta_z0,plotdir+"/stableparticle_eta_vs_z0","#eta","Approximate z_{0}","Muons",-4.0,4.0,-200,200)   
   if not sum2DHists["h_stableparticle_eta_vs_z0"] :
     sum2DHists["h_stableparticle_eta_vs_z0"] = h_particle_eta_z0
   else :
     sum2DHists["h_stableparticle_eta_vs_z0"].Add(h_particle_eta_z0)

   h_particle_d0_z0 = openfile.Get("h_stableparticle_d0_vs_z0")
   h_particle_d0_z0.SetDirectory(0)
   myPainter.draw2DHist(h_particle_d0_z0,plotdir+"/stableparticle_d0_vs_z0","Approximate d_{0}","Approximate z_{0}","Charged LLP decay products",-200,200,-200,200)
   if not sum2DHists["h_stableparticle_d0_vs_z0"] :
     sum2DHists["h_stableparticle_d0_vs_z0"] = h_particle_d0_z0
   else :
     sum2DHists["h_stableparticle_d0_vs_z0"].Add(h_particle_d0_z0)

   openfile.Close()

myPainter.draw2DHist(sum2DHists["h_stableparticle_eta_vs_d0"],"plots/sumsinglemu_stableparticle_eta_vs_d0","#eta","Approximate d_{0}","Muons",-4.0,4.0,-200,200)

myPainter.draw2DHist(sum2DHists["h_stableparticle_eta_vs_z0"],"plots/sumsinglemu_stableparticle_eta_vs_z0","#eta","Approximate z_{0}","Muons",-4.0,4.0,-200,200)

myPainter.draw2DHist(sum2DHists["h_stableparticle_d0_vs_z0"], "plots/sumsinglemu_stableparticle_d0_vs_z0","Approximate d_{0}","Approximate z_{0}","Charged LLP decay products",-200,200,-200,200)