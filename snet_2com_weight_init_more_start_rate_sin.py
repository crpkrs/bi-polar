# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 12:44:39 2018

Generate social networks with no node attributes
             G.edges[i,j]
             net_size: total number of users
             comm_size: number of members in community 0
             fw_size: average number of followers
             alpha: ratio of followers in community 0 per comm-0 member.
             If alpha>=1, the network is not rewired such that the community has density alpha.
             beta: ratio of followers in community 1 per comm-1 member
             
             2019.11.1 removal of calculating alpha and beta in the simulation execution
             2019.11.1 static network
             2020.6.4  beta is used for communities >=1.

@author: oida
"""

import time
import networkx as nx
import numpy as np
# import matplotlib.pyplot as plt
import numpy.random as rd


class Snet(nx.DiGraph):
    """
    dcnt: discount function as a number of received retweets
    dcnt=0: non-descreasing
    dcnt=1: exponential
    dcnt=2: multiplicative
    dcnt=3: linear
    dcnt=4: simple contagion (first exposure only)
    """
    def __init__(self,
                 net_size=20,
                 comm_size=10,
                 fw_size=5,
                 alpha=0.1,
                 dcnt=0,
                 p=0.0,
                 q=0.0,
                 seed=1,
                 G=nx.DiGraph(),
################ 2020 6/4 2communities
                 beta=0.2,
                 comm_num=1,
################ 2020 6/21 more
                 more=0,
################ 2020 6/25 comm_strt
                 comm_strt=0
                 ):
        super(Snet, self).__init__()
        self.net_size = net_size
        self.comm_size = comm_size
        self.fw_size = fw_size
        self.alpha = alpha
################ 2020 6/4 2communities
        self.beta = beta
        self.comm_num = comm_num
################ 2020 6/21 more
        self.more = more
################ 2020 6/25 comm_strt
        self.comm_strt = comm_strt
        self.seed = seed
        self.p = p
        self.q = q
        self.G = G
        self.maxrecv = 1000

        if dcnt == 0:
            self.dcnt_fun = [1 for i in range(1, self.maxrecv)]
        elif dcnt == 1:
            self.dcnt_fun = [0.9 ** (i - 1) for i in range(1, self.maxrecv)]
        elif dcnt == 2:
            self.dcnt_fun = [1.0 / i for i in range(1, self.maxrecv)]
        elif dcnt == 3:
            self.dcnt_fun = [max(1.0 - 0.5 * (i-1), 0) for i in range(1, self.maxrecv)]
        elif dcnt == 4:
            self.dcnt_fun = [max(2.0 - 1.0 * i, 0) for i in range(1, self.maxrecv)]
        else:
            self.dcnt_fun = [1 - 0.5 * 0.1 ** (i-1) for i in range(1, self.maxrecv)]
            # for i in range(10):
            #     print(self.dcnt_fun[i])

    def _gen_snet(self):
        rd.seed(seed=self.seed)
        th = self.fw_size / (self.net_size - 1)
        th1 = self.alpha * self.fw_size / (self.comm_size - 1)
        th2 = (1 - self.alpha) * self.fw_size / (self.net_size - self.comm_size)

        # for i in range(self.net_size): self.add_node(i)
        self.add_nodes_from(range(self.net_size))
        # self.add_edges_from(rd.randint(self.net_size,
        #                                       size=(self.net_size * self.net_size, 2)))
        for i in range(self.net_size):
            for j in range(self.net_size):
                rn = rd.rand()
                if i != j:
                    if i < self.comm_size:
                        if j < self.comm_size:
                            if rn <= th1: self.add_edge(i, j)
                        else:
                            if rn <= th2: self.add_edge(i, j)
                    else:
                        if rn <= th: self.add_edge(i, j)

    def _random_snet(self, netprop):
        """
        Generate small word, powerlaw networks
        with initiator's followers includes communities having ratio self.alpha and self.beta.

        node_states[0]:   whether the node has alread retweeted (True) or not (False).
        node_states[1]:   How many times a node received retweets before it retweeted.
 ################ 2020 6/27 rate
        node_states[2]:   (old: whether the node is a community member (True) or not.)
        node_states[2]:   whether the node belong to community i (i=1000 indicates non-community mem).
################ 2020 6/4 2communities
        node_states[3]:   How many times a node received retweets after it retweeted.
        """
        
        if netprop == 0:
            G1 = nx.fast_gnp_random_graph(n=self.net_size, p=self.fw_size / (self.net_size - 1), seed=self.seed,
                                          directed=True)
        # print("fast_gnp_random_graph(n=net_size, p=fw_size / (net_size - 1), seed=seed, directed=True)")
        elif netprop == 1:
            H = nx.connected_watts_strogatz_graph(n=self.net_size, k=self.fw_size, p=self.p, seed=self.seed)
            G1 = H.to_directed()
            # G1 = nx.newman_watts_strogatz_graph(n=self.net_size, k=self.fw_size, p=0.1, seed=self.seed)

        # print("newman_watts_strogatz_graph(n=net_size, k=6, p=100 * fw_size / (net_size - 1), seed=seed)")
        elif netprop == 2:
            # G1 = nx.barabasi_albert_graph(n=self.net_size, m=self.net_size - 1, seed=self.seed)
        # print("barabasi_albert_graph(n=net_size, m=net_size - 1, seed=seed)")
        # G1 = nx.powerlaw_cluster_graph(n=net_size, m=net_size - 1, p=50 * fw_size / (net_size - 1), seed=seed)
        # print("powerlaw_cluster_graph(n=net_size, m=net_size - 1, p=50 * fw_size / (net_size - 1), seed=seed)")
            H = nx.extended_barabasi_albert_graph(n=self.net_size, m=8, p=self.p, q=self.q, seed=self.seed)
            G1 = H.to_directed()
        else:
        # pokec
            G1 = self.G

################ 2020 6/27 rate
        self.node_states = [[False, 0, 1000, 0] for _ in range(self.net_size)]
################ 2020 6/4 2communities
        self.prop = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]
        
        self.add_nodes_from(range(self.net_size))
        self.add_edges_from(G1.edges)
        if self.comm_num * self.comm_size * 2 > self.net_size:
            print("Error: community overlap")
        for comm_id in range(self.comm_num):
#            print("################ alpha, beta, comm_id=", self.alpha, self.beta, comm_id)
            addb, rmvb, in_follower, out_follower = self._create_comm(comm_id)
#            print("comm_id=", comm_id, len(addb), len(rmvb))
            if comm_id == 0:
                self.prop[0][5] = in_follower / (in_follower + out_follower)
            else:
                self.prop[0][9]  = min(self.prop[0][9],  in_follower / (in_follower + out_follower))
                self.prop[0][10] = max(self.prop[0][10], in_follower / (in_follower + out_follower))
            self.remove_edges_from(rmvb)
            self.add_edges_from(addb)
                
#            print(self.edges())
#         print("edges:", self.size(), "replacements:", len(rmvb))
################ 2020 6/4 2communities

################ 2020 6/4 2communities

    def _create_comm(self, comm_id):
        """
        Make a community in a network
        The first community corresponds to index alpha
        The other communities correspond to index beta
        """

        rd.seed(seed=self.seed)
        in_follower = 0
        out_follower = 0
        addb = []
        rmvb = []
        maxrep = 1000
################ 2020 6/4 2communities
        if comm_id == 0: 
            index = self.alpha
        else:
            index = self.beta
#        strt = comm_id * self.comm_size
################ 2020 6/25 comm_strt
        strt = comm_id * self.comm_size * 2 + self.comm_size * self.comm_strt
################ 2020 6/22        
        if strt >= self.net_size:
            strt = self.comm_size + strt % self.net_size
        for i in range(self.comm_size):
################ 2020 6/4 2communities
            mapp = i + strt
################ 2020 6/27 rate
            self.node_states[mapp][2] = comm_id
#            print("before ==============", self.out_edges(mapp))
            succ = []
            for k in self.successors(mapp): succ += [k]
#            print("mapp, succ", mapp, succ)
            if index < 1:
                follower_in = round(index * len(succ))
                follower_out = len(succ) - follower_in
            else:
                follower_in = len(succ)
                follower_out = len(succ)
#            print("mapp=", mapp, "len=", len(succ), "in=", follower_in, "out=", follower_out)
            succ_in_cnt = 0
            succ_out_cnt = 0
            nsucc = succ[:]
#                print("nsucc", nsucc)
            for k in succ:
                # if k < self.comm_size:
#                if  comm_id * self.comm_size <= k and k < (comm_id + 1) * self.comm_size:
                if  strt <= k and k < strt + self.comm_size:
                    succ_in_cnt += 1
                    if succ_in_cnt > follower_in:
                        id = k
                        repe = 0
                        while (id in nsucc and repe < maxrep):
                            repe += 1
                            rnum = rd.randint(self.comm_size, self.net_size)
#                            id = (rnum + comm_id * self.comm_size) % self.net_size
                            id = (rnum + strt) % self.net_size
                        if repe < maxrep:
                            nsucc += [id]
                            nsucc.remove(k)
    #                            print("nsucc:", nsucc)
                            addb += [(mapp, id)]
                            rmvb += [(mapp, k)]
#                            print("rmv1:", rmvb)    
#                            print("add1:", addb)
                            succ_in_cnt -= 1
                            succ_out_cnt += 1
    #                            print(mapp, len(succ), succ_in_cnt, succ_out_cnt)
                else:
                # if k >= self.comm_size:
                    succ_out_cnt += 1
                    if succ_out_cnt > follower_out:
                        id = k
                        repe = 0
                        while ((id in nsucc or id == mapp) and repe < maxrep):
                            repe += 1
                            rnum = rd.randint(0, self.comm_size)
#                            id = (rnum + comm_id * self.comm_size) % self.net_size
                            id = rnum + strt
                        if repe < maxrep:
                            nsucc += [id]
                            nsucc.remove(k)
    #                            print("nsucc:", nsucc)            

                            addb += [(mapp, id)]
                            rmvb += [(mapp, k)]
#                            print("rmv2:", rmvb)
#                            print("add2:", addb)
                            succ_out_cnt -= 1
                            succ_in_cnt += 1
    #                            print(mapp, len(succ), succ_in_cnt, succ_out_cnt)
            in_follower += succ_in_cnt
            out_follower += succ_out_cnt
            
        # print(in_follower, out_follower)  
        return (addb, rmvb, in_follower, out_follower)

#     def init_snet(self):
#         """
#         node_states[0]:   whether the node has alread retweeted (True) or not (False).
#         node_states[1]:   How many times a node received retweets before it retweeted.
################ 2020 6/27 rate
#         node_states[2]:   whether the node belong to community i (i=1000 indicates non-community mem).
# ################ 2020 6/4 2communities
#         node_states[3]:   How many times a node received retweets after it retweeted.
#         """
#         self.node_states = [[False, 0, False, 0] for _ in range(self.net_size)]
# ################ 2020 6/4 2communities
#         for i in range(self.comm_size):
# ################ 2020 6/25 comm_strt            
#             self.node_states[i + self.comm_size * self.comm_strt][2] = True
#         # for i in range(self.net_size): print(i, self.node_states[i])


    # def exe_sim(self, sim_time, mu):
    def exe_sim(self, sim_time, rtrate_com, rtrate_oth, rtrate_ocom, shape, maxday, 
                delta=0.0, comm_on=1, init_out=0, sin=0):
        """
        rtrate_com: retweet rate inside community 0
        rtrate_oth: retweet rate outside the community
        rtrate_ocom: retweet rate inside community >=1
        shape: exponent of bounded pareto distr.
        maxday: maximum value of bounded pareto distr.
        prop[0]: num of RTs by community members
        prop[1]: unused (num of rcved by community members)
        prop[2]: num of RTs
        prop[3]: unused (num of rcved)
        prop[4]: unused (num of new followers who have not retweeted)
        prop[5]: alpha
        prop[6]: accumulated number of RTs by community members
        prop[7]: accumulated number of RTs 
        prop[8]: unused (accumulated number of new followers who have not retweeted)
################ 2020 6/4 2communities
        prop[9]: beta-min
        prop[10]: beta-max
################ 2020 6/11 weight
		self.num_rcv accumulated number of RT received by followers who have not retweeted
        """

################ 2020 6/4 2communities
        # self.prop += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
################ 2020 6/4 2communities
        self.user_para = {0: rtrate_com, 1: rtrate_oth, 2: rtrate_ocom}
        self.num_rt = 0
        self.num_rt_comm = 0
################ 2020 6/11 weight
        self.num_rcv = 0
        self.cur_time = 1
        rd.seed(seed=self.seed)
        start = time.time()
        sched = [[] for _ in range(sim_time)]
################ 2020 6/21 more
        if self.more == 0:
            for i in range(self.fw_size):
                rn = self.truncated_pareto(shape, 1, maxday)
################ 2020 6/15 weight
                if i < self.fw_size - init_out:
################ 2020 6/25 comm_strt            
                    sched[int(rn)] += [i + self.comm_size * self.comm_strt]
    #                print(i)
                else:
                    fout = self.net_size - 1 + self.fw_size - init_out - i
    #                print(fout, flush=True)                
                    sched[int(rn)] += [fout]
################ 2020 6/21 more
        elif self.more == 1:
            setofinit = []
            for _ in range(self.fw_size):
                rn = self.truncated_pareto(shape, 1, maxday)
                rnum = rd.randint(self.net_size)
                while (rnum in setofinit):
                    # print(rnum, setofinit)
                    rnum = rd.randint(self.net_size)
                setofinit += [rnum]
                sched[int(rn)] += [rnum]
            # print(setofinit)
################ 2020 7/3 
        elif self.more == 2:
            setofinit = []
            for i in range(self.fw_size):
                rn = self.truncated_pareto(shape, 1, maxday)
                if i < self.fw_size - init_out:
                    rnum = rd.randint(self.fw_size)
                    while (rnum in setofinit):
                        # print(rnum, setofinit)
                        rnum = rd.randint(self.fw_size)
                    setofinit += [rnum]
                    sched[int(rn)] += [rnum + self.comm_size * self.comm_strt]
                else:
                    rnum = rd.randint(self.fw_size, self.net_size)
                    while (rnum in setofinit):
                        # print(rnum, setofinit)
                        rnum = rd.randint(self.fw_size, self.net_size)
                    setofinit += [rnum]
                    fout = (rnum + self.comm_size * self.comm_strt) % self.net_size
                    sched[int(rn)] += [fout]
        else:
            setofinit = []
            for i in range(self.fw_size):
                rn = self.truncated_pareto(shape, 1, maxday)
                if i < self.fw_size - init_out:
                    rnum = rd.randint(self.comm_size)
                    while (rnum in setofinit):
                        # print(rnum, setofinit)
                        rnum = rd.randint(self.comm_size)
                    setofinit += [rnum]
                    sched[int(rn)] += [rnum + self.comm_size * self.comm_strt]
                else:
                    rnum = rd.randint(self.comm_size, self.net_size)
                    while (rnum in setofinit):
                        # print(rnum, setofinit)
                        rnum = rd.randint(self.comm_size, self.net_size)
                    setofinit += [rnum]
                    fout = (rnum + self.comm_size * self.comm_strt) % self.net_size
                    sched[int(rn)] += [fout]            
        print("sim_1: ", time.time() - start)

        start = time.time()
        no_retweet_count = 0
        while self.cur_time < sim_time:
            if len(sched[0]) == 0:
# No more user decisions in this minute
                self.prop[-1][6] = self.num_rt_comm
                self.prop[-1][7] = self.num_rt
                if self.prop[-1][2] == 0:
# There were no retweets in this minute
                    no_retweet_count += 1
                    if no_retweet_count == maxday:
# There were no retweets for maxday minutes
                        print("sim_2: ", time.time() - start)
################# May 20 2020 No.2
                        print("cur_time=", self.cur_time, "len(prop)=", len(self.prop))
#################
                        return                
                else:
# There was at least one retweet in this minute
                    no_retweet_count = 0
# Initializing for the next minute
################ 2020 6/4 2communities
                self.prop += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
################ 2020 6/4 2communities
                sched.pop(0)
                self.cur_time += 1
################# May 20 2020 No.3
#                continue
#################             
            else:
# There are still user to decide in this minute            
                head = sched[0].pop(0)
                if self.node_states[head][0]:
# The head has already retweeted
################# May 20 2020 No.4
                    self.node_states[head][3] += 1
#################                     
                    continue
                self.node_states[head][1] += 1
################ 2020 6/11 weight, 7/14 sin
                self.num_rcv += 1
                if rd.rand() <= self.discnt(head, delta, comm_on, sin):
# A head retweets
                    self.node_states[head][0] = True
                    self.num_rt += 1
                    self.prop[-1][2] += 1
################ 2020 6/11 weight
#                    if head_comm == 0:
                    if self.node_states[head][2] == 0:
# The head belongs to the community
                        self.num_rt_comm += 1
                        self.prop[-1][0] += 1
# scheduling
                    if self.out_degree(head) != 0:
# the number of followers is not zero
                        for j in self.successors(head):
                            if not self.node_states[j][0]:
# A follower have not retweeted yet
                                rn = self.truncated_pareto(shape, 1, maxday)
                                sched[int(rn)] += [j]
################# May 20 2020 No.5                                
                            else:
                                self.node_states[head][3] += 1       
#################                                
        print("Simulation ends while progressing")
        return

################ 2020 6/11 weight
    def discnt(self, vertex, delta, comm_on, sin):
        """
		comm_on=2: fluctuate the retweet rates 
		comm_on=1: fluctuate only if from community members 
		comm_on=0: fluctuate only if from non-community members
        node_states[1]: How many times a node received retweets before it retweeted.
        node_states[2]: whether the node belong to community i (i=1000 indicates non-community mem).
		user_para = {0: rtrate_com, 1: rtrate_oth, 2: rtrate_ocom}
        """           
        
        if self.node_states[vertex][1] >= self.maxrecv:
            discnt = 0
        else:
            discnt = self.dcnt_fun[self.node_states[vertex][1] - 1]
        # if self.num_rcv < 10: print("discnt=", discnt)
################ 2020 6/27 rate                    
        if self.node_states[vertex][2] == 0:
            node_type = 0 
        elif self.node_states[vertex][2] == 1000:
            node_type = 1
        else:
            node_type = 2
################ 2020 6/27 rate                    
        if comm_on == 1 and node_type != 0: 
        	delta = 0.0
        if comm_on == 0 and node_type == 0: 
        	delta = 0.0        
        # if comm_on == 1 and node_type == 1: 
        # 	delta = 0.0
        # if comm_on == 0 and node_type == 0: 
        # 	delta = 0.0
  ################ 2020 7/14 sin
        if sin == 1:
            day = 0.1 * np.sin(2.0 * np.pi * self.cur_time / 1440.0)
            # if self.cur_time <= 1440:
            #     print("time=", self.cur_time, "sin=", day)
        else:
            day = 0.0
    
        if self.num_rcv % 2 == 0:
        	rtrate = self.user_para[node_type] * discnt * (1 + delta) * (1 + day)
#        	if self.num_rcv < 20:
#        		print(self.num_rcv)
        else:
        	rtrate = self.user_para[node_type] * discnt * (1 - delta) * (1 + day)
        return rtrate
    
    def truncated_pareto(self, alpha, m, b):
        """
        Random bounded Pareto variate.
        """
        u = rd.rand()
        return (-(u * b ** alpha - u * m ** alpha - b ** alpha) /
                (b ** alpha * m ** alpha)) ** (-1. / alpha)

    def truncated_pareto_expval(self, alpha, m, b):
        """
        Expected value of truncated Pareto distribution.
        """
        if alpha <= 1:
            return 1000000
        part1 = (m ** alpha) / (1. - (m / b) ** alpha)
        part2 = 1. * alpha / (alpha - 1)
        part3 = (1. / (m ** (alpha - 1)) - 1. / (b ** (alpha - 1.)))
        return part1 * part2 * part3

# link = self.edges()
# for i in range(self.net_size):
#    print(user[i])
#    print(self.succ[i].items())
#    print(self.successors(i))


# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.hist(rn, bins=50)
# fig.show()
