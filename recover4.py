from ROOT import *
from os import mkdir, chdir
import multiprocessing
from cc_ana_tool import *

pi = TMath.Pi()

l_pt ="40"

mass_cut = "(raw_mass > 220)"

low_eta_cut = " * (abs(jet_eta[1]) < 0.8)"
high_eta_cut = " * (0.8 < abs(jet_eta[1])) * ((abs(jet_eta[1]) < 2.5))"
eta_cut = " * (abs(jet_eta) < 2.5)"

high_pt_cut = " * (507 < jet_pt[0]) * (hlt320 == 1)"
middle_pt_cut = " * (220 < jet_pt[0] && jet_pt[0] < 507) * (hlt140 == 1)"
low_pt_cut = " * (74 < jet_pt[0] && jet_pt[0] < 220) *  (hlt%s == 1)"%l_pt

r23_min = " * (0.5 < del_r[1])"
r23_15 = " * (del_r[1] < 1.5)"
r23_no = " * (1.5 < del_r[1])"

b_cut = mass_cut + r23_min + eta_cut + low_eta_cut
e_cut = mass_cut + r23_min + eta_cut + high_eta_cut

data_root = "Beta_data.root"
tf = TFile(data_root)
tr = tf.Get("beta")

data_root_jec = "Beta_data_jec.root"
tf_jec = TFile(data_root_jec)
tr_jec = tf_jec.Get("beta")

mc_root_p = "Beta_mc_p.root"
tf_mc_p = TFile(mc_root_p)
tr_mc_p = tf_mc_p.Get("beta")

mc_root_h = "Beta_mc_h.root"
tf_mc_h = TFile(mc_root_h)
tr_mc_h = tf_mc_h.Get("beta")


eta_cut = [b_cut, e_cut]
pt_cut = [high_pt_cut, middle_pt_cut, low_pt_cut]
r23_cut = [r23_15, r23_no]

set_results = hist_setter(tr_jec, eta_cut, pt_cut, r23_cut)

if __name__ == '__main__':
  root_f = ["hist_data_jec.root", "hist_data.root", "hist_mc_p.root", "hist_mc_h.root"]
  tr_l = [tr_jec, tr, tr_mc_p, tr_mc_h]
  jobs = []
  for i in xrange(3):
    p = multiprocessing.Process(target=make_hist,args=(root_f[i],tr_l[i],set_results,))
    jobs.append(p)
    p.start()


#make_hist("hist_data.root", tr, set_results)
#make_hist("hist_mc_p.root", tr_mc_p, set_results)
#make_hist("hist_mc_h.root", tr_mc_h, set_results)

