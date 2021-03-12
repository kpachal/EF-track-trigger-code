include ( 'MadGraphControl/SUSY_SimplifiedModel_PreInclude.py' ) 

def StringToFloat(s):
  ss=s.replace("ns","")
  if "p" in ss:
    return float(ss.replace("p", "."))
  return float(ss)

# Set up to save HepMC
import AthenaCommon.AlgSequence as acas
topAlg = acas.AlgSequence()
from TruthIO.TruthIOConf import WriteHepMC
topAlg += WriteHepMC()

# Extract job settings/masses etc.
from MadGraphControl.MadGraphUtilsHelpers import get_physics_short
phys_short = get_physics_short()
mslep      = StringToFloat(phys_short.split('_')[4]) 
lifetime = str(phys_short.split('_')[6].split('.py')[0])
lifetime        = StringToFloat(lifetime)
print "LIFETIME  ",lifetime
mn1        = StringToFloat(phys_short.split('_')[5])

# Masses of sleptons:
masses['1000011'] = mslep
masses['1000013'] = mslep
masses['1000015'] = mslep
masses['2000011'] = mslep
masses['2000013'] = mslep
masses['2000015'] = mslep

# Have to add gravitino since we're decaying to it
masses['1000039'] = 0.0000001

# Decay widths and
# branching ratios of sleptons:
# depend on the particular one.

# Width = hbar/tau
hbar = 6.582119514e-16 # GeV * ns
# So this should already give us the correct
# units (GeV) for width when we divide by lifetime.
decayWidth = hbar/float(lifetime)
slepton_widthstring = '''DECAY   {0}    {1}'''
branchingRatioMu = '''

#          BR          NDA       ID1       ID2       ID3
         1.0000         2      1000039      13        
'''
branchingRatioE = '''

#          BR          NDA       ID1       ID2       ID3
         1.0000         2      1000039      11
'''
branchingRatioTau = '''

#          BR          NDA       ID1       ID2       ID3
         1.0000         2      1000039      15   
'''
decays['1000011'] = slepton_widthstring.format('1000011',decayWidth)+branchingRatioE
decays['1000013'] = slepton_widthstring.format('1000013',decayWidth)+branchingRatioMu
decays['1000015'] = slepton_widthstring.format('1000015',decayWidth)+branchingRatioTau
decays['2000011'] = slepton_widthstring.format('2000011',decayWidth)+branchingRatioE
decays['2000013'] = slepton_widthstring.format('2000013',decayWidth)+branchingRatioMu
decays['2000015'] = slepton_widthstring.format('2000015',decayWidth)+branchingRatioTau

# For light sleptons
#process = '''
#define slepton = el- el+ er- er+ mul- mul+ mur- mur+
#define lepton = e+ e- mu+ mu-
#generate p p > slepton slepton $ susystrong @1
#add process p p > slepton slepton j $ susystrong @2
#add process p p > slepton slepton j j $ susystrong @3
#'''

# Smuons only
process = '''
generate p p > mul- mul+ $ susystrong @1
add process p p > mur- mur+ $ susystrong @1
add process p p > mul- mul+ j $ susystrong @2
add process p p > mur- mur+ j $ susystrong @2
add process p p > mul- mul+ j j $ susystrong @3
add process p p > mur- mur+ j j $ susystrong @3
'''

njets = 2
evgenLog.info('Registered generation of slepton-pair production via direct decays; mass point ' + str(mslep) + ' with lifetime ' + str(lifetime))

evgenConfig.contact = [ "emma.sian.kuwertz@cern.ch" ]
evgenConfig.keywords += ['SUSY','slepton','longLived','gravitino','simplifiedModel']
evgenConfig.description = 'Direct slepton-pair production in simplified model with non-prompt decays, m_sleptonLR = %s GeV, lifetime = %s'%(mslep,lifetime)

if lifetime != 0:
  evgenConfig.specialConfig = 'GMSBSlepton=%s*GeV;GMSBGravitino=%s*GeV;GMSBSleptonTime=%s*ns;preInclude=SimulationJobOptions/preInclude.SleptonsLLP.py' % (mslep,0.0000001,lifetime)

# Filter and event multiplier 
evt_multiplier = 3 

# Setting for requesting that LHE files contain lifetimes
add_lifetimes_lhe = False

include ( 'MadGraphControl/SUSY_SimplifiedModel_PostInclude.py' )

if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = guess"]
    if "UserHooks" in genSeq.Pythia8.__slots__.keys(): 
      genSeq.Pythia8.UserHooks += ['JetMergingaMCatNLO'] 
    else: 
      genSeq.Pythia8.UserHook = 'JetMergingaMCatNLO'

bonus_file = open('pdg_extras.dat','w')
bonus_file.write( '1000011 SelectronL %s (MeV/c) fermion Selectron -1\n'%(str(mslep)))
bonus_file.write( '2000011 SelectronR %s (MeV/c) fermion Selectron -1\n'%(str(mslep)))
bonus_file.write( '1000013 SmuonL %s (MeV/c) fermion Smuon -1\n'%(str(mslep)))
bonus_file.write( '2000013 SmuonR %s (MeV/c) fermion Smuon -1\n'%(str(mslep)))
bonus_file.write( '-1000011 Anti-selectronL %s (MeV/c) fermion Selectron 1\n'%(str(mslep)))
bonus_file.write( '-2000011 Anti-selectronR %s (MeV/c) fermion Selectron 1\n'%(str(mslep)))
bonus_file.write( '-1000013 Anti-smuonL %s (MeV/c) fermion Smuon 1\n'%(str(mslep)))
bonus_file.write( '-2000013 Anti-smuonR %s (MeV/c) fermion Smuon 1\n'%(str(mslep)))
bonus_file.write( '1000015 Stau1 %s (MeV/c) fermion Stau -1\n'%(str(mslep)))
bonus_file.write( '2000015 Stau2 %s (MeV/c) fermion Stau -1\n'%(str(mslep)))
bonus_file.write( '-1000015 Anti-stau1 %s (MeV/c) fermion Stau 1\n'%(str(mslep)))
bonus_file.write( '-2000015 Anti-stau2 %s (MeV/c) fermion Stau 1\n'%(str(mslep)))
bonus_file.close()

#relax the cuts on displaced vertices and non G4 particles
testSeq.TestHepMC.MaxTransVtxDisp = 100000000 #in mm
testSeq.TestHepMC.MaxVtxDisp = 100000000 #in mm
testSeq.TestHepMC.MaxNonG4Energy = 100000000 #in MeV
# and whitelist our particles.
testSeq.TestHepMC.G4ExtraWhiteFile='pdg_extras.dat'

import os
os.system("get_files %s" % testSeq.TestHepMC.G4ExtraWhiteFile)
