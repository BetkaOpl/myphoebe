#!/usr/bin/env python3
# coding: utf-8

import matplotlib.pyplot as plt

from myphoebe import *

# Configuration file
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('setting.cfg')

params = {
        'text.usetex' : True,
        'font.size'   : cfg._sections['general'].get('text_rest'),
        'font.family' : 'lmodern',
        }
plt.rcParams.update(params)


class Myphoebe2(Myphoebe):
  '''
  A minor modification of Myphoebe (inherited from).

  '''

  def plot_forward_model(self, output='test_forw_T.png', dpi=600):
    '''
    Plot model from Phoebe2 variables.

    '''

    fig, (ax1, ax2) = plt.subplots(figsize = (10,10), nrows=2, ncols=1)

    fig.suptitle(r'Forward model', fontsize=cfg._sections['general'].get('text_title'))

    s  = float(cfg._sections['styles'].get('marker_size'))
    lw = float(cfg._sections['styles'].get('syn_lw'))
    marker = cfg._sections['styles'].get('marker_type')

    ax1.scatter(self.b['times@lcB@latest@model'].value-2400000, self.b['fluxes@lcB@latest@model'].value, color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw)
    ax1.scatter(self.b['times@lcR@latest@model'].value-2400000, self.b['fluxes@lcR@latest@model'].value, color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw)
    ax1.plot(self.b['times@lcB@latest@model'].value-2400000, self.b['fluxes@lcB@latest@model'].value, label='LC BRITE blue', color=cfg._sections['colors'].get('obs_blue'), lw=lw)
    ax1.plot(self.b['times@lcR@latest@model'].value-2400000, self.b['fluxes@lcR@latest@model'].value, label='LC BRITE red', color=cfg._sections['colors'].get('obs_red'), lw=lw)

    ax1.set_xlabel(r'$t$ [HJD-2400000]', labelpad=10)
    ax1.set_ylabel(r'$F$ [1]', labelpad=15)
    ax1.legend(loc='lower left', ncol=2, fontsize=cfg._sections['general'].get('text_legend'))

    # marigns
    lc_t = np.r_[self.b['times@lcB@latest@model'].value-2400000, self.b['times@lcR@latest@model'].value-2400000]
    lc_f = np.r_[self.b['fluxes@lcB@latest@model'].value, self.b['fluxes@lcR@latest@model'].value]
    ax1.set_xlim(min(lc_t)-0.04*(max(lc_t)-min(lc_t)), max(lc_t)+0.04*(max(lc_t)-min(lc_t)))
    ax1.set_ylim(min(lc_f)-0.15*(max(lc_f)-min(lc_f)), max(lc_f)+0.04*(max(lc_f)-min(lc_f)))

    ax2.scatter(self.b['times@primary@rv1@latest@model'].value-2400000, self.b['rvs@primary@rv1@latest@model'].value, color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw)
    ax2.scatter(self.b['times@secondary@rv2@latest@model'].value-2400000, self.b['rvs@secondary@rv2@latest@model'].value, color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw)
    ax2.plot(self.b['times@primary@rv1@latest@model'].value-2400000, self.b['rvs@primary@rv1@latest@model'].value, color=cfg._sections['colors'].get('obs_rv1'), label='RV primary', lw=lw)
    ax2.plot(self.b['times@secondary@rv2@latest@model'].value-2400000, self.b['rvs@secondary@rv2@latest@model'].value, color=cfg._sections['colors'].get('obs_rv2'), label='RV secondary', lw=lw)
    ax2.plot([53800,59000], [0, 0], c = cfg._sections['colors'].get('rv0'), lw=2*lw)

    ax2.set_xlabel(r'$t$ [HJD-2400000]', labelpad=10)
    ax2.set_ylabel(r'RV [km/s]', labelpad=10)
    ax2.legend(loc='lower left', ncol=2, fontsize=cfg._sections['general'].get('text_legend'))
    ax2.set_xlim(53800,59000)
    ax2.set_ylim(-400,400)

    plt.tight_layout()
    plt.savefig(output, dpi=dpi)



def main():
  '''
  Main program.

  '''

  myphoebe = Myphoebe2()

  theta = myphoebe.initial_parameters()

  myphoebe.model(theta)
  myphoebe.plot_forward_model()
   

if __name__ == "__main__":
  main()

