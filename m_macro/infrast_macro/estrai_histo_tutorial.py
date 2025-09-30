import ROOT

mys = ROOT.TFile("../Bd2JpsiKS.root")
tree = mys.Get("tree")
histo=ROOT.TH1D("histo","istogramma",100,5.2,5.3)
myfunz=ROOT.TF1("myfunz","gaus",5.2,5.3)

for event in tree:
    histo.Fill(event.Mbc)


tela = ROOT.TCanvas()
histo.Fit(myfunz,"","",5.27,5.29)
histo.SetFillColor(3)
histo.SetTitle("B^{0}#rightarrow J/#psi (#rightarrowe^{+}e^{-}) + K_{S}^{0} (#rightarrow\pi^{+}\pi^{-})")
histo.GetXaxis().SetTitle("M_{bc} [GeV]")
histo.GetYaxis().SetTitle("counts")
histo.GetXaxis().SetRangeUser(5.23, 5.295)

histo.Draw()
myfunz.Draw("same")


tela.SaveAs("images_b2/histo.pdf")

input("Press Enter to close the plot and exit...")
