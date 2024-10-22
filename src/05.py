import numpy
from matplotlib import pyplot
from matplotlib import axes

frequency = [1,2,5,10,20,50,100,150,200,300,500,1000,2000,5000]

period = list(map(lambda x: 1/x, frequency))

Vins = [ 
    [1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750],
    [1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750, 1.98750],
    [2.02500, 2.02500, 2.02500, 2.02500, 2.02500, 2.02500, 2.02500, 2.02500, 2.02500, 1.97500, 1.97500, 1.97500, 1.97500, 1.97500]
]

Vouts = [
    [ 1.65750, 1.65000, 1.65000, 1.63500, 1.58250, 1.35000, 0.93750, 0.66750, 0.50250, 0.30750, 0.153130, 0.046250, 0.012250, 0.001925],
    [ 1.78750, 1.78750, 1.78750, 1.78750, 1.78750, 1.70000, 1.51250, 1.32500, 1.12500, 0.85000, 0.546000, 0.279000, 0.135000, 0.037500],
    [ 1.97500, 1.95000, 1.95000, 1.95000, 1.91250, 1.80000, 1.38750, 1.05000, 0.77500, 0.43000, 0.175000, 0.040000, 0.012625, 0.002100]
]

delta_ts = [
    [0, -3.00E-03, -3.00E-03, -2.70E-03, -2.70E-03, -2.28E-03, -1.88E-03, -1.54E-03, -1.34E-03, -1.04E-03, -7.30E-04, -4.26E-04, -2.27E-04, -9.18E-05],
    [0, -3.00E-03, -1.80E-03, -1.20E-03, -9.00E-04, -1.00E-03, -8.80E-04, -7.90E-04, -7.20E-04, -5.85E-04, -4.12E-04, -2.38E-04, -1.36E-04, -6.35E-05],
    [0, -3.00E-03, -3.20E-03, -2.40E-03, -2.30E-03, -2.02E-03, -1.86E-03, -1.66E-03, -1.48E-03, -1.16E-03, -8.20E-04, -4.82E-04, -2.34E-04, -9.82E-05]
]

labels = ["Passa basso tradizionale", "1 OPAmp", "2 OPAmp"]
colors = ["#1778ff", "#ff5e19", "#ff1f1f"]
markers= [".", "x", "v"]



# def bode(
#     frequency: list[float], 
#     H_dB: list[float],
#     )

fig = pyplot.figure(1)
x = [["a"], ["a"], ["a"], ["a"], ["b"], ["b"]]
dic: dict[str, axes.Axes] = fig.subplot_mosaic(x, sharex= True)

dic["a"].grid(visible= True, which= "both")
dic["b"].grid(visible= True, which= "both")


#* calcolo modelli teorici
#*------------------------------------------------------------------------------
#* 1

t = 100_000 * 0.000_000_010
Z = lambda s: 1 / ( (s*t)**2 + 3*s*t + 1 )
G = lambda f: Z(-2*numpy.pi*f * 1j)

dummy_f = numpy.geomspace(start=min(frequency), stop=max(frequency), num=100)
dummy_H = list(map( lambda f: 20 * numpy.log10(numpy.abs(G(f))) , dummy_f ))
dummy_o = list(map( lambda f: numpy.angle(G(f))/numpy.pi*180 , dummy_f ))

pyplot.sca(dic["a"])
curve, = pyplot.plot(dummy_f, dummy_H, "#75aaff")
curve.set_label("Tradizionale teorico")

pyplot.sca(dic["b"])
pyplot.plot(dummy_f, dummy_o, "#75aaff")


#* 2

Z = lambda s: 1 / ( (s*t)**2 + 2*s*t + 1 )
G = lambda f: Z(-2*numpy.pi*f * 1j)

dummy_f = numpy.geomspace(start=min(frequency), stop=max(frequency), num=100)
dummy_H = list(map( lambda f: 20 * numpy.log10(numpy.abs(G(f))) , dummy_f ))
dummy_o = list(map( lambda f: numpy.angle(G(f))/numpy.pi*180 , dummy_f ))

pyplot.sca(dic["a"])
curve, = pyplot.plot(dummy_f, dummy_H, "#ff5252")
curve.set_label("OPAmp teorico")

pyplot.sca(dic["b"])
pyplot.plot(dummy_f, dummy_o, "#ff5252")


#*------------------------------------------------------------------------------



#* calcolo con dati empirici
for Vin, Vout, delta_t, label, color, marker in zip(Vins, Vouts, delta_ts, labels, colors, markers) :
    
    angles = list(map(lambda dt, T: -dt/T*360, delta_t, period))
    print(angles)
    
    H_dB = list(map(lambda v0, v1: 20 * numpy.log10(v0/v1), Vout, Vin))
    
    
    pyplot.sca(dic["a"])
    curve, = pyplot.plot(frequency, H_dB, marker)
    curve.set_label(label)
    curve.set_color(color)
    
    pyplot.sca(dic["b"])
    curve, = pyplot.plot(frequency, angles, marker)
    curve.set_color(color)
    
    
    
pyplot.ylim(-10, 190)
pyplot.xscale("log")
      
pyplot.sca(dic["a"])
legend = pyplot.legend()
legend.set_loc("lower left")

dic["b"].set_xlabel("Frequenza [Hz]")
dic["a"].set_ylabel("Modulo [dB]")
dic["b"].set_ylabel("Fase [deg]")
    
pyplot.sca(dic["a"])
pyplot.title("Bode dei passa basso", size = 16, weight = "roman")
pyplot.show()