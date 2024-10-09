# scons build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100
coh_proto_path=/home/yanpeng/GCP_gem5/SynchroTrace-gem5/src/mem/protocol

# Copy the GCP version of the protocol
cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-GCP.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm

# Build with the GCP protocol
mkdir -p build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100

# Copy the QOSB version of the protocol
cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-QOSB.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm

# Build with the QOSB protocol
mkdir -p QOSB/build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons QOSB/build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100
