from MadGraphControl.MadGraphUtils import *

#############################################
### Production of scalar long-lived particles
### though a higgs-like scalar mediator
### Kate obtained job options from here:
### https://its.cern.ch/jira/browse/ATLMCPROD-6900
### However, original analysis treats lifetime
### as a distance.
### We prefer it as an actual lifetime.
### So I have modified the lifetime function to decaydistance.
############################################

# Set up to save HepMC
import AthenaCommon.AlgSequence as acas
topAlg = acas.AlgSequence()
from TruthIO.TruthIOConf import WriteHepMC
topAlg += WriteHepMC()

# PDF
pdflabel = 'lhapdf'
lhaid = 315000 # NNPDF31_lo_as_0118

# parameter mass and average life-time
phys_short = get_physics_short()
infoStrings = phys_short.split("_")
def StringToFloat(s):
  ss=s.replace("ns","")
  if "p" in ss:
    return float(ss.replace("p", "."))
  return float(ss)

mH = StringToFloat(infoStrings[4])
mhS = StringToFloat(infoStrings[5])
lifetime_nom = StringToFloat(infoStrings[6])
print("LIFETIME:",lifetime_nom)

# basename for madgraph LHEF file
rname = 'run_01'

#---------------------------------------------------------------------------
# MG5 Proc card
#---------------------------------------------------------------------------

modelcode='HAHM_variableMW_v3_UFO'
process = '''
import model '''+modelcode+'''
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define f = u c d s u~ c~ d~ s~ b b~ e+ e- mu+ mu- ta+ ta- t t~
generate g g > h HIG=1 HIW=0 QED=0 QCD=0, (h > h2 h2, h2 > f f)
output -f
'''

process_dir = new_process(process)

#---------------------------------------------------------------------------
# Energy
#---------------------------------------------------------------------------
    
beamEnergy = -999.
if hasattr(runArgs,'ecmEnergy'):
    beamEnergy = runArgs.ecmEnergy / 2.
else:
   raise RuntimeError("No center of mass energy found")

#---------------------------------------------------------------------------
# MG5 Run Card
#---------------------------------------------------------------------------

run_card_extras = { 
    'lhe_version':'3.0',
    'cut_decays':'F',
    'event_norm':'sum',
    'pdlabel':pdflabel,
    'lhaid':lhaid,
    'ptj':'0',
    'ptb':'0',
    'pta':'0',
    'ptl':'0',
    'etaj':'-1',
    'etab':'-1',
    'etaa':'-1',
    'etal':'-1',
    'drjj':'0',
    'drbb':'0',
    'drll':'0',
    'draa':'0',
    'drbj':'0',
    'draj':'0',
    'drjl':'0',
    'drab':'0',
    'drbl':'0',
    'dral':'0' ,
    'use_syst':'T',
    'sys_scalefact': '1 0.5 2',
    'sys_pdf'      : "NNPDF31_lo_as_0118"
    }

safefactor=1.1 #generate extra 10% events in case any fail showering
if runArgs.maxEvents > 0: 
    nevents = runArgs.maxEvents*safefactor
else: nevents = 5000*safefactor

modify_run_card(run_card_input=get_default_runcard(process_dir),
                run_card_backup=process_dir+'/Cards/run_card_backup.dat',
                process_dir=process_dir,
                runArgs=runArgs,
                settings=run_card_extras)

#---------------------------------------------------------------------------
# MG5 param Card
#---------------------------------------------------------------------------

if mH <= 125: 
    param_card_extras = { 
        "HIDDEN": { 'epsilon': '1e-10', #kinetic mixing parameter
                    'kap': '1e-4', #higgs mixing parameter
                    'mhsinput':mhS, #dark higgs mass
                    'mzdinput': '1.000000e+03' # Z' mass
                    }, 
        "HIGGS": { 'mhinput':mH}, #higgs mass
        #auto-calculate decay widths and BR of Zp, H, t, hs
        "DECAY": { 'wzp':'Auto', 'wh':'Auto', 'wt':'Auto', 'whs':'Auto'} 
        }
elif mH > 125:
    param_card_extras = { 
        "HIDDEN": { 'epsilon': '1e-10', #kinetic mixing parameter
                    'kap': '1e-4', #higgs mixing parameter
                    'mhsinput':mhS, #dark higgs mass
                    'mzdinput': '1.000000e+03' # Z' mass
                    }, 
        "HIGGS": { 'mhinput':mH}, #higgs mass
        #auto-calculate decay widths and BR of Zp, H, t, hs
        "DECAY": { 'wzp':'5', 'wh':'5', 'wt':'Auto', 'whs':'5'} 
        }

modify_param_card(process_dir=process_dir, 
    param_card_backup=process_dir+'/Cards/param_card_backup.dat',
    params=param_card_extras)

print_cards()

#---------------------------------------------------------------------------
# MG5 Generation
#---------------------------------------------------------------------------

generate(process_dir=process_dir,
         runArgs=runArgs)#,

#---------------------------------------------------------------------------
# Arrange LHE file output
#---------------------------------------------------------------------------

# initialise random number generator/sequence
import random
random.seed(runArgs.randomSeed)
# lifetime function
# Modified to match Madgraph add_time_of_flight function:
# https://bazaar.launchpad.net/~madteam/mg5amcnlo/series2.0/view/head:/madgraph/interface/madevent_interface.py#L2196
# Therefore needs to be converted from lifetime in ns to distance in mm.
def decaydistance(avgtau = 21):
    import math
    # Convert lifetime to seconds
    tau_s = avgtau * 1e-9
    # speed of light in mm/s
    c = 299792458000
    # distance in mm   
    vtau = c * random.expovariate(1./tau_s)
    return vtau
    

# replacing lifetime of scalar, manually
unzip1 = subprocess.Popen(['gunzip',process_dir+'/Events/'+rname+'/unweighted_events.lhe.gz'])
unzip1.wait()
    
oldlhe = open(process_dir+'/Events/'+rname+'/unweighted_events.lhe','r')
newlhe = open(process_dir+'/Events/'+rname+'/unweighted_events2.lhe','w')

# TEST
#import madgraph.various.lhe_parser as lhe_parser
#lhe = lhe_parser.EventFile(process_dir+'/Events/'+rname+'/unweighted_events.lhe')

init = True
for line in oldlhe:
    if init==True:
        newlhe.write(line)
        if '</init>' in line:
            init = False
    else:  
        if 'vent' in line or line.startswith("<"):
            newlhe.write(line)
            continue
        newline = line.rstrip('\n')
        columns = (' '.join(newline.split())).split()
        pdgid = int(columns[0])
        if pdgid == 35:
            part1 = line[:-22]
            part2 = "%.11E" % (decaydistance(lifetime_nom))
            part3 = line[-12:]
            newlhe.write(part1+part2+part3)
        else:
            newlhe.write(line)

oldlhe.close()
newlhe.close()
    
zip1 = subprocess.Popen(['gzip',process_dir+'/Events/'+rname+'/unweighted_events2.lhe'])
zip1.wait()
shutil.move(process_dir+'/Events/'+rname+'/unweighted_events2.lhe.gz',
            process_dir+'/Events/'+rname+'/unweighted_events.lhe.gz')
os.remove(process_dir+'/Events/'+rname+'/unweighted_events.lhe')

arrange_output(process_dir=process_dir,
               lhe_version=3,
               saveProcDir=True,
               runArgs=runArgs)

#---------------------------------------------------------------------------
# Parton Showering Generation
#---------------------------------------------------------------------------

if 'ATHENA_PROC_NUMBER' in os.environ:
    evgenLog.info('Noticed that you have run with an athena MP-like whole-node setup.  Will re-configure now to make sure that the remainder of the job runs serially.')
    njobs = os.environ.pop('ATHENA_PROC_NUMBER')
    if not hasattr(opts,'nprocs'): mglog.warning('Did not see option!')
    else: opts.nprocs = 0
    print opts

include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
include("Pythia8_i/Pythia8_MadGraph.py")
genSeq.Pythia8.Commands += ["Main:timesAllowErrors = 60000"]

#relax the cuts on displaced vertices and non G4 particles
testSeq.TestHepMC.MaxTransVtxDisp = 100000000 #in mm
testSeq.TestHepMC.MaxVtxDisp = 100000000 #in mm
testSeq.TestHepMC.MaxNonG4Energy = 100000000 #in MeV

#--------------------------------------------------------------
# Configuration for EvgenJobTransforms
#--------------------------------------------------------------

evgenConfig.description = "Displaced hadronic jets process Higgs > S S with mH={}GeV, mS={}GeV".format(mH, mhS)
evgenConfig.keywords = ["exotic", "BSM", "BSMHiggs", "longLived"]
evgenConfig.contact  = ['simon.berlendis@cern.ch', 'hao.zhou@cern.ch',
                        'Cristiano.Alpigiani@cern.ch', 'hrussell@cern.ch' ]
evgenConfig.process="Higgs --> LLPs"
evgenConfig.inputfilecheck = 'tmp_LHE_events'
runArgs.inputGeneratorFile='tmp_LHE_events.events'
