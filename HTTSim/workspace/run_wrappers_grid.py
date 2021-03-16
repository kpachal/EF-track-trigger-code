#!/usr/bin/python

import os
import subprocess
import glob
import shutil

inDS_list = [
"mc15_14TeV:mc15_14TeV.900245.PG_singmuInvPtFlat5_etaFlat2022_verylarged0.recon.RDO.e8312_s3642_s3643_r12392",
"mc15_14TeV:mc15_14TeV.900239.PG_singmuInvPtFlat5_etaFlat0103_verylarged0.recon.RDO.e8312_s3642_s3643_r12392",
"mc15_14TeV:mc15_14TeV.900243.PG_singmuInvPtFlat5_etaFlat0709_verylarged0.recon.RDO.e8312_s3642_s3643_r12392",
"mc15_14TeV:mc15_14TeV.900242.PG_singmuInvPtFlat5_etaFlat1214_verylarged0.recon.RDO.e8312_s3642_s3643_r12392",
"mc15_14TeV:mc15_14TeV.900244.PG_singmuInvPtFlat5_etaFlat3234_verylarged0.recon.RDO.e8312_s3642_s3643_r12392",
]

for inDS in inDS_list :

    print "Begin dataset",inDS

    tokens = inDS.split(".")
    outname = "user.kpachal.{0}.{1}.htt-wrapper".format(tokens[1],tokens[2])

    transform_command = '''Reco_tf.py --skipEvents 0 --jobNumber 242000 \
    --inputRDOFile    %IN \
    --outputESDFile    %OUT.ESD.pool.root \
    --digiSteeringConf StandardInTimeOnlyTruth \
    --geometryVersion  ATLAS-P2-ITK-22-02-00 \
    --conditionsTag    OFLCOND-MC15c-SDR-14-03 \
    --DataRunNumber    242000 \
    --imf all:'False' \
    --postInclude all:'InDetSLHC_Example/postInclude.SLHC_Setup_ITK.py' RAWtoESD:'InDetSLHC_Example/postInclude.AnalogueClustering.py' \
    --preExec 'all:from AthenaCommon.GlobalFlags import globalflags; globalflags.DataSource.set_Value_and_Lock("geant4");' RAWtoESD:'rec.UserAlgs=["TrigHTTInput/HTTSGToRawHitsWrapperAlg_jobOptions.py"];' \
    --preInclude all:'InDetSLHC_Example/preInclude.SiliconOnly.py,InDetSLHC_Example/preInclude.SLHC_Setup.py,InDetSLHC_Example/preInclude.SLHC_Setup_Strip_GMX.py,InDetSLHC_Example/preInclude.SLHC_Calorimeter_mu0.py' 'default:InDetSLHC_Example/preInclude.SLHC.SiliconOnly.Reco.py,InDetSLHC_Example/SLHC_Setup_Reco_TrackingGeometry_GMX.py'  \
    --postExec all:'ServiceMgr.PixelLorentzAngleSvc.ITkL03D = True' HITtoRDO:'CfgMgr.MessageSvc().setError+=["HepMcParticleLink"];' '''

    # Could try --nEventsPerFile=100000 --nEventsPerJob=100000 
    pathena_command = '''pathena --trf "{0}" --inDS {1} --outDS {2} --extOutFile=httsim_rawhits_wrap.root --nFiles=20'''.format(transform_command,inDS,outname)

    print pathena_command
    print "\n"

    break
# pathena --trf "Reco_tf.py inputAODFile=%IN outputNTUP_SUSYFile=%OUT.NTUP.root skipEvents=%SKIPEVENTS maxEvents=100 ..." --inDS ... --outDS ... --nEventsPerFile=1000 --nEventsPerJob=100 ...




