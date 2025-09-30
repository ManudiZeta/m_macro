import ROOT

mys = ROOT.TFile("../root_file/vpho_p_pi_n.root")
tree = mys.Get("tree")
histo=ROOT.TH1D("histo","istogramma",100,0,6)
#myfunz=ROOT.TF1("myfunz","gaus",5.2,5.3)
#event.mRecoil>0 and event.p_isSignal == 1 and event.pi_isSignal == 1 and event.gamma_isSignal == 1 and event.p_genMotherPDG == 300553 and event.pi_genMotherPDG == 300553 and event.gamma_genMotherPDG== 300553

for event in tree:
    histo.Fill(event.mRecoil)


tela = ROOT.TCanvas()
#histo.Fit(myfunz,"","",5.27,5.29)
histo.SetFillColor(3)
histo.SetTitle("mRecoil (cuts over isSignal and genMotherPDG)")
histo.GetXaxis().SetTitle("M_{recoil} [GeV]")
histo.GetYaxis().SetTitle("counts")
histo.GetXaxis().SetRangeUser(0, 6)

histo.Draw()
#myfunz.Draw("same")


tela.SaveAs("images_b2/mRecoil.pdf")

ROOT.gApplication.Run()
#input("Press Enter to close the plot and exit...")
