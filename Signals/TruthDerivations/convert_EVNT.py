#!/usr/bin/python

import os
import glob
import subprocess
from magic.condor_handler import CondorHandler

# Do everything but submit if true
isTest = False

# Batch controls
useBatch = True

# Will submit those matching this tag
# If blank, will submit everything from source dir
tag = "" #"higgsportal"

# Getting EVNT files
source_dir = "/eos/user/k/kpachal/PhaseIITrack/Signals/small_nevts"
out_dir_parent = "/eos/user/k/kpachal/PhaseIITrack/TruthDerivations/"
find_format = source_dir+"/run_*{0}*/{0}*/*.EVNT.root".format(tag)
print "Searching for files matching",find_format,"..."
evnt_files = glob.glob(find_format)
print "Got files:",evnt_files

# Create batch handler
location_batchscripts = os.getcwd()+"/batch_scripts/"
location_batchlogs = os.getcwd()+"/batch_logs/"
batchmanager = CondorHandler(location_batchlogs, location_batchscripts)

# Make sure they exist
for thisdir in [location_batchscripts,location_batchlogs] :
  if not os.path.exists(thisdir) :
    os.mkdir(thisdir)

# Want to run a derivation job for each of the 
# existing points, and give output TRUTH files meaningful names
for evnt_file in evnt_files :

  name_string = evnt_file.split("/")[-2]
  print name_string

  # Want an output dir for this
  out_dir = out_dir_parent + "/"+name_string
  if not os.path.exists(out_dir) :
    os.mkdir(out_dir)

  out_file = "{0}.pool.root".format(name_string)

  reco_command = "Reco_tf.py --inputEVNTFile {0} --outputDAODFile {1} --reductionConf TRUTH1".format(evnt_file,out_file)
  run_command = """echo 'starting job.';\ncd {0};\nasetup --restore;\ncd {1};\n{2}\n""".format(os.getcwd(),out_dir,reco_command)

  if isTest :
    print reco_command
    continue

  if useBatch :

    # Make and send
    batchmanager.send_job(run_command,name_string)

  else :
    subprocess.call(reco_command, shell=True) 

  # Uncomment to do just one point
  #break 

