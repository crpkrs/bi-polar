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
net_size = 1632803  # network size (N)
comm_size = 1000    # community size (C)
fw_size = 200       # number of initiator's followers (F_0)
rtrate_com = 0.03   # retweet rate of community 1 members (lambda_1)
rtrate_oth = 0.03   # retweet rate of users not belonging to any community (lambda_0)
rtrate_ocom = 0.03  # retweet rate of community >1 members (lambda_>1)
# p=0               # parameter of SF and SW (p=0.01 for SW, p=0 for SF)
# q=0               # parameter of SF (q=0 for SF)
dcnt = 1            # weight func, 0: independent, 1: 0.9^n-1, 2: 1/n, 3: linear, 4: [n=1], 5: social reinf
shape = 1.2         # shape of truncated Pareto (a)
maxday = 3 * 1440   # scale of truncated Pareto (b)
netprop = 4         # graph type, 0: ER, 1: SW, 2: SF, >2: Pokec
batch_size = 1000   # number of samples
comm_num=1          # number of communities (N_c)
alpha=1             # cohesion of community 1, alpha=1 implies alpha_1=NC
beta=1              # cohesion of community >1, beta=1 implies alpha_>1=NC
delta=0.0           # size of order-dependent fluctuations in retweet prob (delta_1)
comm_on=2           # place where fluctuations occur, comm_on=2 implies everywhere
init_out=0          # number of initiator's followers who are not community 1 members (R_i=100*(f-init_out)/f)
more = 0            # method of selecting initiator's followers
comm_strt=100       # offset added to user id


G1 = nx.DiGraph()
linknp=np.loadtxt("soc-pokec-relationships.txt", dtype='int32')
for i in range(len(linknp)):
    G1.add_edge(linknp[i][0]-1, linknp[i][1]-1)
# net_size = nx.number_of_nodes(G1) # 1632803
    
def sim(seed = None):
    G = snet.Snet(seed=seed, net_size=net_size, comm_size=comm_size, fw_size=fw_size, 
              dcnt=dcnt, alpha=alpha, beta=beta, comm_num=comm_num, more=more, 
              comm_strt=comm_strt, G=G1)
    G._random_snet(netprop=netprop)             
    G.exe_sim(sim_time=sim_time, rtrate_com=rtrate_com, rtrate_oth=rtrate_oth, rtrate_ocom=rtrate_ocom, 
              shape=shape, maxday=maxday, delta=delta, comm_on=comm_on, init_out=init_out)
    print('alpha=', G.prop[0][5], 'beta-min=', G.prop[0][9], 'beta-max=', G.prop[0][10], 
          'time=', G.cur_time - maxday, 'retweets=', G.num_rt, 'comm_retweets=', G.num_rt_comm)
    # outcome.append([G.prop[0][5], G.prop[0][9], G.prop[0][10], G.cur_time - maxday, G.num_rt, G.num_rt_comm])
    return [G.prop[0][5], G.prop[0][9], G.prop[0][10], G.cur_time - maxday, G.num_rt, G.num_rt_comm]
                   
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Tweet Diffusion')
    # parser.add_argument('--delta', type=float)
    # args = parser.parse_args() 
    # print('delta', args.delta)
    # delta = args.delta

    now = datetime.datetime.now().date()
    condition = '_n' + str(net_size) + '_cn' + str(comm_num) + '_cs' + str(comm_strt) \
                + '_a' + str(alpha) + '_b' + str(beta) + '_dlt' + str(delta) + '_on' + str(comm_on) \
                + '_i' + str(init_out) + '_c' + str(comm_size) + '_f' + str(fw_size) \
                + '_r1' + str(rtrate_com) + '_r2' + str(rtrate_oth) + '_r3' + str(rtrate_ocom)\
                + '_d' + str(dcnt) + '_s' + str(shape) \
                + '_m' + str(maxday) + '_net' + str(netprop) + '_mo' + str(more) + '_ba' + str(batch_size)
      
    outcome_fname = str(now) + condition
    p_cores = mp.cpu_count()
    print ("p_cores=", p_cores)
    pool = mp.Pool(1)
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























    


