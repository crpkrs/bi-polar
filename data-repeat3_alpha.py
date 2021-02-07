# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 10:29:40 2018
Execute data collection

@author: kurosaki
"""

import snet_2com_weight_init_more_start_rate_sin as snet
import numpy as np
import datetime
import networkx as nx
import pandas as pd
import argparse
import multiprocessing as mp

sim_time = 100000
net_size = 800000 # 800000
comm_size = 1000 # 8000
fw_size = 100 #100 # fw_size < comm_size
rtrate_com = 0.06
rtrate_oth = 0.03
rtrate_ocom = 0.02
p=0
q=0
dcnt = 5 # 0: non-discount, 1: exp, 2: multi, 3: linear, 4: simple-contagion, 5: social reinforcement
shape = 1.2 # pareto shape
maxday = 3 * 1440 # pareto bound = 3 days (minutes)
netprop = 2 # 0: fast_gnp, 1: Wats, 2: Barabasi
batch_size = 1000 #10
comm_num=1
alpha=0.5
beta=1
delta=0.0 
comm_on=2
init_out=100
more = 2
comm_strt=0


def sim(seed = None):
    G = snet.Snet(seed=seed, net_size=net_size, comm_size=comm_size, fw_size=fw_size, 
              p=p, q=q, dcnt=dcnt, alpha=alpha, beta=beta, comm_num=comm_num, more=more, 
              comm_strt=comm_strt)
    G.seed = seed
    G._random_snet(netprop=netprop)    
    G.exe_sim(sim_time=sim_time, rtrate_com=rtrate_com, rtrate_oth=rtrate_oth, rtrate_ocom=rtrate_ocom, 
              shape=shape, maxday=maxday, delta=delta, comm_on=comm_on, init_out=init_out)
    if nx.is_strongly_connected(G) == False:
        print("strong:", nx.is_strongly_connected(G))
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
                + '_p' + str(p) + '_q' + str(q) + '_d' + str(dcnt) + '_s' + str(shape) \
                + '_m' + str(maxday) + '_net' + str(netprop) + '_mo' + str(more) + '_ba' + str(batch_size) 
    outcome_fname = 'data1/' + str(now) + condition
    p_cores = mp.cpu_count()
    print ("p_cores=", p_cores)
    pool = mp.Pool(4)
    agg = pool.map(sim, range(batch_size))
    outcome = []
    for tmp in agg:
        outcome.append(tmp)

    # for i in range(1):
    #     p = mp.Process(target=sim, args=(i, ))
    #     # outcome.append(p.start())
    #     p.start()
    
    # p.join()       
    
    pd.set_option('display.max_columns', 100)
    outcome_np = np.array(outcome)
    outcome_df = pd.DataFrame(outcome_np, 
            columns=["alpha_init", "alpha", 'beta', "time", "retweet", "comm_retweet"])
    print(outcome_df)
    np.save(outcome_fname, outcome_np)























    


