import numpy as np
import matplotlib.pyplot as plt
from scipy import transpose
from scipy.integrate import odeint
from models import pbpkModel
from exposure import exposure
import variableInput


time = np.linspace(0, 100, 1001)

# PBPK model


def pbpk(BW, VFC):
    # PBPK output

    out = odeint(pbpkModel, list(state.values()), time, args=(BW, VFC))
    return out


veces = np.linspace(1, 10, 10)
colors = ('#ffff00', '#00ffff', '#ff00ff', '#0000ff', '#ff0000', '#00ff00', '#000000', '#ff7f00', '#ff007f', '#7fff00', '#00ff7f')
for i in veces:
    vars = variableInput.randomize()
    BW = vars['BW']
    VFC = vars['VFC']
    exps = exposure(BW)
    state = {
        'arterial': exps['IV'],
        'liver': exps['ORAL'],
        'kidney': 0,
        'urine': 0,
        'muscleblood': 0, 'muscle': exps['IM'],
        'fatblood': 0, 'fat': 0,
        'rich': 0,
        'slowblood': 0, 'slow': 0
    }
    output = pbpk(BW, VFC)
    putout = transpose(output)
    i = 0
    for o in putout:
        # plt.semilogy(time, o, colors[i])
        plt.plot(time, o, colors[i])
        i += 1
plt.show()
