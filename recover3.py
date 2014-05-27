from cc_ana_tool import *
from ROOT import *
from array import array
from time import gmtime, strftime
from os import mkdir, chdir, system
from sys import argv

open_dir = "./"+argv[1]+"/"
print open_dir
root_f = list_root_file(open_dir)

dname = "Beta_"+argv[1]+strftime("_%d%b%Y_%H:%M:%S", gmtime())
mkdir(dname)

tf_out = TFile(dname+"/beta.root","RECREATE")
tr_out_beta = TTree("beta", "beta distribution")

br_beta = array('f', [0, 0, 0])
br_del_eta = array('f', [0, 0 ,0])
br_del_phi = array('f', [0, 0, 0])
br_del_r = array('f', [0, 0, 0])
br_raw_mass = array('f', [0, 0, 0])

br_jet_pt= array('f', [0, 0, 0])
br_jet_eta = array('f', [0, 0, 0])
br_jet_phi = array('f', [0, 0, 0])
br_jet_mass = array('f', [0, 0, 0])
br_jet_btag = array('f', [0, 0, 0])
br_jet_pileup = array('f', [0, 0, 0])

br_hlt40 = array('f', [0])
br_hlt80 = array('f', [0])
br_hlt140 = array('f', [0])
br_hlt200 = array('f', [0])
br_hlt260 = array('f', [0])
br_hlt320 = array('f', [0])

br_hlt40_hpre = array('f', [0])
br_hlt80_hpre = array('f', [0])
br_hlt140_hpre = array('f', [0])
br_hlt200_hpre = array('f', [0])
br_hlt260_hpre = array('f', [0])
br_hlt320_hpre = array('f', [0])

br_hlt40_lpre = array('f', [0])
br_hlt80_lpre = array('f', [0])
br_hlt140_lpre = array('f', [0])
br_hlt200_lpre = array('f', [0])
br_hlt260_lpre = array('f', [0])
br_hlt320_lpre = array('f', [0])

br_njet = array('f', [0])
br_met = array('f', [0])
br_nvtx = array('f', [0])
br_pileup = array('f', [0])

br_b = [br_beta, br_del_eta, br_del_phi, br_del_r, br_raw_mass, br_jet_pt, br_jet_eta, br_jet_phi, br_jet_mass, br_jet_btag, br_jet_pileup, br_hlt40, br_hlt80, br_hlt140, br_hlt200, br_hlt260, br_hlt320, br_hlt40_hpre, br_hlt80_hpre, br_hlt140_hpre, br_hlt200_hpre, br_hlt260_hpre, br_hlt320_hpre, br_hlt40_lpre, br_hlt80_lpre, br_hlt140_lpre, br_hlt200_lpre, br_hlt260_lpre, br_hlt320_lpre, br_njet, br_met, br_nvtx, br_pileup]
br_s = ["beta", "del_eta", "del_phi", "del_r", "raw_mass", "jet_pt", "jet_eta", "jet_phi", "jet_mass", "jet_btag", "jet_pileup", "hlt40", "hlt80", "hlt140", "hlt200", "hlt260", "hlt320", "hlt40_hpre", "hlt80_hpre", "hlt140_hpre", "hlt200_hpre", "hlt260_hpre", "hlt320_hpre", "hlt40_lpre", "hlt80_lpre", "hlt140_lpre", "hlt200_lpre", "hlt260_lpre", "hlt320_lpre", "njet", "met", "nvtx", "pileup"]
br_s2 = ["beta[3]", "del_eta[3]", "del_phi[3]", "del_r[3]", "raw_mass[3]", "jet_pt[3]", "jet_eta[3]", "jet_phi[3]", "jet_mass[3]", "jet_btag[3]", "jet_pileup[3]", "hlt40", "hlt80", "hlt140", "hlt200", "hlt260", "hlt320", "hlt40_hpre", "hlt80_hpre", "hlt140_hpre", "hlt200_hpre", "hlt260_hpre", "hlt320_hpre", "hlt40_lpre", "hlt80_lpre", "hlt140_lpre", "hlt200_lpre", "hlt260_lpre", "hlt320_lpre", "njet", "met", "nvtx", "pileup"]

for x in xrange(len(br_s)):
  tr_out_beta.Branch(br_s[x], br_b[x], br_s2[x])

pt_cut = 25.0

hlt_name = ["HLT_PFJet320", "HLT_PFJet260", "HLT_PFJet200", "HLT_PFJet140", "HLT_PFJet80", "HLT_PFJet40"]

hlt_br = [br_hlt320, br_hlt260, br_hlt200, br_hlt140, br_hlt80, br_hlt40]
hpre_br = [br_hlt320_hpre, br_hlt260_hpre, br_hlt200_hpre, br_hlt140_hpre, br_hlt80_hpre, br_hlt40_hpre]
lpre_br = [br_hlt320_lpre, br_hlt260_lpre, br_hlt200_lpre, br_hlt140_lpre, br_hlt80_lpre, br_hlt40_lpre]

selected_events = 0
tot_events = 0
file_num = 0
for f in root_f:
  file_num = file_num + 1
  tf = TFile(f)
  td = tf.Get("ak5calo")
  tr = td.Get("InclusiveJetTree")
  print "Open file : "+f
  tot_events = tot_events + tr.GetEntries()
  count_ev = 0
  for ev in tr:
    count_ev = count_ev + 1
    if divmod(count_ev, 10000)[1] == 1:
      print "Event : %ist evetnt started, %i events are left, %2.1f %% is done of file : "%(count_ev, tot_events - count_ev, float(count_ev)/float(tot_events)*100.0)+f,"  ",file_num,"/",len(root_f)


    pt  = ev.pfpt
    eta = ev.pfeta
    phi = ev.pfphi
    e   = ev.pfe
    met = ev.met

    if(len(pt) < 3):
      continue
    if(pt[0] < pt[1]):
      print "Jet pT sorting is wrong!"
      break
    if(pt[2] < pt_cut):
      continue

    chf = ev.pfchf
    nhf = ev.pfnhf
    cem = ev.pfcem
    nem = ev.pfnem
    cml = ev.pfcml
    loose_jet_id_cut = 0
    for j in xrange(3):
      loose_jet_id_cut = loose_jet_id_cut + loose_id(chf[j], nhf[j], cem[j], nem[j], cml[j])
    if loose_jet_id_cut < 3:
      continue
    count_ev = count_ev + 1
    for j in [[0, 1], [1, 2], [2, 0]]:
      beta_result = cal_beta(eta[j[0]], phi[j[0]], eta[j[1]], phi[j[1]])
      m1 = TLorentzVector()
      m2 = TLorentzVector()
      m1.SetPtEtaPhiE(pt[j[0]], eta[j[0]], phi[j[0]], e[j[0]])
      m2.SetPtEtaPhiE(pt[j[1]], eta[j[1]], phi[j[1]], e[j[1]])    

      br_beta[j[0]] = beta_result[0]
      br_del_eta[j[0]] = beta_result[1]
      br_del_phi[j[0]] = beta_result[2]
      br_del_r[j[0]] = beta_result[3]
      br_raw_mass[j[0]] = (m1 + m2).M()
      br_jet_pt[j[0]] = pt[j[0]]
      br_jet_eta[j[0]] = eta[j[0]]
      br_jet_phi[j[0]] = phi[j[0]]
      br_jet_mass[j[0]] = m1.M()

    n_jet_25 = 0
    for j in pt:
      n_jet_25 = n_jet_25 + 1
    br_njet[0] = n_jet_25
    br_met[0] = met
    br_nvtx[0] = len(ev.PVx)

    for i in range(len(hlt_name)):
      hlt = ev.GetBranch(hlt_name[i])
      lpre_br[i][0] = hlt.GetLeaf("L1prescale").GetValue()
      hpre_br[i][0] = hlt.GetLeaf("HLTprescale").GetValue()
      hlt_br[i][0] = hlt.GetLeaf("fired").GetValue()

    tr_out_beta.Fill()
  tf.Close()

print "Total input events : %i"%tot_events
print "Passed(selected) events : %i"%selected_events

tf_out.Write()
tf_out.Close()


