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

        # Create an individual router for each controller plus one more for
        # the centralized crossbar.  The large numbers of routers are needed
        # because external links do not model outgoing bandwidth in the
        # simple network, but internal links do.
        # For garnet, one router suffices, use CrossbarGarnet.py

        num_dirs = options.num_dirs
        assert(num_dirs == 1)
        num_cpus = options.num_cpus
        num_routers = options.num_l2caches
        num_cpus_per_router, remainder = divmod(num_cpus, num_routers)
        assert(remainder == 0)

        routers = [Router(router_id=i) for i in range(num_routers+1)]
        xbar = routers[num_routers]
        network.routers = routers

        ext_links = []
        link_count = 0

        for i in range(num_cpus):
            l1cache_ctrl = self.nodes[i]
            router_id, _ = divmod(i, num_cpus_per_router)
            ext_links.append(ExtLink(link_id=link_count,
                                     ext_node=l1cache_ctrl,
                                     int_node=routers[router_id],
                                     latency=link_latency))
            link_count += 1
            print("Extlink[%d] node[%d] type[%s] <--> router[%d]" \
                % (link_count - 1, i, l1cache_ctrl.type, router_id))

        for i in range(num_cpus, num_cpus + num_routers):
            l2cache_ctrl = self.nodes[i]
            router_id = i - num_cpus
            ext_links.append(ExtLink(link_id=link_count,
                                     ext_node=l2cache_ctrl,
                                     int_node=routers[router_id],
                                     latency=link_latency))
            link_count += 1
            print("Extlink[%d] node[%d] type[%s] <--> router[%d]" \
                % (link_count - 1, i, l2cache_ctrl.type, router_id))

        dir = self.nodes[num_cpus + num_routers]
        ext_links.append(ExtLink(link_id=link_count,
                                     ext_node=dir,
                                     int_node=xbar,
                                     latency=link_latency))
        link_count += 1
        print("Extlink[%d] node[%d] type[%s] <--> router[%d]" \
            % (link_count - 1, num_cpus + num_routers,
               dir.type, num_routers))

        network.ext_links = ext_links

        int_links = []
        for i in range(num_routers):
            int_links.append(IntLink(link_id=link_count,
                                     src_node=routers[i],
                                     dst_node=xbar,
                                     latency=cxl_link_latency))
            link_count += 1
            print("Intlink[%d] router[%s] --> router[%d]" \
                % (link_count - 1, i, num_routers))

        for i in range(num_routers):
            int_links.append(IntLink(link_id=link_count,
                                     src_node=xbar,
                                     dst_node=routers[i],
                                     latency=cxl_link_latency))
            link_count += 1
            print("Intlink[%d] router[%s] --> router[%d]" \
                % (link_count - 1, num_routers, i))

        network.int_links = int_links