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

cuts = {
  "d0_min" : [3,5,10],
  "d0_max" : [300],
  "pT_min" : [2,4,5,10]
}

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
doSamples = ["rhadron"]

for sample in doSamples :

  ## Collect histograms
  files = glob.glob(file_dir+"/DAOD_TRUTH1.*{0}*.pool_output.root".format(sample))
  print "Files to plot:",files

  # Get and plot histos
  for filename in files :

   namestring = filename.split("/")[-1].split(".")[1]
   print namestring
   plotdir = "plots/{0}".format(namestring)
   if not os.path.exists(plotdir) :
     os.mkdir(plotdir)

   openfile = ROOT.TFile.Open(filename,"READ")
   openfile.ls()
   histnames = []
   for d0min in cuts["d0_min"] :
      for d0max in cuts["d0_max"] :
         for pTmin in cuts["pT_min"] :    
            histnames.append("nTracksPassing_d0min{0}_d0max{1}_pTmin{2}".format(d0min,d0max,pTmin))
   
   histlist = {}
   for histname in histnames:

      hist = openfile.Get("h_"+histname)
      print "Getting","h_"+histname
      hist.SetDirectory(0)
      myPainter.drawBasicHistogram(hist,1,hist.GetNbinsX(),"Number of tracks surviving cut","Events",plotdir+"/"+histname,True,False,False,False,ROOT.kAzure+7)

      #histlist[]
  
   openfile.Close()


#myPainter.drawManyOverlaidHistograms(hist_list,name_list,"m_{gluino} [GeV]","Events/1000","plots/gluino_mass","automatic","automatic",0,35,extraLegendLines=["Nominal values"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")