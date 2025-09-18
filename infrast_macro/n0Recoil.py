import ROOT
import numpy as np

mys = ROOT.TFile("vpho_p_pi_n.root")
tree = mys.Get("tree")
histo=ROOT.TH1D("histo","istogramma",100,0,5)
m02=0

for event in tree:
    p_p =np.array ([event.p_px, event.p_py, event.p_pz])
    p_pi =np.array ([event.pi_px, event.pi_py, event.pi_pz])
    p_g =np.array ([event.gamma_px, event.gamma_py, event.gamma_pz])
    p_tot = p_p + p_pi + p_g                
    deltaE = (event.InvM) - (event.p_E + event.pi_E + event.gamma_E )

    m02 = deltaE*deltaE - p_tot.dot(p_tot)
    histo.Fill(np.sqrt(m02))


tela = ROOT.TCanvas()
histo.SetFillColor(3)
histo.SetTitle("#bar{n_0} mass")
histo.GetXaxis().SetTitle("M_{n0} [GeV]")
histo.GetYaxis().SetTitle("counts")

histo.Draw()

tela.SaveAs("infrast_macro/images_b2/n0-bar.pdf")

input("Press Enter to close the plot and exit...")
