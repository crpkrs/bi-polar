# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 12:44:39 2018

Generate social networks with no node attributes
             G.edges[i,j]
             net_size: total number of users
             comm_size: number of members in community 1
             fw_size: number of initiator's followers
             alpha: cohesion index of community 1, alpha>=1 denotes alpha_1=NC           
             beta: cohesion index of community >1, beta>=1 denotes alpha_>1=NC  

@author: oida
"""

import time
import networkx as nx
import numpy as np
# import matplotlib.pyplot as plt
import numpy.random as rd


class Snet(nx.DiGraph):
    """
    dcnt: a function as a number of received messages
    dcnt=0: independent
    dcnt=1: exponential
    dcnt=2: multiplicative
    dcnt=3: linear
    dcnt=4: simple contagion
    dcnt=5: social reinforcement
    """
    def __init__(self,
                 net_size=20,
                 comm_size=10,
                 comm_size2=0,
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
                 comm_strt=0,
################ 2021 3/27            
                 rate_rewire=0.0
                 ):
        super(Snet, self).__init__()
        self.net_size = net_size
        self.comm_size = comm_size
        self.comm_size2 = comm_size2
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
        self.rate_rewire=rate_rewire


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



    def _random_snet(self, netprop):
        """
        Generate a random graph including communities of cohesion indexes alpha and beta

        node_states[0]:   the user has alread retweeted (True) or not (False).
        node_states[1]:   number of times the user has received retweets before posting 
 ################ 2020 6/27 rate
        node_states[2]:   community id (which starts from zero) the user belongs to (1000 means nonexistence)
################ 2020 6/4 2communities
        node_states[3]:   number of times the user has received retweets after posting
        """
        
        if netprop == 0:
            G1 = nx.fast_gnp_random_graph(n=self.net_size, p=self.fw_size / (self.net_size - 1), seed=self.seed,
                                          directed=True)
        elif netprop == 1:
            H = nx.connected_watts_strogatz_graph(n=self.net_size, k=self.fw_size, p=self.p, seed=self.seed)
            G1 = H.to_directed()

        elif netprop == 2:
            H = nx.extended_barabasi_albert_graph(n=self.net_size, m=8, p=self.p, q=self.q, seed=self.seed)
            G1 = H.to_directed()

        else:
        # Pokec
            G1 = self.G
            
            
            
################ 2021 3/27  rewire links randomly with a rate of rate_rewire

        n_size = self.net_size
        l_size = len(G1.edges)
        num_rwir = round(self.rate_rewire * l_size)
        # print("num_rwir", num_rwir)         
        if num_rwir != 0:
            G1_list = list(G1.edges)
            G2 = nx.DiGraph()
            G2.add_edges_from(G1.edges)
            l_select = []
            # add_link = []
            # rmv_link = []
            for i in range(num_rwir):
                # if (i % 10000 == 0 ): print("i=", i)
                pt = rd.randint(0,l_size)
                while (pt in l_select):
                    pt = rd.randint(0,l_size)
                l_select += [pt]
                n1 = G1_list[pt][0]
                s1 = G1_list[pt][1]
                n2 = rd.randint(0,n_size)
                while (n2 in G1.successors(n1) or n2 in G2.successors(n1) or n1 == n2):
                    n2 = rd.randint(0,n_size)   
                # print(G1_list[pt], pt, n1, s1, n2)
                G1.remove_edge(n1,s1)
                G1.add_edge(n1,n2)
                
            #     rmv_link += [(n1,s1)]
            #     add_link += [(n1,n2)]
            # G1.remove_edges_from(rmv_link)
            # G1.add_edges_from(add_link)
            
            # print("Total links:", len(G1.edges), "rewired:", num_rwir)
            # print("rmv: ", rmv_link, "add: ", add_link)
            # print(len(G1.edges), list(G1.edges))         
################ 2021 3/27            
                            
    
            

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

    def _create_comm(self, comm_id):
        """
        Create a community according to Algorithm 1 in the paper.
        alpha and beta correspond to cohesion indexes of community 1 and >1
        """

        rd.seed(seed=self.seed)
        in_follower = 0
        out_follower = 0
        addb = []
        rmvb = []
        maxrep = 1000
################ 2020 6/4 2communities
        if comm_id == 0: # comm_id=0 corresponds to C_1
            index = self.alpha
            c_size = self.comm_size
        else:
            index = self.beta
            if self.comm_size2 == 0:
                c_size = self.comm_size
            else:
                c_size = rd.randint(self.comm_size2, self.comm_size+1)
################ 2020 6/25 comm_strt
        strt = comm_id * self.comm_size * 2 + self.comm_size * self.comm_strt
################ 2020 6/22        
        if strt >= self.net_size:
            strt = self.comm_size + strt % self.net_size
        for i in range(c_size):
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
                if  strt <= k and k < strt + c_size:
                    succ_in_cnt += 1
                    if succ_in_cnt > follower_in:
                        id = k
                        repe = 0
                        while (id in nsucc and repe < maxrep):
                            repe += 1
                            rnum = rd.randint(c_size, self.net_size)
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
                    succ_out_cnt += 1
                    if succ_out_cnt > follower_out:
                        id = k
                        repe = 0
                        while ((id in nsucc or id == mapp) and repe < maxrep):
                            repe += 1
                            rnum = rd.randint(0, c_size)
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


    # def exe_sim(self, sim_time, mu):
    def exe_sim(self, sim_time, rtrate_com, rtrate_oth, rtrate_ocom, shape, maxday, 
                delta=0.0, comm_on=1, init_out=0, sin=0):
        """
        Execute event-driven simulation

        rtrate_com: retweet rate inside community 1
        rtrate_oth: retweet rate outside communities
        rtrate_ocom: retweet rate inside community >1
        shape: exponent of bounded Pareto
        maxday: maximal value of bounded Pareto
        prop[0]: number of RTs by community 1 members at this minute
        prop[1]: unused 
        prop[2]: number of RTs at this minute
        prop[3]: unused 
        prop[4]: unused 
        prop[5]: cohesion index alpha_1
        prop[6]: accumulated number of RTs by community 1 members
        prop[7]: accumulated number of RTs 
        prop[8]: unused 
################ 2020 6/4 2communities
        prop[9]: min cohesion index of alpha_>1
        prop[10]: max cohesion index of alpha_>1
################ 2020 6/11 weight
		self.num_rcv: accumulated number of RTs received by users who have not retweeted
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
# No more events at this minute
                self.prop[-1][6] = self.num_rt_comm
                self.prop[-1][7] = self.num_rt
                if self.prop[-1][2] == 0:
# No retweets are posted at this minute
                    no_retweet_count += 1
                    if no_retweet_count == maxday:
# No retweets for maxday period
                        print("sim_2: ", time.time() - start)
################# May 20 2020 No.2
                        print("cur_time=", self.cur_time, "len(prop)=", len(self.prop))
#################
                        return                
                else:
# At least one retweet exists at this minute
                    no_retweet_count = 0
# Initialization before going on to the next minute
################ 2020 6/4 2communities
                self.prop += [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
################ 2020 6/4 2communities
                sched.pop(0)
                self.cur_time += 1
################# May 20 2020 No.3
#                continue
#################             
            else:
# There still exists an event at this minute            
                head = sched[0].pop(0)
                if self.node_states[head][0]:
# The user has already retweeted
################# May 20 2020 No.4
                    self.node_states[head][3] += 1
#################                     
                    continue
                self.node_states[head][1] += 1
################ 2020 6/11 weight, 7/14 sin
                self.num_rcv += 1
                if rd.rand() <= self.discnt(head, delta, comm_on, sin):
# A user post a retweet
                    self.node_states[head][0] = True
                    self.num_rt += 1
                    self.prop[-1][2] += 1
################ 2020 6/11 weight
#                    if head_comm == 0:
                    if self.node_states[head][2] == 0:
# The user belongs to community 1
                        self.num_rt_comm += 1
                        self.prop[-1][0] += 1
# Put new events in the calendar
                    if self.out_degree(head) != 0:
# At least one follower of the user exists
                        for j in self.successors(head):
                            if not self.node_states[j][0]:
# The follower has not retweeted yet
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
        Calculate a retweet probability
        
		comm_on=2: retweet probability fluctuates everywhere 
		comm_on=1: fluctuate only inside community 1 
		comm_on=0: fluctuate only outside community 1 
		user_para = {0: rtrate_com, 1: rtrate_oth, 2: rtrate_ocom}
        delta: size of order-dependent fluctuations in retweet prob (delta_1)
        sin: daily cycle fluctuations start (1) or not (0)
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
