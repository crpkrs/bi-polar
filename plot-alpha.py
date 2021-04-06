# -*- coding: utf-8 -*-
"""
Created on Mon May 27 08:42:38 2019

@author: oida
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os.path
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages



def Lplot(fname='', title='', oname='', vc=10.0, xmax=0, gridon=0):
    ten_name = fname  + '.npy'
    ten_np = np.load(ten_name)
#    print(ten_np)
    ten = ten_np.tolist()
    avg_vc = []
    std_vc = []
    temp = []
    i = 0
    for k in range(len(ten)):
#            print("i=", i, ten[k])
        if ten[k][3] > 60000: print('############### time-limit', ten[k][3])
        if ten[k][4] >= vc: 
            temp.append(ten[k])
            i = i + 1

    print("i=", i)
    avg_vc.append(np.average(temp, axis=0))
    std_vc.append(np.std(temp, axis=0))
        
    avg_vc_np = np.array(avg_vc)
    std_vc_np = np.array(std_vc)
    pd.set_option('display.max_columns', 200)
    avg_vc_df = pd.DataFrame(avg_vc_np, 
        columns=["alpha_init", "alpha", 'beta', "time", "retweet", "comm_retweet"])
    # print(avg_vc_df)
    std_vc_df = pd.DataFrame(std_vc_np, 
        columns=["alpha_init", "alpha", 'beta', "time", "retweet", "comm_retweet"])
    # print(std_vc_df)
    # print(std_vc_df.div(avg_vc_df))            

     # Treq = prop_np[:,0]
    nt = np.array(temp)
    fig = plt.figure(figsize=(6,4.5))

    # fig = plt.figure()
    plt.hist(nt[:,4], bins=40, alpha=0.5, histtype='stepfilled')
    # plt.axvline(nt[:,4].mean(), color='black')
    if xmax == 0: plt.xlim(0,)
    else: plt.xlim(0,xmax)
    plt.ylim(0.8,1000)
    # plt.xscale('log')
    plt.title(title, fontsize=22, pad=15)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    if gridon == 1: plt.grid()
    plt.yscale('log')
    # plt.xlabel("Cascade size", fontsize=20)
    plt.xlabel("Cascade size", fontsize=20, labelpad=12)
    fig.tight_layout()
    plt.show()
    file = oname + '.pdf'
    pdf = PdfPages(file)
    pdf.savefig(fig)
    pdf.close()  



# increases in r1(=\lambda_1), r2(=\lambda_0), r3(=\lambda_i, i>=2)
fn ='2021-02-23_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(a) $\alpha_1=NC$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='nc-l0.02')

fn ='2021-02-10_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(b) $\alpha_1=0.2$, $N_c=20$, $\lambda_0^{20}=0.03$'
Lplot(fn,title, vc=0, oname='20comm-l0.03', xmax=14000)

# fn ='2020-07-22_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(c) $\alpha_1=NC$, $\lambda_0^1=0.025$'
# Lplot(fn,title, vc=0, oname='nc-l0.025')

# fn ='2020-07-22_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(d) $\alpha_1=NC$, $\lambda_0^1=0.03$'
# Lplot(fn,title, vc=0, oname='nc-l0.03')

# increases in alpha 
# fn ='2020-07-27_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(e) $\alpha_1=0.1$, $\lambda_0^1=0.02$'
# Lplot(fn,title, vc=0, oname='1comm-a0.1', xmax=3000)

# fn ='2020-07-28_n800000_cn1_cs0_a0.2_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(f) $\alpha_1=0.2$, $\lambda_0^1=0.02$'
# Lplot(fn,title, vc=0, oname='1comm-a0.2', xmax=3500)

# increases in comm_num 
# fn ='2020-07-27_n800000_cn2_cs0_a1_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(g) $\alpha_1=NC$, $N_c=2$, $\lambda_0^2=0.02$'
# Lplot(fn,title, vc=0, oname='1comm-b0.5', xmax=3000)

# fn ='2020-07-21_n800000_cn20_cs0_a1_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(h) $\alpha_1=NC$, $N_c=20$, $\lambda_0^{20}=0.02$'
# Lplot(fn,title, vc=0, oname='19comm-b0.5', xmax=3500)

# social reinforcement
# fn ='2020-10-20_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.04_r20.04_r30.02_p0_q0_d5_s1.2_m4320_net2_mo0_ba1000'
# title = r'(j) $\lambda_0^1=0.04$, $d(n)=1-5\cdot 0.1^n$'
# Lplot(fn,title, vc=0, oname='r10.04-d5')

# fn ='2020-10-20_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo0_ba1000'
# title = r'(i) $\lambda_0^1=0.03$, $d(n)=1-5\cdot 0.1^n$'
# Lplot(fn,title, vc=0, oname='r10.03-d5')

# Pokec
# fn ='2020-09-24_n1632803_cn1_cs100_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.017_r20.017_r30.017_d1_s1.2_m4320_net4_mo0_ba1000'
fn ='2021-02-11_n1632803_cn1_cs100_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.017_r20.017_r30.017_d1_s1.2_m4320_net4_mo0_ba1000'
title = r'(k) Pokec, $\alpha_1=NC$, $\lambda_0^1=0.017$'
Lplot(fn,title, vc=0, oname='Pokec-r10.017-cs100')

# fn ='2020-09-25_n1632803_cn1_cs100_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.03_r20.03_r30.03_d1_s1.2_m4320_net4_mo0_ba1000'
fn ='2021-02-13_n1632803_cn1_cs100_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.03_r20.03_r30.03_d1_s1.2_m4320_net4_mo0_ba1000'
title = r'(l) Pokec, $\alpha_1=NC$, $\lambda_0^1=0.03$'
Lplot(fn,title, vc=0, oname='Pokec-r10.03-cs100')


# random community size and rewiring links
fn ='2021-03-30_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_c2100_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000_rw0.01'
title = r'(m) SF, $|\mathbb{C}_i| \sim U(10^2,10^3)$, $r_w=1\%$'
Lplot(fn,title, vc=0, oname='20comm-l0.03-rc-rw', xmax=14000)

fn ='2021-03-31_n200000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_c2100_f50_r10.04_r20.04_r30.04_p0.01_q0_d1_s1.2_m4320_net1_mo2_ba1000_rw0.01'
title = r'(n) SW, $|\mathbb{C}_i| \sim U(10^2,10^3)$, $r_w=1\%$'
Lplot(fn,title, vc=0, oname='SW-20comm-l0.04-rc-rw', xmax=50000)

fn ='2021-03-31_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_c2100_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000_rw0.0'
title = r' SF, $|\mathbb{C}_i| \sim U(10^2,10^3)$'
Lplot(fn,title, vc=0, oname='20comm-l0.03-rc', xmax=14000)

fn ='2021-04-01_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_c20_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000_rw0.01'
title = r' SF, $r_w=1\%$'
Lplot(fn,title, vc=0, oname='20comm-l0.03-rw', xmax=14000)











