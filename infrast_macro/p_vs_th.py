import ROOT

mys = ROOT.TFile("../root_file/vpho_p_pi_n.root")
tree = mys.Get("tree")
graf=ROOT.TGraph()

for event in tree:
	if(event.pRecoil<7):
		graf.AddPoint(event.pRecoilTheta, event.pRecoil)

tela = ROOT.TCanvas()
#histo.Fit(myfunz,"","",5.27,5.29)
graf.GetXaxis().SetTitle("#theta_{recoil} [rad]")
graf.GetYaxis().SetTitle("p_{recoil} [GeV]")
graf.GetXaxis().SetRangeUser(0, 3.14)

graf.Draw("AP")
tela.Update()
ROOT.gApplication.Run()
#input("Press Enter to close the plot and exit...")
