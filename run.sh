NUM_NODES=4
NUM_THREADS=8
NUM_THREADS_TOT=$((NUM_NODES * NUM_THREADS))
EVENT_PATH=/home/yanpeng/GCP_gem5/prism/GCP_scripts/result/kvs_run_workloada.dat_pthread_rwlock_prefer_w_${NUM_NODES}_${NUM_THREADS}/
OUTPUT_PATH=/home/yanpeng/GCP_gem5/prism/GCP_scripts/result/kvs_run_workloada.dat_pthread_rwlock_prefer_w_${NUM_NODES}_${NUM_THREADS}/
PROFILE_DIR=results/kvs_run_workloada.dat_pthread_rwlock_prefer_w_${NUM_NODES}_${NUM_THREADS}/
ARC=ARM

mkdir -p ${PROFILE_DIR}

build/${ARC}/gem5.opt                                                                          \
  --debug-flags=STIntervalPrint                                                               \
  configs/example/synchrotrace_ruby.py                                                      \
    --ruby                                                                                    \
    --network=garnet2.0                                                                       \
    --topology=disagg                                                                        \
    --event-dir=$EVENT_PATH                                                                   \
    --output-dir=$OUTPUT_PATH                                                                 \
    --num-cpus=${NUM_THREADS_TOT} --num-threads=${NUM_THREADS_TOT} --num-dirs=${NUM_THREADS_TOT} --num-l2caches=${NUM_THREADS_TOT} --num-sockets=${NUM_NODES}                               \
    --l1d_size=64kB --l1d_assoc=2 --l1i_size=64kB --l1i_assoc=2 --l2_size=4096kB --l2_assoc=8 \
    --cpi-iops=1 --cpi-flops=1                                                                \
    --bandwidth-factor=4 --monitor-freq=100 --cacheline_size=64                               \
    --cxl-link-latency=200                                                                      \
    --profile-dir=${PROFILE_DIR}