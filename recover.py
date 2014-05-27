from ROOT import *
from os import mkdir, chdir
from cc_ana_tool import *


def comp_data_mc(h_list, color, pad):
  tmp = h_list[0].GetName().split("_")
  for x in xrange(len(tmp)):
    if tmp[x] == "log":
      set_log = int(tmp[x+1])
      break

  pad.cd()
  padt = TPad("t", "t", 0.0, 1.0, 1.0, 0.45)
  padb = TPad("b", "b", 0.0, 0.45, 1.0, 0.0)
  margin_s = 0.005
  margin_b = 2.0
  padt.Draw()
  padt.cd()
  padt.SetLogy(set_log)
  padt.SetBottomMargin(0.05)
  padt.SetTopMargin(0.18)
  for i, h in enumerate(h_list):
    h.Scale(1.0/h.GetEntries())
    h.SetLineColor(color[i])
    if i == 0:
      if set_log == 1:
        h.SetMinimum(0.00001)
      else:
        h.SetMinimum(0)
      h.SetStats(0)
      h.GetYaxis().SetTitle("Normalized Yield")
      h.GetYaxis().SetTitle("Normalized Yield")
      h.GetYaxis().SetTitleOffset(0.9)
      h.GetYaxis().SetTitleSize(0.06)
      h.GetYaxis().SetLabelSize(0.06)
      h.GetXaxis().SetLabelOffset(1.7)
      h.GetXaxis().SetTitleOffset(1.7)
      h.SetLineWidth(2)
      h.Draw()
    else:
      h.SetLineWidth(1)
      h.DrawNormalized("same")
  pad.cd()
  padb.Draw()
  padb.cd()
  padb.SetGrid()
  padb.SetTopMargin(0.018)
  padb.SetBottomMargin(0.3)
  
  for i, h in enumerate(h_list[1:]):
    if i == 0:
      h.Divide(h_list[0])
      h.SetStats(0)
      h.SetTitle("")
      h.GetYaxis().SetTitle("data / mc")
      h.GetYaxis().SetTitleSize(0.08)
      h.GetYaxis().SetTitleOffset(0.65)
      h.GetYaxis().SetLabelSize(0.1)
      h.GetXaxis().SetTitleSize(0.1)
      h.GetYaxis().SetLabelSize(0.05)
      h.GetXaxis().SetLabelSize(0.07)
      h.Draw()
    else:
      h.Divide(h_list[0])
      h.Draw("same")
  pad.cd()
  return pad

def comp_cut(h_list, color, pad):
  le = TLegend(0.8, 0.1, 0.9, 0.2)
  le.SetFillStyle(0)
  le.SetBorderSize(0)
  for i, h in enumerate(h_list):
    h.SetLineColor(color[i])
    le.AddEntry(h, l_name[i])
    if i == 0:
      h.SetStats(0)
      h.SetMinimum(0)
      title = ""
      for x in h.GetTitle().split()[2:]:
        title = title + x
      h.SetTitle(title)
      h.GetYaxis().SetTitle("Normalized Yield")
      h.GetYaxis().SetTitleOffset(1.5)
      h.DrawNormalized()
    else:
      h.DrawNormalized("same")
  le.Draw()
  return pad, le

data_root = "hist_data_jec.root"
mc_root_p = "hist_mc_p_jec.root"
mc_root_h = "hist_mc_h_jec.root"
tf = TFile(data_root)
tf_mc_p = TFile(mc_root_p)
tf_mc_h = TFile(mc_root_h)

dname = "test_jec"
mkdir(dname)
chdir(dname)

list_his = [x.GetName() for x in tf.GetListOfKeys()]

c1 = TCanvas("c1", "c1", 800, 600)
color = [1, 2, 4]
for x in list_his:
  h_data = tf.Get(x)
  h_mc_p = tf_mc_p.Get(x)
  h_mc_h = tf_mc_h.Get(x)

  hist_list = []
  for i in [h_data, h_mc_p, h_mc_h]:
    hist_list.append(i.Clone(x+"comp"))
  tmpc = comp_data_mc(hist_list, color, c1)
  tmpc.SaveAs(x+".png")





