
file = "opamp_2_3a_norm.csv"
path = "C:\\Workspace\\python\\Lab4-2\\data\\4\\"

from extract import csv_extract
(delta_t, Vdiodo, Vout, err) = csv_extract(path + file)

Idiodo = list(map( lambda x: x/1000 , Vout))

import numpy
func = lambda V, Is, n, I0: Is * ( numpy.exp(40*V/n) - 1 ) + I0

from scipy.optimize import curve_fit
(Is, n, I0), (errs) = curve_fit( 
    f = func,
    xdata= Vdiodo,
    ydata= Idiodo,
    sigma= err/numpy.sqrt(12)
)

errs = numpy.sqrt(numpy.diag(errs))

Is_err = errs[0]
n_err = errs[1]

from myutils import bsci_err
print("Is = " + bsci_err(Is, Is_err))
print("n  = " + bsci_err(n, n_err))
print("I0 = " + bsci_err(I0, errs[2]))
# print(err/1000)

from matplotlib import pyplot
curve, = pyplot.plot(Vdiodo, Idiodo)
curve.set_label("Punti empirici")

V_dummy = numpy.linspace(min(Vdiodo), max(Vdiodo), num= 100)
I_dummy = list(map( lambda V: func(V, Is, n, I0), V_dummy))

curve, = pyplot.plot(V_dummy, I_dummy)
curve.set_label("Risultato del fit")

pyplot.xlabel("DDP diodo [V]")
pyplot.ylabel("Corrente attraverso il diodo [A]")
pyplot.title("Plot Shockley", size = 16, weight = "roman")

legend = pyplot.legend()
legend.set_loc("upper left")

axes = pyplot.gca()
axes.grid(visible= True, which= "both")
pyplot.axhline(linewidth = .8, color = "k")
pyplot.axvline(linewidth = .8, color = "k")



pyplot.show()

# I = Is * ( exp(40*V/n) - 1 )

# vout = - 1000* Idiodo
