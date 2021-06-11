import ROOT
from art.morisot import Morisot


# Initialize painter
myPainter = Morisot()
myPainter.luminosity = None
myPainter.CME = None
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
file_pattern = "/eos/user/k/kpachal/PhaseIITrack/HTTSim_BatchOutputs/MGPy8EG_A14NNPDF23LO_GG_qqn1_2000_1950_rpvLF_1ns/straighttrack_{0}GeVthreshold_doHitFilter{1}_barCodeFrac{2}__000051/HoughTransform_d0phi0_0.root"

extralines = ["DV+jets with pileup"]

plotdir = "plots_accumulators/"

for pTthreshold in ["5","10","15"] :

    # Two hit filtering options
    for doHitFiltering in [True, False] :

        # Three cut thresholds for barcode matching
        for barcode_frac in [0.5, 0.7, 0.9] :  

          thisfile = file_pattern.format(pTthreshold,doHitFiltering,int(10*barcode_frac))

          openfile = ROOT.TFile.Open(thisfile,"READ")

          # Get our 5 - something to choose from
          for event in range(5) :
            hist = openfile.Get("HoughTransform_d0phi0_0_{0}".format(event))
            hist.SetDirectory(0)
          
            # Plot 
            outname = "accumulator_pTCut{0}_doHitFilter{1}_barcodefrac{2}_event{3}".format(pTthreshold,doHitFiltering,int(10*barcode_frac),event)
            myPainter.draw2DHist(hist,plotdir+outname,"#phi","d_{0}".format("{0}"),"Hits")