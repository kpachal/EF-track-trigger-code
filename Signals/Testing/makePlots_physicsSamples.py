from art.morisot import Morisot
import glob
import ROOT
import os

# Initialize painter
myPainter = Morisot()
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

# Dir in which to look for files
file_dir = "outputFiles"                     

tag = "_pTcut5"

samples = {
   "slep" : {
      "doChildren" : False,
   },
   "rhadron" : {
      "doChildren" : True,
   },
   "higgsportal" : {
      "doChildren" : True,
   }
}
doSamples = ["higgsportal","slep","rhadron"]

for sample in doSamples :

  doChildren = samples[sample]["doChildren"]

  ## Collect histograms
  files = glob.glob(file_dir+"/DAOD_TRUTH1.*{0}*.pool{1}_output.root".format(sample,tag))
  print "Files to plot:",files

  # Get and plot histos
  for filename in files :

    namestring = filename.split("/")[-1].split(".")[1]
    print namestring
    plotdir = "plots/{0}{1}".format(namestring,tag)
    if not os.path.exists(plotdir) :
      os.mkdir(plotdir)

    openfile = ROOT.TFile.Open(filename,"READ")

    # nBSM
    h_nBSM_event = openfile.Get("h_nBSM_event")
    h_nBSM_event.SetDirectory(0)
    myPainter.drawBasicHistogram(h_nBSM_event,1,10,"Number of LLPs","Events",plotdir+"/nBSM_event",True,False,False,False,ROOT.kAzure+7)

    # LLP locations
    h_BSM_eta = openfile.Get("h_BSM_eta")
    h_BSM_eta.SetDirectory(0)
    myPainter.drawBasicHistogram(h_BSM_eta,1,h_BSM_eta.GetNbinsX(),"#eta","LLPs",plotdir+"/BSM_eta",True,False,False,False,ROOT.kAzure+7)
    h_BSM_phi = openfile.Get("h_BSM_phi")
    h_BSM_phi.SetDirectory(0)
    myPainter.drawBasicHistogram(h_BSM_phi,1,h_BSM_phi.GetNbinsX(),"#phi","LLPs",plotdir+"/BSM_phi",True,False,False,False,ROOT.kAzure+7)
    h_BSM_pT = openfile.Get("h_BSM_pT")
    h_BSM_pT.SetDirectory(0)
    myPainter.drawBasicHistogram(h_BSM_pT,1,h_BSM_pT.FindBin((500 if sample is "higgsportal" else 2000)),"p_{T} [GeV]","LLPs",plotdir+"/BSM_pT",True,True,False,False,ROOT.kAzure+7)

    # If it decays in generation:
    if doChildren :

      # LLP decay
      h_BSM_decay = openfile.Get("h_BSM_decayRadius")
      h_BSM_decay.SetDirectory(0)
      myPainter.drawBasicHistogram(h_BSM_decay,1,h_BSM_eta.FindBin(300),"Decay radius [mm]","LLPs",plotdir+"/BSM_decayRadius",True,True,False,False,ROOT.kAzure+7)

      # Charged LLP decay products
      h_particle_PID = openfile.Get("h_stableparticle_PID")
      h_particle_PID.SetDirectory(0)
      myPainter.drawBasicHistogram(h_particle_PID,1,h_particle_PID.GetNbinsX(),"Particle PID","Charged LLP decay products",plotdir+"/stableparticle_PID",True,True,False,False,ROOT.kAzure+7)      
      h_particle_eta = openfile.Get("h_stableparticle_eta")
      h_particle_eta.SetDirectory(0)
      myPainter.drawBasicHistogram(h_particle_eta,1,h_particle_eta.GetNbinsX(),"#eta","Charged LLP decay products",plotdir+"/stableparticle_eta",True,False,False,False,ROOT.kAzure+7)
      h_particle_phi = openfile.Get("h_stableparticle_phi")
      h_particle_phi.SetDirectory(0)
      myPainter.drawBasicHistogram(h_particle_phi,1,h_particle_phi.GetNbinsX(),"#phi","Charged LLP decay products",plotdir+"/stableparticle_phi",True,False,False,False,ROOT.kAzure+7)
      h_particle_pT = openfile.Get("h_stableparticle_pT")
      h_particle_pT.SetDirectory(0)
      myPainter.drawBasicHistogram(h_particle_pT,1,h_particle_pT.FindBin(100),"p_{T} [GeV]","Charged LLP decay products",plotdir+"/stableparticle_pT",True,True,False,False,ROOT.kAzure+7)      
      h_particle_d0 = openfile.Get("h_stableparticle_d0")
      h_particle_d0.SetDirectory(0)
      myPainter.drawBasicHistogram(h_particle_d0,h_particle_d0.FindBin(-300),h_particle_d0.FindBin(300),"Approximate d_{0}","Charged LLP decay products",plotdir+"/stableparticle_d0",True,True,False,False,ROOT.kAzure+7)     
      h_particle_z0 = openfile.Get("h_stableparticle_z0")
      h_particle_z0.SetDirectory(0)
      myPainter.drawBasicHistogram(h_particle_z0,h_particle_z0.FindBin(-300),h_particle_z0.FindBin(300),"Approximate z_{0}","Charged LLP decay products",plotdir+"/stableparticle_z0",True,True,False,False,ROOT.kAzure+7)     

      # 2D hists
      h_particle_eta_d0 = openfile.Get("h_stableparticle_eta_vs_d0")
      h_particle_eta_d0.SetDirectory(0)
      myPainter.draw2DHist(h_particle_eta_d0,plotdir+"/stableparticle_eta_vs_d0","#eta","Approximate d_{0}","Charged LLP decay products",-3.2,3.2,-200,200)
      h_particle_eta_z0 = openfile.Get("h_stableparticle_eta_vs_z0")
      h_particle_eta_z0.SetDirectory(0)
      myPainter.draw2DHist(h_particle_eta_z0,plotdir+"/stableparticle_eta_vs_z0","#eta","Approximate z_{0}","Charged LLP decay products",-3.2,3.2,-200,200)         
      h_particle_d0_z0 = openfile.Get("h_stableparticle_d0_vs_z0")
      h_particle_d0_z0.SetDirectory(0)
      myPainter.draw2DHist(h_particle_d0_z0,plotdir+"/stableparticle_d0_vs_z0","Approximate d_{0}","Approximate z_{0}","Charged LLP decay products",-200,200,-200,200)    

    openfile.Close()


#myPainter.drawManyOverlaidHistograms(hist_list,name_list,"m_{gluino} [GeV]","Events/1000","plots/gluino_mass","automatic","automatic",0,35,extraLegendLines=["Nominal values"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")