#!/usr/bin/python

import os
import subprocess
import glob
import shutil

inDS_list = [
"mc15_14TeV:mc15_14TeV.900245.PG_singmuInvPtFlat5_etaFlat2022_verylarged0.recon.RDO.e8312_s3642_s3643_r12392"
"mc15_14TeV:mc15_14TeV.900239.PG_singmuInvPtFlat5_etaFlat0103_verylarged0.recon.RDO.e8312_s3642_s3643_r12392"
"mc15_14TeV:mc15_14TeV.900243.PG_singmuInvPtFlat5_etaFlat0709_verylarged0.recon.RDO.e8312_s3642_s3643_r12392"
"mc15_14TeV:mc15_14TeV.900242.PG_singmuInvPtFlat5_etaFlat1214_verylarged0.recon.RDO.e8312_s3642_s3643_r12392",
"mc15_14TeV:mc15_14TeV.900244.PG_singmuInvPtFlat5_etaFlat3234_verylarged0.recon.RDO.e8312_s3642_s3643_r12392"
]

for inDS in inDS_list :

    
# pathena --trf "Reco_tf.py inputAODFile=%IN outputNTUP_SUSYFile=%OUT.NTUP.root skipEvents=%SKIPEVENTS maxEvents=100 ..." --inDS ... --outDS ... --nEventsPerFile=1000 --nEventsPerJob=100 ...




