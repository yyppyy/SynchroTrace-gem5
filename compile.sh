# Copy the GCP version of the protocol
cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-GCP.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm
# cp ${coh_proto_path}/MOESI_CMP_directory-L2cache-GCP.sm ${coh_proto_path}/MOESI_CMP_directory-L2cache.sm
# cp ${coh_proto_path}/MOESI_CMP_directory-dir-GCP.sm ${coh_proto_path}/MOESI_CMP_directory-dir.sm
# Build with the GCP protocol
mkdir -p build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100

# Copy the QOSB version of the protocol
cp ${coh_proto_path}/MOESI_CMP_directory-L1cache-QOSB.sm ${coh_proto_path}/MOESI_CMP_directory-L1cache.sm
# cp ${coh_proto_path}/MOESI_CMP_directory-L2cache-QOSB.sm ${coh_proto_path}/MOESI_CMP_directory-L2cache.sm
# cp ${coh_proto_path}/MOESI_CMP_directory-dir-QOSB.sm ${coh_proto_path}/MOESI_CMP_directory-dir.sm
# Build with the QOSB protocol
mkdir -p QOSB/build/ARM
~/python2.7/bin/python2 /home/yanpeng/.local/bin/scons QOSB/build/ARM/gem5.opt PROTOCOL=MOESI_CMP_directory -j100