#!/usr/bin/python

import os
import subprocess
import glob
import shutil
from magic.condor_handler import CondorHandler
import itertools

# Do everything but submit if true
isTest = False

# Gridpack mode?
doGridpack = True
# If true, create the gridpack
# If false, run with it
creation = True

# CME:
# Currently 14 TeV, but should also do 100.
CME = 14000

# Batch controls
useBatch = True
# Currently supported: condor, pbs
batch_type = "condor"

# Turn on only what you want for smaller tests
doModels = ["slep"]

# If some jobs failed, regenerate just those.
# If this list is empty, will do everything.
rerun = [#"stau_100_0_0p01ns",
        #"stau_200_0_0p01ns",
        #"stau_300_0_0p01ns",
        #"stau_400_0_0p1ns",
        #"stau_400_0_1ns",
        #"stau_500_0_0p01ns",
        #"stau_500_0_1ns",
        ]

DSID = 100001

# Replace with something importable later
# once we have more models and a real grid.
# Lifetime should be in nanoseconds
grid = {
 "slep" : {
   "documentation" : "https://its.cern.ch/jira/browse/ATLMCPROD-5638",
   "mPar" : [50],
   "mChild" : [0],
   "lifetime" : [0.1],
   "joTemplate" : "mc.MGPy8EG_A14NNPDF23LO_SlepSlep_LLP_{0}_{1}_{2}ns.py",
   "controlFile" : "MadGraphControl_SimplifiedModel_SlepSlep_direct_LLP.py"
 },
 "higgsportal" : {
   "documentation" : "https://its.cern.ch/jira/browse/ATLMCPROD-6900",
   "mPar" : [125],
   "mChild" : [15,60],
   "lifetime" : [0.1,0.5],
   "joTemplate" : "mc.MGPy8EG_A14NNPDF23_NNPDF31ME_HSSLLP_{0}_{1}_{2}ns.py",
   "controlFile" : "MadGraphControl_HSS_mc16.py"
 },
 "rhadron" : {
   "documentation" : "https://its.cern.ch/jira/browse/ATLMCPROD-8791",
   "mPar" : [2000],
   "mChild" : [1950],
   "lifetime" : [1],
   "joTemplate" : "mc.MGPy8EG_A14NNPDF23LO_GG_qqn1_{0}_{1}_rpvLF_{2}ns.py",
   "controlFile" : "MadGraphControl_SimplifiedModel_RPV_LLP_Filtered.py",
 },
 "smuon" :{
   "documentation" : "https://its.cern.ch/jira/browse/ATLMCPROD-5638 plus edits from TrackTrigStudy",
   "mPar" : [50],
   "mChild" : [0],
   "lifetime" : [0.1],
   "joTemplate" : "mc.MGPy8EG_A14NNPDF23LO_SmuSmu_LLP_{0}_{1}_{2}ns.py",
   "controlFile" : "MadGraphControl_SimplifiedModel_SmuSmu_direct_LLP.py",   
 }
}

parameters = {
 "slep" : {
   "rundir" : "/eos/home-k/kpachal/PhaseIITrack/Signals/run_slep",
   "nEvents" : 50,
 },
 "higgsportal" : {
   "rundir" : "/eos/home-k/kpachal/PhaseIITrack/Signals/run_higgsportal",
   "nEvents" : 50,
 },
 "rhadron" : {
   "rundir" : "/eos/user/k/kpachal/PhaseIITrack/Signals/run_rhadron",
  "nEvents" : 50,
 },
 "smuon" : {
   "rundir" : "/eos/user/k/kpachal/PhaseIITrack/Signals/run_smuon",
   "nEvents" : 500
 }
}


# Create batch handler
location_batchscripts = os.getcwd()+"/batch_scripts/"
location_batchlogs = os.getcwd()+"/batch_logs/"
batchmanager = CondorHandler(location_batchlogs, location_batchscripts)
batchmanager.job_length = "tomorrow"

# Make sure dirs exist
for thisdir in [location_batchscripts,location_batchlogs] :
  if not os.path.exists(thisdir) :
    os.mkdir(thisdir)

# Loop over models
random = 1234
for model in doModels :

  # In each, generate grid of points
  # in tuple format. 
  # Leave implementation of this to Jess - I have just one point.
  points = []
  this_grid = grid[model]
  
  points = list(itertools.product(this_grid["mPar"],this_grid["mChild"],this_grid["lifetime"]))

  #points.append((this_grid["mPar"][0],this_grid["mChild"][0],this_grid["lifetime"][0]))

  # Now loop over points to generate. 
  for point in points :

    # For bookkeeping
    tag_string = "{0}_{1}_{2}_{3}ns".format(model,point[0],point[1],point[2])
    tag_string = tag_string.replace(".","p")
    dir_name = parameters[model]["rundir"]+"/"+tag_string
    if doGridpack :
      if creation :
        dir_name += "_gridpack"
      else :
        dir_name += "_gridpack_testing"

    # For rerunning failed points
    if len(rerun) > 0 :
      if tag_string not in rerun :
        continue

    # Make directory to run this and a sub-directory for the job options
    if not os.path.exists(dir_name) :
      os.mkdir(dir_name)
    jo_subdir = dir_name+"/{0}".format(DSID)
    if not os.path.exists(jo_subdir) :
      os.mkdir(jo_subdir)

    # Make the JO file
    jo_name_simple = this_grid["joTemplate"].format(point[0],point[1],"{0}".format(point[2]).replace(".","p"))
    jo_name = jo_subdir+"/"+jo_name_simple
    jo_contents = '''include ('{0}')'''.format(this_grid["controlFile"])
    with open(jo_name,"w") as file :
      file.write(jo_contents)

    # Get ready to run
    random = random+1
    if doGridpack :
      path_command = "JOBOPTSEARCHPATH=/afs/cern.ch/work/k/kpachal/PhaseIITrack/Signals/Generation/ControlFiles_Gridpack/:$JOBOPTSEARCHPATH"
      setup_command = "setupATLAS -c slc6;\n"
      if creation : use_events = 5
      else : use_events = parameters[model]["nEvents"]
      generate_command = "Gen_tf.py --ecmEnergy={0} --firstEvent=1 --jobConfig={1}/{2} --maxEvents={3} --outputEVNTFile=test_evgen.EVNT.root --randomSeed={4}".format(CME,dir_name,DSID,use_events,random)
      if creation :
        generate_command += " --outputFileValidation=False"
      else :
        # Copy gridpack from location it was generated
        gridpack_list = glob.glob(dir_name.replace("_testing","")+"/*.tar.gz")
        if len(gridpack_list) != 1 :
          print "Didn't find gridpack! List was:"
          exit(1)
        gridpack_name = gridpack_list[0]
        shutil.copy(gridpack_name,jo_subdir)
        # Now it should be picked up automatically.

    else :
      path_command = "JOBOPTSEARCHPATH=/afs/cern.ch/work/k/kpachal/PhaseIITrack/Signals/Generation/ControlFiles/:$JOBOPTSEARCHPATH"
      setup_command = ""
      generate_command = "Gen_tf.py --ecmEnergy={0} --firstEvent=1 --jobConfig={1}/{2} --maxEvents={3} --outputEVNTFile=test_evgen.EVNT.root --randomSeed={4}".format(CME,dir_name,DSID,parameters[model]["nEvents"],random)
    
    # Common stuff
    # Add this back in if I have my own Athena mods at some point
    #source_command = "asetup --restore;\nsource ../Filtering/build/x86_64-centos7-gcc62-opt/setup.sh"
    source_command = setup_command+"asetup 21.6.59,AthGeneration"
    run_command = """echo 'starting job.';\ncd {0};\n{1};\n{4};\ncd {2};\n{3}\n""".format(os.getcwd(),path_command,dir_name,generate_command,source_command)

    if isTest :
      print(generate_command)
      continue

    if useBatch :

      # Make batch script
      script_string = tag_string
      if doGridpack :
        if creation :
          script_string += "_gridpack"
        else :
          script_string += "_gridpack_testing"
      batchmanager.send_job(run_command,script_string)

    else :
      local_command = "cd {0};".format(dir_name)+generate_command
      subprocess.call(local_command, shell=True) 
    
    # Uncomment to do just one point
    #break  
