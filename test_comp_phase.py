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


def phase(HJD, P=5.732436, T0 = 2457733.8493):
  phi = ((HJD-T0)/P)%1.
  return phi


class Myphoebe2(Myphoebe):
  '''
  A minor modification of Myphoebe (inherited form).

  '''

  def chi2_contrib(self, ids, dataset):
    '''
    Print chi2 for each dataset.

    '''
    
    print('chi2 from dataset', dataset, '=', "{:19.10f}".format(np.sum(self.chi[ids])))


  def plot_forward_model_phase_com(self, output='test_comp_phase.png', dpi=600):
    '''
    Plot model from PHOEBE 2 variables.

    '''

    fig, (ax1, ax2) = plt.subplots(figsize = (10,10), nrows=2, ncols=1)

    fig.suptitle(r'$\chi^2$', fontsize=cfg._sections['general'].get('text_title'))

    s         = float(cfg._sections['styles'].get('marker_size'))
    lw        = float(cfg._sections['styles'].get('syn_lw'))
    res_lw    = float(cfg._sections['styles'].get('res_lw'))
    cs        = float(cfg._sections['styles'].get('capsize'))
    marker    = cfg._sections['styles'].get('marker_type')
    capsize   = float(cfg._sections['styles'].get('capsize'))
    err_thick = float(cfg._sections['styles'].get('err_thick'))
     
    ids = np.where(self.dataset==1)

    ax1.scatter(phase(self.x[ids]), self.ysyn[ids], color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw, label='BRITE - sythetic')
    for i in ids:
      ax1.plot([phase(self.x[i]), phase(self.x[i])], [self.yobs[i], self.ysyn[i]], color=cfg._sections['colors'].get('b_rv1'), lw=res_lw, zorder=4)
    ax1.errorbar(phase(self.x[ids]), self.yobs[ids], self.yerr[ids], color=cfg._sections['colors'].get('obs_blue'), lw=lw, fmt='none', label='BRITE blue - observed', capsize=capsize, elinewidth=err_thick, capthick=err_thick)
    
    self.chi2_contrib(ids, 1)
    
    max_lcB_F, min_lcB_F = max(np.r_[self.yobs[ids], self.ysyn[ids]]), min(np.r_[self.yobs[ids], self.ysyn[ids]])


    ids = np.where(self.dataset==2)

    ax1.scatter(phase(self.x[ids]), self.ysyn[ids], color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw)
    for i in ids:
      ax1.plot([phase(self.x[i]), phase(self.x[i])], [self.yobs[i], self.ysyn[i]], color=cfg._sections['colors'].get('r_rv2'), lw=res_lw, zorder=4)
    ax1.errorbar(phase(self.x[ids]), self.yobs[ids], self.yerr[ids], color=cfg._sections['colors'].get('obs_red'), lw=lw, fmt='none', label='BRITE red - observed', capsize=capsize, elinewidth=err_thick, capthick=err_thick)

    ax1.set_xlabel(r'$\varphi$', labelpad=10)
    ax1.set_ylabel(r'$F$ [1]', labelpad=15)
    ax1.legend(loc='lower left', ncol=3, fontsize=cfg._sections['general'].get('text_legend'))

    self.chi2_contrib(ids, 2)

    ax1.set_xlim(-0.02, 1.02)

    max_lcR_F, min_lcR_F = max(np.r_[self.yobs[ids], self.ysyn[ids]]), min(np.r_[self.yobs[ids], self.ysyn[ids]])

    # marigns
    min_F = min(min_lcB_F, min_lcR_F)
    max_F = max(max_lcB_F, max_lcR_F)
    ax1.set_ylim(min_F-0.15*(max_F-min_F), max_F+0.04*(max_F-min_F))


    ids = np.where(self.dataset==3)

    ax2.scatter(phase(self.x[ids]), self.ysyn[ids], color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw, label=r'RV - sythetic')
    for i in ids:
      ax2.plot([phase(self.x[i]), phase(self.x[i])], [self.yobs[i], self.ysyn[i]], color=cfg._sections['colors'].get('b_rv1'), lw=res_lw, zorder=4)
    ax2.errorbar(phase(self.x[ids]), self.yobs[ids], self.yerr[ids], color=cfg._sections['colors'].get('obs_rv1'), fmt='none', label='RV$_1$ - observed', capsize=capsize, elinewidth=err_thick, capthick=err_thick)

    self.chi2_contrib(ids, 3)   

    ids = np.where(self.dataset==4)

    ax2.scatter(phase(self.x[ids]), self.ysyn[ids], color=cfg._sections['colors'].get('syn'), marker=marker, s=s, lw=lw)
    for i in ids:
      ax2.plot([phase(self.x[i]), phase(self.x[i])], [self.yobs[i], self.ysyn[i]], lw=res_lw, zorder=4, color=cfg._sections['colors'].get('r_rv2'))
    ax2.errorbar(phase(self.x[ids]), self.yobs[ids], self.yerr[ids], color=cfg._sections['colors'].get('obs_rv2'), fmt='none', label='RV$_2$ - observed', capsize=capsize, elinewidth=err_thick, capthick=err_thick)

    self.chi2_contrib(ids, 4)
    
    ax2.plot([-0.02, 1.02], [0, 0], c = cfg._sections['colors'].get('rv0'), lw=2*lw)

    ax2.set_xlabel(r'$\varphi$', labelpad=10)
    ax2.set_ylabel(r'RV [km/s]', labelpad=10)
    ax2.legend(loc='lower left', ncol=3, fontsize=cfg._sections['general'].get('text_legend'))
    ax2.set_xlim(-0.02, 1.02)
    ax2.set_ylim(-400,400)
    
    plt.tight_layout()
    plt.savefig(output, dpi=dpi)


def main():
  '''
  Main program.

  '''

  myphoebe = Myphoebe2()

  theta = myphoebe.initial_parameters()

  myphoebe.chi2(theta)

  myphoebe.plot_forward_model_phase_com()
   

if __name__ == "__main__":
  main()

