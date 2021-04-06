# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 10:29:40 2018
Execute simulations

@author: oida
"""

import snet_2com_weight_init_more_start_rate_sin as snet
import numpy as np
import datetime
import networkx as nx
import pandas as pd
import argparse
import multiprocessing as mp

sim_time = 100000   # maximum simulation time
net_size = 800000   # network size (N)
comm_size = 1000    # size of community 1 (C) 
comm_size2 = 100    # sizes of community >1 ~ U(c,c2), c2=0 implies they are fixed at c 
fw_size = 100       # number of initiator's followers (F_0), F_0 = F (mean number of followers) for SW and ER
rtrate_com = 0.03   # retweet rate of community 1 members (lambda_1)
rtrate_oth = 0.03   # retweet rate of users not belonging to any community (lambda_0)
rtrate_ocom = 0.03  # retweet rate of community >1 members (lambda_>1)
p=0                 # parameter of SF and SW (p=0.01 for SW, p=0 for SF)
q=0                 # parameter of SF (q=0 for SF)
dcnt = 1            # weight func, 0: independent, 1: 0.9^n-1, 2: 1/n, 3: linear, 4: [n=1], 5: social reinf
shape = 1.2         # shape of truncated Pareto (a)
maxday = 3 * 1440   # scale of truncated Pareto (b)
netprop = 2         # graph type, 0: ER, 1: SW, 2: SF, >2: Pokec
batch_size = 1000   # number of samples
comm_num=20          # number of communities (N_c)
alpha=0.2             # cohesion of community 1, alpha=1 implies alpha_1=NC
beta=0.5             # cohesion of community >1, beta=1 implies alpha_>1=NC
delta=0.0           # size of order-dependent fluctuations in retweet prob 
comm_on=2           # place where fluctuations occur, comm_on=2 implies everywhere
init_out=0          # number of initiator's followers not belonging to community 1
more = 2            # method of selecting initiator's followers
comm_strt=0         # offset added to user id
rate_rewire=0.01    # rate of links rewired


def sim(seed = None):
    G = snet.Snet(seed=seed, net_size=net_size, comm_size=comm_size, comm_size2=comm_size2, fw_size=fw_size, 
              p=p, q=q, dcnt=dcnt, alpha=alpha, beta=beta, comm_num=comm_num, more=more, 
              comm_strt=comm_strt,rate_rewire=rate_rewire)
    G._random_snet(netprop=netprop)    
    G.exe_sim(sim_time=sim_time, rtrate_com=rtrate_com, rtrate_oth=rtrate_oth, rtrate_ocom=rtrate_ocom, 
              shape=shape, maxday=maxday, delta=delta, comm_on=comm_on, init_out=init_out)
    if nx.is_strongly_connected(G) == False:
        print("strong:", nx.is_strongly_connected(G))
    print('alpha=', G.prop[0][5], 'beta-min=', G.prop[0][9], 'beta-max=', G.prop[0][10], 
          'time=', G.cur_time - maxday, 'retweets=', G.num_rt, 'comm_retweets=', G.num_rt_comm)
    return [G.prop[0][5], G.prop[0][9], G.prop[0][10], G.cur_time - maxday, G.num_rt, G.num_rt_comm]
                   
if __name__ == '__main__':

    now = datetime.datetime.now().date()
    condition = '_n' + str(net_size) + '_cn' + str(comm_num) + '_cs' + str(comm_strt) \
                + '_a' + str(alpha) + '_b' + str(beta) + '_dlt' + str(delta) + '_on' + str(comm_on) \
                + '_i' + str(init_out) + '_c' + str(comm_size) + '_c2' + str(comm_size2) + '_f' + str(fw_size) \
                + '_r1' + str(rtrate_com) + '_r2' + str(rtrate_oth) + '_r3' + str(rtrate_ocom)\
                + '_p' + str(p) + '_q' + str(q) + '_d' + str(dcnt) + '_s' + str(shape) + '_m' + str(maxday) \
                + '_net' + str(netprop) + '_mo' + str(more) + '_ba' + str(batch_size) + '_rw' + str(rate_rewire) 
    outcome_fname = str(now) + condition
    p_cores = mp.cpu_count()
    print ("p_cores=", p_cores)
    pool = mp.Pool(5)
    agg = pool.map(sim, range(batch_size))
    outcome = []
    for tmp in agg:
        outcome.append(tmp)

   
    
    pd.set_option('display.max_columns', 100)
    outcome_np = np.array(outcome)
    outcome_df = pd.DataFrame(outcome_np, 
            columns=["alpha_init", "alpha", 'beta', "time", "retweet", "comm_retweet"])
    print(outcome_df)
    np.save(outcome_fname, outcome_np)

    # sim(0)





















    


