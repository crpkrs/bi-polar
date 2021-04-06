
Bi-polarization in Cascade Size Distributions

Simulation Programs for Python 3.7 and Mathematica program for the recurrence relation:

1. snet_2com_weight_init_more_start_rate_sin.py: 
    a simulation program for all results in the paper
    
2. data-repeat3_alpha.py: 
    a simulation execution program for the SW, SF, and ER graphs.
    
3. data-repeat4_alpha.py: 
    a simulation execution program for the Pokec graph.
    soc-pokec-relationships.txt (https://snap.stanford.edu/data/soc-Pokec.html) must be in the same folder.
    
4. data-repeat-rewire_alpha.py:
    a simulation execution program extended for random community sizes and rewiring of links

5. plot-data.py: 
    a program that outputs a histogram in Fig. 3 and Table 2 (a pdf file) using simulation output data (numpy data).

Output of data-repeat-rewire_alpha.py:
 
1. 2021-03-30_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_c2100_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000_rw0.01.npy

    simulation start: Mar. 30, 2021
    
    n: net_size=800000      <------- network size (N)
    
    cn: comm_num=20         <------- number of communities (N_c)
    
    cs: comm_strt=0         <------- offset added to user id
    
    a: alpha=0.2            <------- cohesion index of community 1, alpha=1 implies alpha_1=NC
    
    b: beta=0.5             <------- cohesion indexes of community >1, beta=1 implies alpha_>1=NC
    
    dlt: delta=0.0          <------- size of order-dependent fluctuations in retweet prob (delta_1)
    
    on: comm_on=2           <------- place where fluctuations occur, comm_on=2 implies everywhere
    
    i: init_out=0           <------- number of initiator's followers not belonging to community 1 (R_i=100*(f-i)/f)
    
    c: comm_size=1000       <------- size of community 1 (C) 
    
    c2: comm_size2=100      <------- sizes of community >1 has a distribution U(c2,c), c2=0 implies they are fixed at c
    
    f: fw_size=100          <------- number of initiator's followers (F_0), F_0 = F (mean number of followers) for SW and ER
    
    r1: rtrate_com=0.03     <------- retweet rate of community 1 members (lambda_1)
    
    r2: rtrate_oth=0.03     <------- retweet rate of users not belonging to any community (lambda_0)
    
    r3: rtrate_ocom=0.03    <------- retweet rate of community >1 members (lambda_>1)
    
    p: p=0                  <------- parameter of SF and SW (p=0.01 for SW, p=0 for SF)
    
    q: q=0                  <------- parameter of SF (q=0 for SF)
    
    d: dcnt=1               <------- weight func, 0: independent, 1: 0.9^n-1, 2: 1/n, 3: linear, 4: [n=1], 5: social reinf
    
    s: shape=1.2            <------- shape of truncated Pareto (a)
    
    m: maxday=4320          <------- scale of truncated Pareto (b)
    
    net: netprop=2          <------- graph type, 0: ER, 1: SW, 2: SF, >2: Pokec
    
    mo: more=2              <------- method of selecting initiator's followers
    
    ba: batch_size=1000     <------- number of samples to calculate statistics or a histogram
    
    rw: rate_rewire=0.01    <------- rate of links rewired uniformly at random

Outputs of plot-data.py:

    nc-l0.02.pdf            <------- Fig. 3(a)
    
    20comm-l0.03.pdf        <------- Fig. 3(b)
    
    Pokec-r0.017_cs100.pdf  <------- Fig. 3(k)
    
    Pokec-r0.03_cs100.pdf   <------- Fig. 3(l)
    
    20comm-l0.03-rc-rw.pdf  <------- Fig. 3(m)
    
    SW-20comm-l0.04-rc-rw.pdf <------- Fig. 3(n)
    
    20comm-l0.03-rc.pdf     <------- Table 2, |C_i|~U(100,1000), r_w=0%
    
    20comm-l0.03-rw.pdf     <------- Table 2, |C_i|=1000, r_w=1%
    
A Mathematica program for the recurrence relation model: drawing-balls-urn.nb


    
    