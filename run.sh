NUM_NODES=16
NUM_THREADS=8
EVENT_PATH=/home/yanpeng/GCP_gem5/prism/GCP_scripts/result/kvs_run_workloada.dat_pthread_rwlock_prefer_w_${NUM_NODES}_${NUM_THREADS}/
OUTPUT_PATH=/home/yanpeng/GCP_gem5/prism/GCP_scripts/result/kvs_run_workloada.dat_pthread_rwlock_prefer_w_${NUM_NODES}_${NUM_THREADS}/
ARC=ARM

build/${ARC}/gem5.opt                                                                          \
  --debug-flags=STIntervalPrint                                                               \
  configs/example/synchrotrace_ruby.py                                                      \
    --ruby                                                                                    \
    --network=garnet2.0                                                                       \
    --topology=disagg                                                                        \
    --event-dir=$EVENT_PATH                                                                   \
    --output-dir=$OUTPUT_PATH                                                                 \
    --num-cpus=128 --num-threads=128 --num-dirs=128 --num-l2caches=128                                \
    --l1d_size=64kB --l1d_assoc=2 --l1i_size=64kB --l1i_assoc=2 --l2_size=4096kB --l2_assoc=8 \
    --cpi-iops=1 --cpi-flops=1                                                                \
    --bandwidth-factor=4 --monitor-freq=100 --cacheline_size=64                               \
    --cxl-link-latency=3