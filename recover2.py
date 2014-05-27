from ROOT import *
import sys
from math import sqrt
import os

### Const.
pi = TMath.Pi()

### Beta
def cal_del_eta(eta1, eta2):
  diff = eta2 - eta1
  eta1_sign = TMath.Sign(1.0, eta1)
  return eta1_sign*diff

def cal_del_phi(phi1, phi2):
  diff = phi2 - phi1
  if(diff > pi):
    return diff - 2. * pi
  elif(diff < -pi):
    return diff + 2. * pi
  else:
    return diff

def cal_beta(eta1, phi1, eta2, phi2):
  del_eta = cal_del_eta(eta1, eta2)
  del_phi = cal_del_phi(phi1, phi2)
  del_r = sqrt(del_eta**2 + del_phi**2)
  beta = TMath.ATan2(del_phi, del_eta)
  return [beta, del_eta, del_phi, del_r]

def loose_id(pfchf, pfnhf, pfcem, pfnem, pfcml):
  if pfchf > 0 and pfnhf < 0.99 and pfcem < 0.99 and pfnem < 0.99 and pfcml >0:
    return 1
  else:
    return -1

###
def list_root_file(path):
  ls = os.listdir(path)
  flist = []
  for x in ls:
    if x.endswith(".root"):
      flist.append(path+x)
  return flist

### Hist.

# e.g. hist_maker("beta", "title", [30, 0, pi], "#beta", "count", tr, br, cut, 2, 0)
def hist_maker(name, title, bin_set, x_name, y_name, tr, br, cut):
  hist = TH1F(name, title, bin_set[0], bin_set[1], bin_set[2])
  hist.GetXaxis().SetTitle(x_name)
  hist.GetYaxis().SetTitle(y_name)
  #hist.SetLineColor(color)
  hist.SetLineWidth(1)
  #hist.SetStats(0)
  tr.Project(name, br, cut)
  return hist

def bin_mod(br, name_tag, tr, cut):
  tr.Draw(br+">>h_"+name_tag, cut)
  tmp = gDirectory.Get("h_"+name_tag)
  bin_max = tmp.GetXaxis().GetXmax()
  bin_min = tmp.GetXaxis().GetXmin()
  bin_d = bin_max - bin_min
  if bin_d >100:
    return [100, bin_min, bin_max]
  else:
    return [50, bin_min, bin_max]


def hist_setter(tr, eta_cut, pt_cut, r23_cut):

  hist_val = ["beta", "del_eta", "del_phi", "del_r", "raw_mass", "jet_pt", "jet_eta", "jet_phi", "jet_mass"]
  hist_log = [0, 0, 0, 0, 1, 1, 0, 0, 1]
  x_n = ["#beta", "#Delta #eta", "#Delta #phi", "#Delta R", "Raw mass [GeV/c^{2}]", "p_{T} [GeV/c]", "#eta", "#phi", "Jet mass [GeV/c^{2}]"]
  y_n = "count"
  bin = [[30, 0, pi], [40, -2, 2], [40, -2, 2], [30, 0, 3], [100, 0, 4000], [100, 0, 2500], [60, -3, 3], [60, -pi, pi], [100, 0, 600]]

  hist_eta_cut = ["b_", "e_"]
  hist_pt_cut = ["h_", "m_", "l_"]
  hist_r23_cut = ["r15", "nor"]

  hist_title_h = ["Hight pt ", "Middle pt ", "Low pt "]
  hist_title_b = ["#beta", "#Delta #eta", "#Delta #phi", "#Delta R", "Raw mass", "Jet %d p_{T}", "Jet %d #eta", "Jet %d #phi", "Jet %d mass"]
  hist_title_t = ["(jet2 #eta < 0.8, ", "(0.8 < jet2 #eta < 2.5, "]
  hist_title_t2 = ["0.5 < r23 < 1.5)", "1.5 < r23)"]

  hist_name = []
  hist_title = []
  hist_bin_set = []
  hist_x_name = []
  hist_y_name = []
  hist_cut = []
  hist_br = []
  
  index_c = [0, 2, 3, 1]
  for e_i, e in enumerate(eta_cut):
    for p_i, p in enumerate(pt_cut):
      for r_i, r in enumerate(r23_cut):
        for j in [1, 2, 3]:
          for v_i, v in enumerate(hist_val):
            hist_name.append(v + "_%d_"%j + "log_%d_"%hist_log[v_i] + "cut_" + hist_eta_cut[e_i] + hist_pt_cut[p_i] + hist_r23_cut[r_i])
            if  v.startswith("beta"):
              hist_br.append("abs(%s[%d])"%(v,j-1))
            else:
              hist_br.append(v+"[%d]"%(j-1))
            hist_cut.append(e + p + r)
            if hist_title_b[v_i].startswith("Jet"):
              hist_title.append(hist_title_h[p_i] + hist_title_b[v_i]%j + hist_title_t[e_i] + hist_title_t2[r_i])
            else:
              hist_title.append(hist_title_h[p_i] + hist_title_b[v_i]+ "%d%d"%(j,index_c[j]) + hist_title_t[e_i] + hist_title_t2[r_i])
            if hist_log[v_i] == 1:
              tmp_br = v + "[%d]"%(j-1)
              tmp_name = v + "%d_"%j + hist_eta_cut[e_i] + hist_pt_cut[p_i] + hist_r23_cut[r_i]
              tmp_cut = e + p + r
              hist_bin_set.append(bin_mod(tmp_br, tmp_name, tr, tmp_cut))
            elif v.startswith("del_eta") and j != 2:
              hist_bin_set.append([100,-5, 5])
            elif v.startswith("del_phi") and j != 2:
              hist_bin_set.append([60, -pi, pi])
            else: 
              hist_bin_set.append(bin[v_i])
            hist_x_name.append(x_n[v_i])
            hist_y_name.append(y_n)
  hist_name.append("met")
  hist_title.append("Missing e_{T}")
  hist_bin_set.append(bin_mod("met", "missing_et", tr, "1"))
  hist_x_name.append("Missing e_{T} [GeV]")
  hist_y_name.append("count")
  hist_cut.append("1")
  hist_br.append("met")

  hist_name.append("njet")
  hist_title.append("Number of jet p_{T} > 25 GeV/c")
  hist_bin_set.append([100 ,0 ,100])
  hist_x_name.append("Number of jet/event")
  hist_y_name.append("count")
  hist_cut.append("1")
  hist_br.append("njet")

  hist_name.append("nvtx")
  hist_title.append("Number of vertex")
  hist_bin_set.append([100, 0, 100])
  hist_x_name.append("Number of vertex/event")
  hist_y_name.append("count")
  hist_cut.append("1")
  hist_br.append("nvtx")

  return hist_name, hist_title, hist_bin_set, hist_x_name, hist_y_name, hist_br, hist_cut

def make_hist(out_root, tr, set_results):
  tf = TFile(out_root, "RECREATE")
  hist = []
  for i in xrange(len(set_results[0])):
    hist.append(hist_maker(set_results[0][i], set_results[1][i], set_results[2][i], set_results[3][i], set_results[4][i], tr, set_results[5][i], set_results[6][i]))
  tf.Write()
  tf.Close()
  

