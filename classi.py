import numpy as np

class Misura:
    def __init__(self,val,s):
        self.val = val
        self.s = s

    def __str__(self):
        if isinstance(self.val, (list, np.ndarray)):
            stringa = "".join(f"{val} ± {s}\n" for val,s in zip(self.val,self.s))
            return stringa
        elif isinstance(self.val, (int,float)):
            return f"{self.val} ± {self.s}"
        else:
            return "Errore nella formattazione della classe"

    def __getitem__(self, index):
        if index == 0:
            return self.val
        elif index == 1:
            return self.s
        else:
            raise IndexError("Misura ha solo indici 0 (val) e 1 (s)")

class RisultatiFit:
    def __init__(self, anal=None, res=None, chi=None):
        self.anal = anal
        if res is not None:
            self.res = np.sum(res[1])
        else:
            self.res = None
        if chi is not None:
            self.chi = np.sum(chi[1])
        else:
            self.chi = None
        if chi is not None and anal is not None:
            self.chi_ridotto = np.sum(chi[1]) / (len(chi[0]) - len(anal[0]))
        else:
            self.chi_ridotto = None

    def __str__(self):
        stringa_anal = "".join(f"{val} ± {s}\n" for val,s in zip(self.anal[0],self.anal[1]))
        return f"Parametri regressione :\n{stringa_anal}\nSomma residui :\n{self.res:.4f}\nSomma chi quadri e chi ridotto :\n{self.chi:.4f}\n{self.chi_ridotto:.4f}\n"

    def __getitem__(self, index):
        if index == 0:
            return self.anal
        elif index == 1:
            return self.res
        elif index == 2:
            return self.chi
        else:
            raise IndexError("Misura ha solo indici 0 (val) e 1 (s)")