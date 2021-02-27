# bi-polar

Simulation Programs for Python 3.7:

1. snet_2com_weight_init_more_start_rate_sin.py: 
    a simulation program for all results in the paper
    
2. data-repeat3_alpha.py: 
    a simulation execution program for SW, SF, and ER graphs.
    
3. data-repeat4_alpha.py: 
    a simulation execution program for Pokec.
    soc-pokec-relationships.txt (https://snap.stanford.edu/data/soc-Pokec.html) must be in the same folder.

4. plot-data.py: 
    a program that inputs a simulation output (numpy data) and outputs a histogram in Fig. 3 in the paper (a pdf file).

Output of data-repeat3_alpha.py:
 
1. 2021-02-10_n800000_cn20_cs0_a0.2_b0.5_dlt0.0_on2_i0_c1000_f100_r10.03_r20.03_r30.03_p0_q0_d1_s1.2_m4320_net2_mo2_ba1000.npy

    simulation start: Feb. 10, 2021
    n: net_size=800,000     <------- network size (N)
    cn: comm_num=20         <------- number of communities (N_c)
    cs: comm_strt=0         <------- offset added to user id
    a: alpha=0.2            <------- cohesion of community 1, alpha=1 implies alpha_1=NC
    b: beta=0.5             <------- cohesion of community >1, beta=1 implies alpha_>1=NC
    dlt: delta=0.0          <------- size of order-dependent fluctuations in retweet prob (delta_1)
    on: comm_on=2           <------- place where fluctuations occur, comm_on=2 implies everywhere
    i: init_out=0           <------- number of initiator's followers who are not community 1 members (R_i=100*(f-init_out)/f)
    cs: comm_size=1000      <------- community size (C)
    f: fw_size=100          <------- number of initiator's followers (F_0)
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
    ba: batch_size=1000     <------- number of samples

Outputs of plot-data.py:
    nc-l0.02.pdf            <------- Fig. 3(a)
    20comm-l0.03.pdf        <------- Fig. 3(b)
    Pokec-r0.017_cs100.pdf  <------- Fig. 3(k)
    Pokec-r0.03_cs100.pdf   <------- Fig. 3(l)
    