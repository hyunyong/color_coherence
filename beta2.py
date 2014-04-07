from colorcoherence import *
from ROOT import *
from array import array

tf_out = TFile("../beta_j.root","RECREATE")

tr_out_b = TTree("beta<0.8", "beta distribution eta < 0.8")
tr_out_e = TTree("0.8<beta<2.5", "beta distribution 0.8 < eta2 < 2.5")

beta_b = array('f', [0])
beta_e = array('f', [0])

del_eta_b = array('f', [0])
del_eta_e = array('f', [0])

del_phi_b = array('f', [0])
del_phi_e = array('f', [0])

r23_e = array('f', [0])
r23_b = array('f', [0])

raw_mass_e = array('f', [0])
raw_mass_b = array('f', [0])

pt_e = array('f', [0, 0, 0])
pt_b = array('f', [0, 0, 0])

eta_e = array('f', [0, 0, 0])
eta_b = array('f', [0, 0, 0])

phi_e = array('f', [0, 0, 0])
phi_b = array('f', [0, 0, 0])

br_b = [beta_b, del_eta_b, del_phi_b, r23_b, raw_mass_b, pt_b, eta_b, phi_b]
br_e = [beta_e, del_eta_e, del_phi_e, r23_e, raw_mass_e, pt_e, eta_e, phi_e]
br_s = ["beta", "del_eta", "del_phi", "r23", "raw_mass", "pt", "eta", "phi"]
 
for x in xrange(len(br_s)):
  tr_out_b.Branch(br_s[x]+"_b", br_b[x], br_s[x]+"_b")
for x in xrange(len(br_s)):
  tr_out_e.Branch(br_s[x]+"_e", br_e[x], br_s[x]+"_e")

pt_cut = 30.0
r_cut_min = 0.5
r_cut_max = 1.5
mass_cut = 220.0
eta_cut = 2.5

root_f = list_root_file("/pnfs/user/Jangbae/Delphes_Generation/SimulatedResults/")

selected_events = 0

for f in root_f:
  tf = TFile(f)
  td = tf.Get("ak5gen")
  tr = td.Get("InclusiveJetTree")
  print "Open file : "+f 
  for e in tr:
    pt  = e.genpfpt
    eta = e.genpfeta
    phi = e.genpfphi
    e   = e.genpfe

    if(len(pt) < 3):
      continue
    if(pt[0] < pt[1]):
      print "Jet pT sorting is wrong!"
      break
    if(abs(eta[0]) > eta_cut or abs(eta[1]) > eta_cut):
      continue
    if(pt[2] < pt_cut):
      continue
    raw_mass = cal_raw_mass(pt, eta, phi, e)
    if(raw_mass < mass_cut):
      continue
    #raw_mass_t[0] = raw_mass
    beta_r = cal_beta(eta, phi)
    r23 = beta_r[1]
    if(r23 < r_cut_min or r23 > r_cut_max):
      continue
    selected_events = selected_events + 1
    if(abs(eta[1]) < 0.8):
      beta_b[0]    = abs(beta_r[0])
      del_eta_b[0] = beta_r[2]
      del_phi_b[0] = beta_r[3]
      for i in range(3):
        pt_b[i]  = pt[i]
        eta_b[i] = eta[i]
        phi_b[i] = phi[i]
      r23_b[0] = beta_r[1]
      raw_mass_b[0] = raw_mass
      tr_out_b.Fill()
    elif(abs(eta[1]) < 2.5):
      beta_e[0]    = abs(beta_r[0])
      del_eta_e[0] = beta_r[2]
      del_phi_e[0] = beta_r[3]
      for i in range(3):
        pt_e[i]  = pt[i]
        eta_e[i] = eta[i]
        phi_e[i] = phi[i]
      r23_e[0] = beta_r[1]
      raw_mass_e[0] = raw_mass
      tr_out_e.Fill()

tf_out.Write()
tf_out.Close() 
    

