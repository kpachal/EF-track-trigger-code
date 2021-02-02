include ( 'MadGraphControl/SUSY_SimplifiedModel_PreInclude.py' ) 

#############################################
### Production of GMSB sleptons
### decaying to displaced e/mu/tau + gravitino.
### Kate obtained job options from here:
### https://its.cern.ch/jira/browse/ATLMCPROD-5638
### Sleptons created in generation process and
### decay to form displaced lepton signals in sim step.
############################################

def StringToFloat(s):
  ss=s.replace("ns","")
  if "p" in ss:
    return float(ss.replace("p", "."))
  return float(ss)

# Extract job settings/masses etc.
from MadGraphControl.MadGraphUtilsHelpers import get_physics_short
phys_short = get_physics_short()
mslep      = StringToFloat(phys_short.split('_')[4]) 
lifetime = str(phys_short.split('_')[6].split('.py')[0])
lifetime        = StringToFloat(lifetime)
print "LIFETIME  ",lifetime
mn1        = StringToFloat(phys_short.split('_')[5])

masses['1000011'] = mslep
masses['1000013'] = mslep
masses['1000015'] = mslep
masses['2000011'] = mslep
masses['2000013'] = mslep
masses['2000015'] = mslep

# Have to add gravitino since we're decaying to it
masses['1000039'] = 0.0000001

# slepton pairs + up to 2 extra partons
process = '''
generate p p > el- el+ $ susystrong @1
add process p p > er- er+ $ susystrong @1
add process p p > mul- mul+ $ susystrong @1
add process p p > mur- mur+ $ susystrong @1
add process p p > ta1- ta1+ $ susystrong @1
add process p p > ta2- ta2+ $ susystrong @1
add process p p > el- el+ j $ susystrong @2
add process p p > er- er+ j $ susystrong @2
add process p p > mul- mul+ j $ susystrong @2
add process p p > mur- mur+ j $ susystrong @2
add process p p > ta1- ta1+ j $ susystrong @2
add process p p > ta2- ta2+ j $ susystrong @2
add process p p > el- el+ j j $ susystrong @3
add process p p > er- er+ j j $ susystrong @3
add process p p > mul- mul+ j j $ susystrong @3
add process p p > mur- mur+ j j $ susystrong @3
add process p p > ta1- ta1+ j j $ susystrong @3
add process p p > ta2- ta2+ j j $ susystrong @3
'''
njets = 2
evgenLog.info('Registered generation of slepton and stau pair production via direct decays; mass point ' + str(mslep) + ' with lifetime ' + str(lifetime))

evgenConfig.contact = [ "katherine.pachal@cern.ch" ]
evgenConfig.keywords += ['SUSY','slepton','longLived','gravitino','simplifiedModel']
evgenConfig.description = 'Direct slepton/stau-pair production in simplified model with non-prompt decays, m_sleptonLR = %s GeV, lifetime = %s'%(mslep,lifetime)

if lifetime != 0:
  evgenConfig.specialConfig = 'GMSBSlepton=%s*GeV;GMSBGravitino=%s*GeV;GMSBSleptonTime=%s*ns;preInclude=SimulationJobOptions/preInclude.SleptonsLLP.py' % (mslep,0.0000001,lifetime)

# Filter and event multiplier 
evt_multiplier = 10
include ( 'GeneratorFilters/HTT_BSMFilter.py' )

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

testSeq.TestHepMC.G4ExtraWhiteFile='pdg_extras.dat'

import os
os.system("get_files %s" % testSeq.TestHepMC.G4ExtraWhiteFile)
