from os import listdir
from os.path import isfile, join
import subprocess
import yaml
import argparse
import shlex
import os

running_procs = []
MAX_PROCS = 75
total_procs = 0

root_path = '/home/yanpeng/GCP_gem5/prism/GCP_scripts/result/'

workloads = {
    'kvs' : ['run_workloada.dat', 'run_workloadb.dat', 'run_workloadc.dat'],
    # 'kc': ['run_workloadl.dat', 'run_workloadh.dat'],
}
# workloads = {
#     'kvs' : ['run_workloada.dat', ],
# }

# workloads = {
#     'kvs' : ['run_workloadb.dat', 'run_workloadc.dat'],
# }

num_threads_per_nodess = [8, ]
# num_threads_per_nodess = [8, ]

# num_nodess = [16, ]
num_nodess = [16, 8, 4, 2, 1]
# num_nodess = [1, ]
# num_nodess = [16, 8]

lock_types = ['pthread_rwlock_prefer_w',
              'percpu',
              'cohort_rw_spin_mutex',
              'mcs',
            #   'pthread_mutex'
              ]
# lock_types = ['pthread_mutex', ]
# lock_types = ['pthread_rwlock_prefer_w', ]
# lock_types = ['mcs', ]
# lock_types = ['percpu', ]
# lock_types = ['cohort_rw_spin_mutex', ]

if __name__ == "__main__":
    for app in workloads:
        for workload in workloads[app]:
            for lock_type in lock_types:
                for num_nodes in num_nodess:
                    for num_threads_per_nodes in num_threads_per_nodess:

                        num_threads_tot = num_nodes * num_threads_per_nodes
                        config_path = root_path + '_'.join((app, workload,
                                        lock_type,
                                        str(num_nodes),
                                        str(num_threads_per_nodes))) + '/'
                        event_path = config_path
                        output_path = config_path + 'output/'

                        os.system('mkdir -p %s' % output_path)

                        cmd = 'build/ARM/gem5.opt --outdir=%s \
                            --debug-flags=STIntervalPrint \
                                configs/example/synchrotrace_ruby.py' \
                                    % output_path

                        option_list = []
                        option_list.append('--ruby')
                        option_list.append('--network=garnet2.0')
                        option_list.append('--topology=disagg')
                        option_list.append('--event-dir=' \
                            + event_path)
                        option_list.append('--output-dir=' \
                            + output_path)
                        option_list.append('--num-cpus=' \
                            + str(num_threads_tot))
                        option_list.append('--num-threads=' \
                            + str(num_threads_tot))
                        option_list.append('--num-dirs=' \
                            + str(num_threads_tot))
                        option_list.append('--num-l2caches=' \
                            + str(num_threads_tot))
                        option_list.append('--num-sockets=' \
                            + str(num_nodes))
                        option_list.append('--l1d_size=64kB')
                        option_list.append('--l1d_assoc=2')
                        option_list.append('--l1i_size=64kB')
                        option_list.append('--l1i_assoc=2')
                        option_list.append('--l2_size=4096kB')
                        option_list.append('--l2_assoc=8')
                        option_list.append('--cpi-iops=1')
                        option_list.append('--cpi-flops=1')
                        option_list.append('--bandwidth-factor=8')
                        option_list.append('--vcs-per-vnet=8')
                        option_list.append('--monitor-freq=100')
                        option_list.append('--cacheline_size=64')
                        option_list.append('--link-latency=20')
                        option_list.append('--cxl-link-latency=60')
                        option_list.append('--cxl-switch-latency=60')
                        option_list.append('--profile-dir=' \
                            + str(output_path))
                        # option_list.append('--garnet-network=flexible')

                        options = ' '.join(option_list)

                        cmd += ' '
                        cmd += options

                        print(cmd)
                        cmds = shlex.split(cmd)

                        running_procs.append(subprocess.Popen(cmds))
                        while (len(running_procs) == MAX_PROCS):
                            for i,p in enumerate(running_procs):
                                try:
                                    p.wait(timeout=1)
                                    running_procs.pop(i)
                                    total_procs += 1
                                    print("finished: %d" % (total_procs))
                                    break
                                except subprocess.TimeoutExpired:
                                    pass