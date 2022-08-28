#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def CriticalStateFunction(mu=0.6):
    return (np.sqrt(mu**2 + 1) + mu)**2


# In[3]:


def StressPolygon(Sv, Pp, mu=0.6, figsize=[8, 8]):
    f_mu = CriticalStateFunction(mu)
    1/f_mu * Sv + (1-1/f_mu)*Pp
    Svline = np.array([0, 4*Sv])
    Sh = np.array([0, 4*Sv])
    # Normal Fault Triangle
    Sh_lowbnd_n = 1/f_mu * Sv + (1-1/f_mu)*Pp
    SH_upbnd_n = Sv
    
    # Strik Slip Fault Triangle
    SH_lowbnd_ss = Sv
    SH_upbnd_ss = f_mu*np.array([Sh_lowbnd_n, Sv]) + (1-f_mu)*Pp
    Sh_upbnd_ss = Sv
    
    # Reverse Fault Triangle
    Sh_lowbnd_r = Sv
    SH_upbnd_r = f_mu*Sv + (1-f_mu)*Pp
    
    # Create Figure
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle('Bounds of SH & Sh')
    ax.plot(Sh, Svline, color='blue')
    
    # Plot Normal Fault Triangle
    ax.vlines(Sh_lowbnd_n, Sh_lowbnd_n, Sv, color='blue')
    ax.hlines(SH_upbnd_n, Sh_lowbnd_n, Sv, color='blue')
    normal = ax.fill_between([Sh_lowbnd_n, Sv], y1=[Sv, Sv], y2=[Sh_lowbnd_n, Sv], alpha=0.3, color='red')
    
    # Plot Strike Slip Fault Triangle
    ax.plot([Sh_lowbnd_n, Sv], SH_upbnd_ss, color='blue')
    ax.vlines(Sv, Sv, SH_upbnd_ss[-1], color='blue')
    strikeslip = ax.fill_between([Sh_lowbnd_n, Sv], y1=SH_upbnd_ss, y2=[Sv, Sv], alpha=0.3, color='green')
    
    # Plot Reverse Fault Triangle
    plt.hlines(SH_upbnd_r, Sv, SH_upbnd_r, color='blue')
    reverse = ax.fill_between([Sv, SH_upbnd_r], y1=[SH_upbnd_r, SH_upbnd_r], y2=[Sv, SH_upbnd_r], alpha=0.3, color='orange')
    
    ax.grid()
    ax.set_title(f'Sv={Sv} & Pp={Pp}')
    ax.set_xlabel('Sh')
    ax.set_ylabel('SH')
    
    ax.set_xlim(0, 1.1*SH_upbnd_r)
    ax.set_ylim(0, 1.1*SH_upbnd_r)
    
    legend1 = ax.legend(handles=[normal, strikeslip, reverse], 
                        labels=['Normal Falut', 'Strike Slip Fault', 'Reverse Fault'], 
                        loc='lower right')
    
    ax.add_artist(legend1)

    return ax


# In[4]:


def StressPolygonAdjusted(Sv, Pp, Pm, C0, wbo, mu=0.6, figsize=[8, 8], T0=0, sigmaT=0):
    ax = StressPolygon(Sv, Pp, figsize=figsize, mu=mu)
    
    f_mu = CriticalStateFunction(mu)
    lb = 1/f_mu * Sv + (1-1/f_mu)*Pp
    x = np.linspace(0.9*lb, 1.2*Sv, 2)
    
    y = 3*x - 2*Pp - (Pm-Pp) + T0 - sigmaT      
    ax.plot(x, y, label=f'(Pm-Pp)={Pm-Pp}')
    
    
    tb = np.deg2rad(90-wbo/2)
    x2 = np.linspace(0.9*lb, 0.9*ax.get_xlim()[1])
    
    def helper(co):
        y2 = (co + 2*Pp + (Pm-Pp) + sigmaT)/(1-2*np.cos(2*tb)) - (1+2*np.cos(2*tb))/(1-2*np.cos(2*tb)) * x2
        ax.plot(x2, y2, label=f'Wbo={wbo} Co={co}')
        
    try:
        for co in C0:
            helper(co)
    except:
        helper(C0)  
    
    legend2 = ax.legend(loc='upper left')
    ax.add_artist(legend2)
    
    return ax

# In[ ]:




