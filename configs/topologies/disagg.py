# Copyright (c) 2010 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Steve Reinhardt

from __future__ import print_function
from __future__ import absolute_import

from m5.params import *
from m5.objects import *

from .BaseTopology import SimpleTopology

class disagg(SimpleTopology):
    description='disagg'

    def makeTopology(self, options, network, IntLink, ExtLink, Router):

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis
        link_latency = options.link_latency # used by simple and garnet
        cxl_link_latency = options.cxl_link_latency
        router_latency = options.router_latency # only used by garnet
        cxl_switch_latency = options.cxl_switch_latency
        core_local_link_latency = 6

        # Create an individual router for each controller plus one more for
        # the centralized crossbar.  The large numbers of routers are needed
        # because external links do not model outgoing bandwidth in the
        # simple network, but internal links do.
        # For garnet, one router suffices, use CrossbarGarnet.py

        num_sockets = options.num_sockets
        num_cpus = options.num_cpus
        num_l2caches = options.num_l2caches
        num_dirs = options.num_dirs
        num_cpus_per_socket, rmdr = divmod(num_cpus, num_sockets)
        assert(rmdr == 0)
        num_l2s_per_socket, rmdr = divmod(num_l2caches, num_sockets)
        assert(rmdr == 0)
        num_dirs_per_socket, rmdr = divmod(num_dirs, num_sockets)
        assert(rmdr == 0)
        num_cpus_per_dir, rmdr = divmod(num_cpus, num_dirs)
        assert(rmdr == 0)
        num_l2s_per_dir, rmdr = divmod(num_l2caches, num_dirs)
        assert(rmdr == 0)
        # num_cpus_per_l2cache, rmdr = divmod(num_cpus, num_l2caches)
        # assert(rmdr == 0)

        l1_ctrls = self.nodes[0:num_cpus]
        l2_ctrls = self.nodes[num_cpus:num_cpus+num_l2caches]
        dir_ctrls = self.nodes[num_cpus+num_l2caches:]

        router_count = 0
        socket_root_routers = []
        intra_socket_routers = []
        link_count = 0
        ext_links = []
        int_links = []

        for i in range(num_sockets):

            # create socket root router
            socket_root_router = Router(router_id=router_count,
                                        latency=router_latency)
            router_count += 1
            socket_root_routers.append(socket_root_router)

            # create a router for each dir
            dir_routers = [Router(router_id=router_count+j,
                                  latency=router_latency) \
                                for j in range(num_dirs_per_socket)]
            router_count += num_dirs_per_socket
            intra_socket_routers += dir_routers

            # connect l1 to corresponding dir router
            for j, l1_ctrl in enumerate(l1_ctrls[i * num_cpus_per_socket:\
                (i + 1) * num_cpus_per_socket]):
                dir_router = dir_routers[j // num_cpus_per_dir]
                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node=l1_ctrl,
                                        int_node=dir_router,
                                        latency=core_local_link_latency))
                link_count += 1
                print("Extlink[%d] node[%d] type[%s] <--> router[%d]" \
                % (link_count - 1, j, l1_ctrl.type, j // num_cpus_per_dir))

            # connect l2 to corresponding dir router
            for j, l2_ctrl in enumerate(l2_ctrls[i * num_l2s_per_socket:\
                (i + 1) * num_l2s_per_socket]):
                dir_router = dir_routers[j // num_l2s_per_dir]
                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node=l2_ctrl,
                                        int_node=dir_router,
                                        latency=core_local_link_latency))
                link_count += 1
                print("Extlink[%d] node[%d] type[%s] <--> router[%d]" \
                % (link_count - 1, j, l2_ctrl.type, j // num_l2s_per_dir))

            # connect dir to corresponding dir router
            for j, dir_ctrl in enumerate(dir_ctrls[i * num_dirs_per_socket:\
                (i + 1) * num_dirs_per_socket]):
                dir_router = dir_routers[j]
                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node=dir_ctrl,
                                        int_node=dir_router,
                                        latency=core_local_link_latency))
                link_count += 1
                print("Extlink[%d] node[%d] type[%s] <--> router[%d]" \
                % (link_count - 1, j, dir_ctrl.type, j))

            # connect dir routers to the socket root router
            # todo: make it a mesh
            for dir_router in dir_routers:
                int_links.append(IntLink(link_id=link_count,
                                     src_node=dir_router,
                                     dst_node=socket_root_router,
                                     latency=link_latency))
                link_count += 1
                int_links.append(IntLink(link_id=link_count,
                                     src_node=socket_root_router,
                                     dst_node=dir_router,
                                     latency=link_latency))
                link_count += 1

        # add CXL switch
        CXL_switch = Router(router_id=router_count,
                            latency=cxl_switch_latency)
        router_count += 1

        # connect socket root routers to CXL switch
        for socket_root_router in socket_root_routers:
            int_links.append(IntLink(link_id=link_count,
                                     src_node=socket_root_router,
                                     dst_node=CXL_switch,
                                     latency=cxl_link_latency))
            link_count += 1
            int_links.append(IntLink(link_id=link_count,
                                    src_node=CXL_switch,
                                    dst_node=socket_root_router,
                                    latency=cxl_link_latency))
            link_count += 1

        network.ext_links = ext_links
        network.routers += socket_root_routers
        network.routers += intra_socket_routers
        network.routers.append(CXL_switch)
        network.int_links = int_links