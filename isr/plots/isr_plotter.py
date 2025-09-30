import uproot
import matplotlib.pyplot as plt

#converto il tree di output in un file panda data frame
df_sig = uproot.open("../../../root_file/isr/isr_list_gamma_MC.root")["tree"].arrays(filter_name=["theta"],library="pd")

#numero di variabili caricate. Se non le scremo con filter_name, le carica tutte
print(f"Number of columns (= number of variables): {len(df_sig.columns)}")

plt.hist(df_sig["theta"])

plt.savefig("prova_theta.png", bbox_inches="tight")