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
    ten_name = 'data1/' + fname  + '.npy'
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
        # if ten[k][4] < vc:
        #     print(ten[k][4])

    print("i=", i)
    avg_vc.append(np.average(temp, axis=0))
    std_vc.append(np.std(temp, axis=0))
        
    avg_vc_np = np.array(avg_vc)
    std_vc_np = np.array(std_vc)
    pd.set_option('display.max_columns', 200)
    avg_vc_df = pd.DataFrame(avg_vc_np, 
        columns=["alpha_init", "alpha", 'beta', "time", "retweet", "comm_retweet"])
    print(avg_vc_df)
    std_vc_df = pd.DataFrame(std_vc_np, 
        columns=["alpha_init", "alpha", 'beta', "time", "retweet", "comm_retweet"])
    # print(std_vc_df)
    print(std_vc_df.div(avg_vc_df))            

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



###################### beta ################
###################### SF #############

# fn ='2020-06-28_n800000_cn20_cs0_a0.5_b0.5_dlt0.0_on2_i0_c1000_f100_r10.07_r20.05_r30.06_p0_q0_d1_s1.2_m4320_net2_mo1_ba1000'
# title = 'SF cn=20, more=1, batch_size=1000, delta=0'
# Lplot(fn,title, vc=0)
# fn ='2020-06-29_n800000_cn20_cs0_a0.5_b0.5_dlt1.0_on2_i0_c1000_f100_r10.07_r20.05_r30.06_p0_q0_d1_s1.2_m4320_net2_mo1_ba1000'
# title = 'SF cn=20, more=1, batch_size=1000, delta=1'
# Lplot(fn,title, vc=0)
# fn ='2020-07-03_n800000_cn20_cs0_a0.5_b0.5_dlt0.0_on2_i50_c1000_f100_r10.07_r20.05_r30.06_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = 'SF cn=20, more=2, init_out=50, batch_size=1000, delta=0'
# Lplot(fn,title, vc=0)
# fn ='2020-07-04_n800000_cn20_cs0_a0.5_b0.5_dlt0.0_on2_i0_c1000_f100_r10.07_r20.05_r30.06_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = '20 comm., $\lambda_i,\lambda_o=0.07, 0.05$'
# Lplot(fn,title, vc=0, oname='20comm-l0.07')
# fn ='2020-07-19_n800000_cn20_cs0_a0.5_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = '20 comm. $\lambda_i=\lambda_o=0.02$'
# Lplot(fn,title, vc=0, oname='20comm-l0.02')
fn ='2020-08-06_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(b) $\alpha_1=0.2$, $N_c=20$, $\lambda_0^{20}=0.03$'
# title = r'(b) $\alpha_1=0.2$, $\alpha_2^{20}=0.5$, $\lambda_0^{20}=0.03$'
Lplot(fn,title, vc=0, oname='20comm-l0.03', xmax=14000)

# r1 and r2 increases
fn ='2020-07-20_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(a) $\alpha_1=NC$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='nc-l0.02')
fn ='2020-07-22_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(c) $\alpha_1=NC$, $\lambda_0^1=0.025$'
Lplot(fn,title, vc=0, oname='nc-l0.025')
fn ='2020-07-22_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(d) $\alpha_1=NC$, $\lambda_0^1=0.03$'
Lplot(fn,title, vc=0, oname='nc-l0.03')

fn ='2020-12-02_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.035_r20.035_r30.035_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'$\alpha_1=NC$, $\lambda_0^1=0.035$'
Lplot(fn,title, vc=0, oname='nc-l0.035')


# r1 or r2 increases
# fn ='2020-08-04_n800000_cn1_cs0_a0.2_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'1 comm., $\alpha=0.2$ $\lambda_i=0.02, \lambda_o=0.03$'
# Lplot(fn,title, vc=0, oname='1comm-li0.02-lo0.03')
# fn ='2020-08-06_n800000_cn1_cs0_a0.2_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'1 comm., $\alpha=0.2$ $\lambda_i=0.03, \lambda_o=0.02$'
# Lplot(fn,title, vc=0, oname='1comm-l0.03')
# fn ='2020-08-05_n800000_cn1_cs0_a0.2_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'1 comm., $\alpha=0.2$, $\lambda_i=\lambda_o=0.03$'
# Lplot(fn,title, vc=0, oname='1comm-l0.03')

# fn ='2020-08-07_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'No comm., $\lambda_i=0.02, \lambda_o=0.03$'
# Lplot(fn,title, vc=0, oname='nc-lo0.02-li0.03')
# fn ='2020-08-07_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.02_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'No comm., $\lambda_i=0.03, \lambda_o=0.02$'
# Lplot(fn,title, vc=0, oname='nc-lo0.03-li0.02')


# comm_num increases
fn ='2020-07-27_n800000_cn2_cs0_a1_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(g) $\alpha_1=NC$, $N_c=2$, $\lambda_0^2=0.02$'
Lplot(fn,title, vc=0, oname='1comm-b0.5', xmax=3000)
# fn ='2020-07-27_n800000_cn5_cs0_a1_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = 'SF cn=5, more=2, init_out=0, a=1, b=0.5'
# Lplot(fn,title, vc=0)
# fn ='2020-07-26_n800000_cn10_cs0_a1_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = 'SF cn=10, more=2, init_out=0, a=1, b=0.5'
# Lplot(fn,title, vc=0)
fn ='2020-07-21_n800000_cn20_cs0_a1_b0.5_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(h) $\alpha_1=NC$, $N_c=20$, $\lambda_0^{20}=0.02$'
Lplot(fn,title, vc=0, oname='19comm-b0.5', xmax=3500)


# alpha increases
fn ='2020-07-27_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(e) $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='1comm-a0.1', xmax=3000)
fn ='2020-07-28_n800000_cn1_cs0_a0.2_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
title = r'(f) $\alpha_1=0.2$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='1comm-a0.2', xmax=3500)




# init_out increases

# fn ='2020-07-20_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(e) 100%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='100%-a0.5', xmax=3000, gridon=1)
# # fn ='2020-07-23_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# # title = 'SF cn=1, more=2, init_out=10, a=0.5'
# # Lplot(fn,title, vc=0, oname='90%-a0.5', xmax=3000, gridon=1)
# fn ='2020-07-23_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(f) 50%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='50%-a0.5', xmax=3000, gridon=1)
# fn ='2020-07-24_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(g) 10%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='10%-a0.5', xmax=3000, gridon=1)
# # fn ='2020-07-25_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# # title = r'(h) 2%, $\alpha_1=0.5$'
# # Lplot(fn,title, vc=0, oname='2%-a0.5', xmax=3000, gridon=1)
# fn ='2020-07-25_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# title = r'(h) 0%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='0%-a0.5', xmax=3000, gridon=1)



#init_out increases
fn ='2020-08-31_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(a) $R_i=100\%$, $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='100%-a0.1', xmax=3000, gridon=1)
fn ='2020-08-31_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i10_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(b) 90% in $C_1$, $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='90%-a0.1', xmax=3000, gridon=1)
fn ='2020-08-03_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i50_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(b) $R_i=50\%$, $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='50%-a0.1', xmax=3000, gridon=1)
fn ='2020-08-04_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i90_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(c) $R_i=10\%$, $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='10%-a0.1', xmax=3000, gridon=1)
fn ='2020-09-02_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i98_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(d) 2%, $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='2%-a0.1', xmax=3000, gridon=1)
fn ='2020-09-01_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i100_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(d) $R_i=0\%$, $\alpha_1=0.1$, $\lambda_0^1=0.02$'
Lplot(fn,title, vc=0, oname='0%-a0.1', xmax=3000, gridon=1)

# fn ='2020-09-12_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i100_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba4000'
# title = r'(d) 0%, $\alpha_1=0.1, 40000$'
# Lplot(fn,title, vc=60, oname='0%-a0.1', xmax=3000, gridon=1)
# fn ='2020-09-13_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i98_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba2000'
# title = r'(d) 0%, $\alpha_1=0.1, 20000$'
# Lplot(fn,title, vc=60, oname='2%-a0.1', xmax=3000, gridon=1)

##### more = 3
# fn ='2020-09-02_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(e) 100%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='100%-a0.5-m3', xmax=3000, gridon=1)
# # fn ='2020-09-03_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# # title = r'(e) 90%, $\alpha_1=0.5$'
# # Lplot(fn,title, vc=0, oname='90%-a0.5-m3', xmax=3000, gridon=1)
# fn ='2020-09-04_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(f) 50%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='50%-a0.5-m3', xmax=3000, gridon=1)
# fn ='2020-09-04_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(g) 10%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='10%-a0.5-m3', xmax=3000, gridon=1)
# # fn ='2020-09-05_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# # title = r'(h) 2%, $\alpha_1=0.5$'
# # Lplot(fn,title, vc=0, oname='2%-a0.5-m3', xmax=3000, gridon=1)
# fn ='2020-09-06_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 0%, $\alpha_1=0.5$'
# Lplot(fn,title, vc=0, oname='0%-a0.5-m3', xmax=3000, gridon=1)

##### lambda1=0.6
fn ='2020-09-02_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(i) $R_i=100\%$, $\lambda_0=0.03$, $\lambda_1=0.06$'
Lplot(fn,title, vc=0, oname='100%-l0.06', xmax=14000, gridon=1)
# fn ='2020-09-02_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(f) 90%, $\lambda_0=0.03$, $\lambda_1=0.06$'
# Lplot(fn,title, vc=0, oname='90%-l0.06', xmax=14000, gridon=1)
fn ='2020-09-03_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(j) $R_i=50\%$, $\lambda_0=0.03$, $\lambda_1=0.06$'
Lplot(fn,title, vc=0, oname='50%-l0.06', xmax=14000, gridon=1)
fn ='2020-09-03_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(k) $R_i=10\%$, $\lambda_0=0.03$, $\lambda_1=0.06$'
Lplot(fn,title, vc=0, oname='10%-l0.06', xmax=14000, gridon=1)
# fn ='2020-09-06_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(l) 2%, $\lambda_0=0.03$, $\lambda_1=0.06$'
# Lplot(fn,title, vc=0, oname='2%-l0.06', xmax=14000, gridon=1)
fn ='2020-09-05_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(l) $R_i=0\%$, $\lambda_0=0.03$, $\lambda_1=0.06$'
Lplot(fn,title, vc=0, oname='0%-l0.06', xmax=14000, gridon=1)


##### lambda1=0.6, d=4
fn ='2020-09-02_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
title = r'(m) $R_i=100\%$, d(n)=[n=1]'
Lplot(fn,title, vc=0, oname='100%-l0.06-d4', xmax=2500, gridon=1)
# fn ='2020-09-03_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
# title = r'(m) 90%, d(n)=[n=1]'
# Lplot(fn,title, vc=0, oname='90%-l0.06-d4', xmax=2500, gridon=1)
fn ='2020-09-03_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
title = r'(n) $R_i=50\%$, d(n)=[n=1]'
Lplot(fn,title, vc=0, oname='50%-l0.06-d4', xmax=2500, gridon=1)
fn ='2020-09-04_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
title = r'(o) $R_i=10\%$, d(n)=[n=1]'
Lplot(fn,title, vc=0, oname='10%-l0.06-d4', xmax=2500, gridon=1)
# fn ='2020-09-04_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
# title = r'(p) 2%, d(n)=[n=1]'
# Lplot(fn,title, vc=0, oname='2%-l0.06-d4', xmax=2500, gridon=1)
fn ='2020-09-04_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
title = r'(p) $R_i=0\%$, d(n)=[n=1]'
Lplot(fn,title, vc=0, oname='0%-l0.06-d4', xmax=2500, gridon=1)


# ##### lambda1=0.6, 2com, a2=0.5

# # fn ='2020-09-05_n800000_cn2_cs0_a0.5_b0.5_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.06_p0_q0_d4_s1.2_m4320_net2_mo3_ba1000'
# # title = r'(q) 0%, $C_1$-$C_2$'
# # Lplot(fn,title, vc=0, oname='0%-cn2', xmax=2500, gridon=1)

# ##### lambda1=0.6, (s,m) = (0.8, 7T)

fn ='2020-09-10_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s0.8_m10080_net2_mo3_ba1000'
title = r'(q) $R_i=100\%$, (a,b)=(0.8,7T)'
Lplot(fn,title, vc=0, oname='100%-s08', xmax=14000, gridon=1)
# fn ='2020-09-09_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s0.8_m10080_net2_mo3_ba1000'
# title = r'(q 90%, (a,b)=(0.8,7T)'
# Lplot(fn,title, vc=0, oname='90%-s08', xmax=14000, gridon=1)
fn ='2020-09-09_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s0.8_m10080_net2_mo3_ba1000'
title = r'(r) $R_i=50\%$, (a,b)=(0.8,7T)'
Lplot(fn,title, vc=0, oname='50%-s08', xmax=14000, gridon=1)
fn ='2020-09-08_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s0.8_m10080_net2_mo3_ba1000'
title = r'(s) $R_i=10\%$, (a,b)=(0.8,7T)'
Lplot(fn,title, vc=0, oname='10%-s08', xmax=14000, gridon=1)
# fn ='2020-09-08_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s0.8_m10080_net2_mo3_ba1000'
# title = r'(t) 2%, (a,b)=(0.8,7T)'
# Lplot(fn,title, vc=0, oname='2%-s08', xmax=14000, gridon=1)
fn ='2020-09-07_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s0.8_m10080_net2_mo3_ba1000'
title = r'(t) $R_i=0\%$, (a,b)=(0.8,7T)'
Lplot(fn,title, vc=0, oname='0%-s08', xmax=14000, gridon=1)

# ##### d=0
# fn ='2020-09-10_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d0_s1.2_m4320_net2_mo3_ba1000'
# title = r'(u) 100%, d(n)=1'
# Lplot(fn,title, vc=0, oname='100%-d0', xmax=35000, gridon=1)
# # fn ='2020-09-09_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d0_s1.2_m4320_net2_mo3_ba1000'
# # title = r'(t) 90%, d(n)=1'
# # Lplot(fn,title, vc=0, oname='90%-d0', xmax=35000, gridon=1)
# fn ='2020-09-08_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d0_s1.2_m4320_net2_mo3_ba1000'
# title = r'(v) 50%, d(n)=1'
# Lplot(fn,title, vc=0, oname='50%-d0', xmax=35000, gridon=1)
# fn ='2020-09-08_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d0_s1.2_m4320_net2_mo3_ba1000'
# title = r'(w) 10%, d(n)=1'
# Lplot(fn,title, vc=0, oname='10%-d0', xmax=35000, gridon=1)
# # fn ='2020-09-08_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d0_s1.2_m4320_net2_mo3_ba1000'
# # title = r'(t) 2%, d(n)=1'
# # Lplot(fn,title, vc=0, oname='2%-d0', xmax=35000, gridon=1)
# fn ='2020-09-07_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d0_s1.2_m4320_net2_mo3_ba1000'
# title = r'(x) 0%, d(n)=1'
# Lplot(fn,title, vc=0, oname='0%-d0', xmax=35000, gridon=1)


##### d=4,  (s,m) = (2, T)
# fn ='2020-09-11_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s2.0_m1440_net2_mo3_ba1000'
# title = r'(y) 100%, (a,b)=(2.0,T)'
# Lplot(fn,title, vc=60, oname='100%-s2', xmax=2500, gridon=1)
# # fn ='2020-09-10_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s2.0_m1440_net2_mo3_ba1000'
# # title = r'(y) 90%, (a,b)=(2.0,T)'
# # Lplot(fn,title, vc=0, oname='90%-s2', xmax=2500, gridon=1)
# fn ='2020-09-09_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s2.0_m1440_net2_mo3_ba1000'
# title = r'(z) 50%, (a,b)=(2.0,T)'
# Lplot(fn,title, vc=0, oname='50%-s2', xmax=2500, gridon=1)
# fn ='2020-09-09_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s2.0_m1440_net2_mo3_ba1000'
# title = r'(aa) 10%, (a,b)=(2.0,T)'
# Lplot(fn,title, vc=0, oname='10%-s2', xmax=2500, gridon=1)
# # fn ='2020-09-08_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s2.0_m1440_net2_mo3_ba1000'
# # title = r'(m) 2%, (a,b)=(2.0,T)'
# # Lplot(fn,title, vc=0, oname='2%-s2', xmax=2500, gridon=1)
# fn ='2020-09-07_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d4_s2.0_m1440_net2_mo3_ba1000'
# title = r'(ab) 0%, (a,b)=(2.0,T)'
# Lplot(fn,title, vc=0, oname='0%-s2', xmax=2500, gridon=1)




# # fn ='2020-08-02_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i100_c1000_f100_r10.02_r20.02_r30.03_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# # title = 'SF cn=1, more=3, init_out=100, a=1'
# # Lplot(fn,title, vc=0)

# # fn ='2020-08-09_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# # title = r'0%, $\alpha=0.5$ more=3'
# # Lplot(fn,title, vc=0, oname='10%-a0.1')

# # fn ='2020-09-11_n800000_cn1_cs1_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# # title = r'0%, cs=1'
# # Lplot(fn,title, vc=0, oname='cs=1')

# ##### d=5
# fn ='2020-10-11_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo2_ba1000'
# title = '100%, d=5'
# Lplot(fn,title, vc=0)
# fn ='2020-10-11_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo2_ba1000'
# title = '90%, d=5'
# Lplot(fn,title, vc=0)
# fn ='2020-10-11_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo2_ba1000'
# title = '50%, d=5'
# Lplot(fn,title, vc=0)
# fn ='2020-10-11_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo2_ba1000'
# title = '10%, d=5'
# Lplot(fn,title, vc=0)
# fn ='2020-10-12_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo2_ba1000'
# title = '2%, d=5'
# Lplot(fn,title, vc=0)
# fn ='2020-10-11_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo2_ba1000'
# title = '0%, d=5'
# Lplot(fn,title, vc=0)



fn ='2020-10-20_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.04_r20.04_r30.02_p0_q0_d5_s1.2_m4320_net2_mo0_ba1000'
title = r'(j) $\lambda_0^1=0.04$, $d(n)=1-5\cdot 0.1^n$'
Lplot(fn,title, vc=0, oname='r10.04-d5')
fn ='2020-10-20_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.02_p0_q0_d5_s1.2_m4320_net2_mo0_ba1000'
title = r'(i) $\lambda_0^1=0.03$, $d(n)=1-5\cdot 0.1^n$'
Lplot(fn,title, vc=0, oname='r10.03-d5')


# ##### a=0.5 lambda_1=lambda_2=0.25

fn ='2020-09-15_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(e) $R_i=100\%$, $\alpha_1=0.5$, $\lambda_0^1=0.025$'
Lplot(fn,title, vc=0, oname='100%-a0.5-r10.025-m3', xmax=7000, gridon=1)
# fn ='2020-09-14_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 90%, $\alpha_1=0.5$, $\lambda_0^1=0.025$'
# Lplot(fn,title, vc=0, oname='90%-a0.5-r10.025-m3', xmax=7000, gridon=1)
fn ='2020-09-14_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(f) $R_i=50\%$, $\alpha_1=0.5$, $\lambda_0^1=0.025$'
Lplot(fn,title, vc=0, oname='50%-a0.5-r10.025-m3', xmax=7000, gridon=1)
fn ='2020-09-14_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(g) $R_i=10\%$, $\alpha_1=0.5$, $\lambda_0^1=0.025$'
Lplot(fn,title, vc=0, oname='10%-a0.5-r10.025-m3', xmax=7000, gridon=1)
# fn ='2020-09-14_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 2%, $\alpha_1=0.5$, $\lambda_0^1=0.025$'
# Lplot(fn,title, vc=0, oname='2%-a0.5-r10.025-m3', xmax=7000, gridon=1)
fn ='2020-09-14_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.025_r20.025_r30.025_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
title = r'(h) $R_i=0\%$, $\alpha_1=0.5$, $\lambda_0^1=0.025$'
Lplot(fn,title, vc=0, oname='0%-a0.5-r10.025-m3', xmax=7000, gridon=1)

# # ##### a=0.1, lambda1=0.6

# fn ='2020-09-16_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 90%, $\alpha_1=0.1$, $\lambda_1=0.06$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='90%-a0.1-r10.06', xmax=20000, gridon=1)
# fn ='2020-09-15_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 50%, $\alpha_1=0.1$, $\lambda_1=0.06$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='50%-a0.1-r10.06', xmax=20000, gridon=1)
# fn ='2020-09-15_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 10%, $\alpha_1=0.1$, $\lambda_1=0.06$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='10%-a0.1-r10.06', xmax=20000, gridon=1)
# fn ='2020-09-15_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 2%, $\alpha_1=0.1$, $\lambda_1=0.06$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='2%-a0.1-r10.06', xmax=20000, gridon=1)
# fn ='2020-09-15_n800000_cn1_cs0_a0.1_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 0%, $\alpha_1=0.1$, $\lambda_1=0.06$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='0%-a0.1-r10.06', xmax=20000, gridon=1)

# # ##### a=0.5, lambda1=0.5
# fn ='2020-09-16_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.05_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 50%, $\alpha_1=0.5$, $\lambda_1=0.05$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='50%-a0.5-r10.05', xmax=20000, gridon=1)
# # ##### a=0.1, lambda1=0.3
# fn ='2020-09-16_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.03_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 50%, $\alpha_1=0.5$, $\lambda_1=0.03$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='50%-a0.5-r10.03', gridon=1)

# ##### a=0.5, lambda1=0.4

# fn ='2020-09-18_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.04_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 100%, $\alpha_1=0.5$, $\lambda_1=0.04$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='100%-a0.5-r10.04', gridon=1)
# fn ='2020-09-17_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.04_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 90%, $\alpha_1=0.5$, $\lambda_1=0.04$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='90%-a0.5-r10.04', gridon=1)
# fn ='2020-09-16_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.04_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 50%, $\alpha_1=0.5$, $\lambda_1=0.04$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='50%-a0.5-r10.04', gridon=1)
# fn ='2020-09-17_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.04_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 10%, $\alpha_1=0.5$, $\lambda_1=0.04$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='10%-a0.5-r10.04', gridon=1)
# fn ='2020-09-17_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.04_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 2%, $\alpha_1=0.5$, $\lambda_1=0.04$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='2%-a0.5-r10.04', gridon=1)
# fn ='2020-09-18_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.04_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 0%, $\alpha_1=0.5$, $\lambda_1=0.04$, $\lambda_0=0.03$'
# Lplot(fn,title, vc=120, oname='0%-a0.5-r10.04', gridon=1)

# ##### lambda1=0.6, (s,m) = (0.8, 7T), d(n)=1/n

# fn ='2020-09-19_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i0_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d2_s0.8_m10080_net2_mo3_ba1000'
# title = r'(h) 100%, $(a,b)=(0.8,7T)$, $d=1/n$'
# Lplot(fn,title, vc=120, oname='100%-s08-d=n-1', gridon=1)
# fn ='2020-09-19_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i10_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d2_s0.8_m10080_net2_mo3_ba1000'
# title = r'(h) 90%, $(a,b)=(0.8,7T)$, $d=1/n$'
# Lplot(fn,title, vc=120, oname='90%-s08-d=n-1', gridon=1)
# fn ='2020-09-19_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d2_s0.8_m10080_net2_mo3_ba1000'
# title = r'(h) 50%, $(a,b)=(0.8,7T)$, $d=1/n$'
# Lplot(fn,title, vc=120, oname='10%-s08-d=n-1', gridon=1)
# fn ='2020-09-18_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d2_s0.8_m10080_net2_mo3_ba1000'
# title = r'(h) 10%, $(a,b)=(0.8,7T)$, $d=1/n$'
# Lplot(fn,title, vc=120, oname='10%-s08-d=n-1', gridon=1)
# fn ='2020-09-19_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d2_s0.8_m10080_net2_mo3_ba1000'
# title = r'(h) 2%, $(a,b)=(0.8,7T)$, $d=1/n$'
# Lplot(fn,title, vc=120, oname='2%-s08-d=n-1', gridon=1)
# fn ='2020-09-18_n800000_cn1_cs0_a0.5_b1_dlt0.0_on2_i100_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d2_s0.8_m10080_net2_mo3_ba1000'
# title = r'(h) 0%, $(a,b)=(0.8,7T)$, $d=1/n$'
# Lplot(fn,title, vc=120, oname='0%-s08-d=n-1', gridon=1)

# ##### a=0.9, lambda1=0.06
# fn ='2020-09-20_n800000_cn1_cs0_a0.9_b1_dlt0.0_on2_i50_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 50%, $\alpha_1=0.9$'
# Lplot(fn,title, vc=120, oname='50%-a0.9', gridon=1)
# fn ='2020-09-19_n800000_cn1_cs0_a0.9_b1_dlt0.0_on2_i90_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 90%, $\alpha_1=0.9$'
# Lplot(fn,title, vc=120, oname='90%-a0.9', gridon=1)
# fn ='2020-09-20_n800000_cn1_cs0_a0.9_b1_dlt0.0_on2_i98_c1000_f100_r10.06_r20.03_r30.02_p0_q0_d1_s1.2_m4320_net2_mo3_ba1000'
# title = r'(h) 2%, $\alpha_1=0.9$'
# Lplot(fn,title, vc=120, oname='2%-a0.9', gridon=1)




# ###################### Pokec #############
# fn ='2020-06-30_n1632803_cn20_cs0_a0.5_b0.5_dlt0.0_on2_i0_c1000_f200_r10.045_r20.035_r30.04_d1_s1.2_m4320_net4_mo1_ba1000'
# title = 'Pokec cn=20, more=1'
# Lplot(fn,title, vc=0)

# fn ='2020-09-22_n1632803_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.03_r20.03_r30.03_d1_s1.2_m4320_net4_mo0_ba1000'
# title = 'Pokec, no comm., $\lambda_0=0.03$'
# Lplot(fn,title, vc=100, oname='Pokec-r10.03')


# fn ='2020-09-22_n1632803_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.018_r20.018_r30.018_d1_s1.2_m4320_net4_mo0_ba1000'
# title = 'Pokec, no comm., $\lambda_0=0.018$'
# Lplot(fn,title, vc=0, gridon=1)
# fn ='2020-09-23_n1632803_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.017_r20.017_r30.017_d1_s1.2_m4320_net4_mo0_ba1000'
# title = 'Pokec, no comm., $\lambda_0=0.017$'
# Lplot(fn,title, vc=0, gridon=1)

# fn ='2020-09-24_n1632803_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.0175_r20.0175_r30.0175_d1_s1.2_m4320_net4_mo0_ba1000'
# title = 'Pokec, no comm., $\lambda_0=0.0175$'
# Lplot(fn,title, vc=0, oname='Pokec-r10.0175')

fn ='2020-09-24_n1632803_cn1_cs100_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.017_r20.017_r30.017_d1_s1.2_m4320_net4_mo0_ba1000'
title = r'(k) Pokec, $\alpha_1=NC$, $\lambda_0^1=0.017$'
Lplot(fn,title, vc=0, oname='Pokec-r10.017-cs100')

fn ='2020-09-25_n1632803_cn1_cs100_a1_b1_dlt0.0_on2_i0_c1000_f200_r10.03_r20.03_r30.03_d1_s1.2_m4320_net4_mo0_ba1000'
title = r'(l) Pokec, $\alpha_1=NC$, $\lambda_0^1=0.03$'
Lplot(fn,title, vc=0, oname='Pokec-r10.03-cs100')


# fn ='2020-10-05_n1632803_cn1_cs0_a0.1_b1_dlt0.0_on2_i0_c1000_f200_r10.025_r20.025_r30.025_d1_s1.2_m4320_net4_mo3_ba1000'
# title = '100%, Pokec cn=1'
# Lplot(fn,title, vc=200)
# fn ='2020-10-07_n1632803_cn1_cs0_a0.1_b1_dlt0.0_on2_i10_c1000_f200_r10.025_r20.025_r30.025_d1_s1.2_m4320_net4_mo3_ba1000'
# title = '90% Pokec cn=1'
# Lplot(fn,title, vc=200)
# fn ='2020-10-05_n1632803_cn1_cs0_a0.1_b1_dlt0.0_on2_i50_c1000_f200_r10.025_r20.025_r30.025_d1_s1.2_m4320_net4_mo3_ba1000'
# title = '50%, Pokec cn=1'
# Lplot(fn,title, vc=200)
# fn ='2020-10-06_n1632803_cn1_cs0_a0.1_b1_dlt0.0_on2_i90_c1000_f200_r10.025_r20.025_r30.025_d1_s1.2_m4320_net4_mo3_ba1000'
# title = '10%, Pokec cn=1'
# Lplot(fn,title, vc=200)
# fn ='2020-10-07_n1632803_cn1_cs0_a0.1_b1_dlt0.0_on2_i98_c1000_f200_r10.025_r20.025_r30.025_d1_s1.2_m4320_net4_mo3_ba1000'
# title = '2%, Pokec cn=1'
# Lplot(fn,title, vc=200)
# fn ='2020-10-07_n1632803_cn1_cs0_a0.1_b1_dlt0.0_on2_i100_c1000_f200_r10.025_r20.025_r30.025_d1_s1.2_m4320_net4_mo3_ba1000'
# title = '0%, Pokec cn=1'
# Lplot(fn,title, vc=200)





# ############## seed = None ################
# # fn ='2020-08-22_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba100'
# # title = r'(a) 0 comm., $\lambda_0=0.02, batch=100'
# # Lplot(fn,title, vc=0, oname='nc-l0.02-batch100')
# # fn ='2020-08-23_n800000_cn1_cs0_a1_b1_dlt0.0_on2_i0_c1000_f100_r10.02_r20.02_r30.02_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000'
# # title = r'(a) 0 comm., $\lambda_0=0.02, batch=1000$'
# # Lplot(fn,title, vc=0, oname='nc-l0.02-batch100')




def Prog2D(data, name, title, ylabel='$R^{120}_s$', ymin=-0.04, ymax=1.04, nonbipol=1):
     
    fig = plt.figure() 
    ri = [100, 90, 50, 10, 2, 0]
    # plt.xscale('log')
    # plt.yscale('log')
    plt.grid()

    # if nonbipol == 0:
    #     plt.plot(ri, data[0], marker="s", markersize=8, markeredgewidth=0.1, label="(A)", linewidth = 1.5, linestyle="solid")
    plt.plot(ri, data[1], marker="^", markersize=10, markeredgewidth=0.1, label="B", linewidth = 1.5, linestyle="solid")
    plt.plot(ri, data[2], marker="x", markersize=8, markeredgewidth=1, label="C", linewidth = 1.5, linestyle="dotted")
    plt.plot(ri, data[3], marker="x", markersize=8, markeredgewidth=1, label="D", linewidth = 1.5, linestyle="dotted")
    plt.plot(ri, data[4], marker="x", markersize=8, markeredgewidth=1, label="E", linewidth = 1.5, linestyle="dotted")
    plt.plot(ri, data[5], marker="x", markersize=8, markeredgewidth=1, label="F", linewidth = 1.5, linestyle="dotted")
    plt.plot(ri, data[6], marker="x", markersize=8, markeredgewidth=1, label="G", linewidth = 1.5, linestyle="dotted")
    plt.plot(ri, data[7], marker="x", markersize=8, markeredgewidth=1, label="H", linewidth = 1.5, linestyle="dashed")
    plt.plot(ri, data[8], marker="x", markersize=8, markeredgewidth=1, label="I", linewidth = 1.5, linestyle="dashed")
    plt.plot(ri, data[9], marker="^", markersize=10, markeredgewidth=0.1, label="J", linewidth = 1.5, linestyle="solid")

    
    plt.xlabel('$R_i$', fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    plt.ylim(ymin, ymax)
    # plt.xlim(xmin,xmax)
    plt.legend(loc='best', fontsize=14, ncol=3)
    plt.title(title, fontsize=20, pad=15)
    plt.tick_params(labelsize=14)
    plt.show()

    file = name +'.pdf'   
    pdf = PdfPages(file)
    pdf.savefig(fig,bbox_inches='tight')
    pdf.close()   
  
Rs = list()
# Rs.append([0.809, 0.761, 0.561, 0.165, 0.050, 0.024]) # A
# Rs.append([0.809, 0.761, 0.561, 0.165, 101/2000, 85/4000]) # A 4000samples
Rs.append([1, 1, 1, 1, 1, 1]) # A epsilon = 0
Rs.append([0.917, 0.909, 0.744, 0.301, 0.118, 0.066]) # B r1=r2=0.025
# Rs.append([0.868, 0.838, 0.648, 0.224, 0.077, 0.037]) # B a=0.5
Rs.append([0.997, 0.994, 0.968, 0.589, 0.330, 0.228]) # C
Rs.append([0.997, 0.994, 0.968, 0.585, 0.329, 0.227]) # D
Rs.append([0.997, 0.994, 0.972, 0.567, 0.337, 0.228]) # E
Rs.append([0.997, 0.994, 0.968, 0.589, 0.330, 0.228]) # F
Rs.append([0.997, 0.995, 0.959, 0.603, 0.339, 0.238]) # G
Rs.append([0.997, 0.994, 0.971, 0.566, 0.337, 0.237]) # H
Rs.append([0.950, 0.951, 0.784, 0.288, 0.095, 0.038]) ###  I d=5
Rs.append([0.976, 0.978, 0.893, 0.451, 0.226, 0.169]) ###  J
data = np.array(Rs)
Prog2D(data, name='succ-rate', title='(a) $R_i$ vs. $R^{120}_s$', nonbipol=1)

m60 = list()
# m60.append([1075,   1049,  1037,   973,   751,   945]) # A
# m60.append([1075,   1049,  1037,   973,   842.207921,   888.458824]) # A 4000samples
m60.append([871.924,   801.071,  585.732,   164.866,   41.107,   25.95]) # A epsilon = 0
m60.append([4012.339149,   4029.377338,  4034.228495,  4063.299003,  4069.415254,  4021.318182]) # B r1=r2=0.025
# m60.append([2009,   2014,  2018,  2025,  2051,  2045]) # B
m60.append([11602, 11621, 11587, 11636, 11610, 11621]) # C
m60.append([1495,   1490,  1498,  1512,  1508,  1542]) # D
m60.append([11603, 11619, 11597, 11610, 11599, 11689]) # E
m60.append([30083, 30098, 30090, 30114, 30128, 30164]) # F
m60.append([1481,   1486,  1503,  1526,  1537,  1531]) # G
m60.append([4873.219659,   4891.522133,  4894.056643,  4885.69788,  4894.919881,  4930.518987]) # H
m60.append([14780.175789,   14768.807571,  14770.409439,  14784.368056,  14760.252632,  14735.157895]) ###  I d=5
m60.append([9230.873975,   9243.317996,  9221.949608,  9297.492239,  9291.920354,  9203.621302]) ###  J
m = np.array(m60)
# print(np.mean(m, axis=0), np.mean(m, axis=1), np.mean(m, axis=1)[0])
data[0] = m[0]/np.mean(m, axis=1)[0]
data[1] = m[1]/np.mean(m, axis=1)[1]
data[2] = m[2]/np.mean(m, axis=1)[2]
data[3] = m[3]/np.mean(m, axis=1)[3]
data[4] = m[4]/np.mean(m, axis=1)[4]
data[5] = m[5]/np.mean(m, axis=1)[5]
data[6] = m[6]/np.mean(m, axis=1)[6]
data[7] = m[7]/np.mean(m, axis=1)[7]
data[8] = m[8]/np.mean(m, axis=1)[8]
data[9] = m[9]/np.mean(m, axis=1)[9]
Prog2D(data, name='mean', title=r'(b) $R_i$ vs. $\overline{m}^{120}$', ylabel=r'$\overline{m}^{120}$', ymin=0.9, ymax=1.15)

vc60 = list()
# vc60.append([0.580677, 0.612142, 0.608279, 0.750031, 0.917951, 0.818362]) # A
# vc60.append([0.580677, 0.612142, 0.608279, 0.750031, 0.817853, 0.824245]) # A 4000samples
vc60.append([0.580677, 0.612142, 0.608279, 0.750031, 0.817853, 0.824245]) # A epsilon = 0
vc60.append([0.087665, 0.089881, 0.085826,  0.08537, 0.096213, 0.089129]) # B r1=r2=0.025
# vc60.append([0.103296, 0.104864, 0.10867,  0.109865, 0.118313, 0.127632]) # B  a=0.5
vc60.append([0.044495, 0.043998, 0.045291, 0.044223, 0.042701, 0.043991]) # C
vc60.append([0.142525, 0.140832, 0.145464, 0.145096, 0.14548,  0.135798]) # D
vc60.append([0.043153, 0.042984, 0.043963, 0.046433, 0.042582, 0.043903]) # E
vc60.append([0.021225, 0.02019,  0.020709, 0.019869, 0.019248, 0.021085]) # F
vc60.append([0.14786, 0.145744, 0.142331, 0.140192, 0.140736, 0.149713]) # G
vc60.append([0.069244, 0.070861, 0.07171, 0.071482, 0.069607, 0.070032]) # H
vc60.append([0.026874, 0.026155, 0.02638, 0.027058, 0.024541, 0.029477]) ###  I d=5
vc60.append([0.057891, 0.059395, 0.059103, 0.057784, 0.054247, 0.060757]) ###  I
vc = np.array(vc60)
data[0] = vc[0]/np.mean(vc, axis=1)[0]
data[1] = vc[1]/np.mean(vc, axis=1)[1]
data[2] = vc[2]/np.mean(vc, axis=1)[2]
data[3] = vc[3]/np.mean(vc, axis=1)[3]
data[4] = vc[4]/np.mean(vc, axis=1)[4]
data[5] = vc[5]/np.mean(vc, axis=1)[5]
data[6] = vc[6]/np.mean(vc, axis=1)[6]
data[7] = vc[7]/np.mean(vc, axis=1)[7]
data[8] = vc[8]/np.mean(vc, axis=1)[8]
data[9] = vc[9]/np.mean(vc, axis=1)[9]
Prog2D(data, name='vc10', title='(c) $R_i$ vs. $\overline{VC}^{120}$', ylabel=r'$\overline{VC}^{120}$', ymin=0.8, ymax=1.3)



