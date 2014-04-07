from ROOT import *
import sys
from math import sqrt
import os

pi = TMath.Pi()

def cal_del_phi(phi1, phi2):
  diff = phi2 - phi1
  if(diff > pi):
    return diff - 2. * pi
  elif(diff < -pi):
    return diff + 2. * pi
  else:
    return diff

def cal_raw_mass(pt, eta, phi, e):
  m1 = TLorentzVector()
  m2 = TLorentzVector()
  m1.SetPtEtaPhiE(pt[0], eta[0], phi[0], e[0])
  m2.SetPtEtaPhiE(pt[1], eta[1], phi[1], e[1])
  return (m1 + m2).M()

def cal_beta(eta, phi):
  del_eta = eta[2] - eta[1]
  del_phi = cal_del_phi(phi[1], phi[2])
  r23 = sqrt(del_eta**2 + del_phi**2)
  sign_eta2 = TMath.Sign(1., eta[1])
  beta = TMath.ATan2(del_phi, sign_eta2 * del_eta)
  return [beta, r23, del_eta, del_phi]

def list_root_file(path):
  ls = os.listdir(path)
  flist = []
  for x in ls:
    if x.endswith(".root"):
      flist.append(x)
  return flist


