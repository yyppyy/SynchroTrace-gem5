coh_proto_path=/home/yanpeng/GCP_gem5/SynchroTrace-gem5/src/mem/protocol
synchrotrace_path=/home/yanpeng/GCP_gem5/SynchroTrace-gem5/src/cpu/testers/synchrotrace


cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-GCP.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm
cp ${synchrotrace_path}/synchro_trace-GCP.cc ${synchrotrace_path}/synchro_trace.cc
cp ${synchrotrace_path}/synchro_trace-GCP.hh ${synchrotrace_path}/synchro_trace.hh
mkdir -p build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100


cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-wo-o-opt.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm
cp ${synchrotrace_path}/synchro_trace-GCP.cc ${synchrotrace_path}/synchro_trace.cc
cp ${synchrotrace_path}/synchro_trace-GCP.hh ${synchrotrace_path}/synchro_trace.hh
mkdir -p WO_O_OPT/build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons WO_O_OPT/build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100


cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-GCP.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm
cp ${synchrotrace_path}/synchro_trace-wo-combined-data-opt.cc ${synchrotrace_path}/synchro_trace.cc
cp ${synchrotrace_path}/synchro_trace-wo-combined-data-opt.hh ${synchrotrace_path}/synchro_trace.hh
mkdir -p WO_COMBINED_DATA_OPT/build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons WO_COMBINED_DATA_OPT/build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100


cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-wo-locality-opt.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm
cp ${synchrotrace_path}/synchro_trace-wo-locality-opt.cc ${synchrotrace_path}/synchro_trace.cc
cp ${synchrotrace_path}/synchro_trace-wo-locality-opt.hh ${synchrotrace_path}/synchro_trace.hh
mkdir -p WO_LOCALITY_OPT/build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons WO_LOCALITY_OPT/build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100