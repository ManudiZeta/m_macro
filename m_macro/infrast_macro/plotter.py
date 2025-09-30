import matplotlib.pyplot as plt
import uproot

df = uproot.open('Bd2JpsiKS.root:tree').arrays(['isSignal', 'Mbc'], library='pd')

df.hist('Mbc', bins=100, range=(4.3, 5.3), by='isSignal')
plt.xlabel(r'M$_{\rm bc}$ [GeV/c$^{2}$]')
plt.ylabel('Number of candidates')
plt.xlim(4.3, 5.3)
plt.savefig('Mbc_MCsplit.png')
