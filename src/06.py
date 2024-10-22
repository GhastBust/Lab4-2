from extract import csv_extract
from matplotlib import pyplot
import numpy

file1 = "a_impulse_100.csv"
file2 = "a_impulse_50.csv"
file3 = "a_impulse_10.csv"
path = "C:\\Workspace\\python\\Lab4-2\\data\\5\\"


def detect_growth_ground( ch0: list[float] ) -> tuple[int, float] : 
    
    temp = []
    mean = 0
    std = 0
    num = 30
    
    for i, point in enumerate(ch0):
        
        if i < num:
            temp.append(point)
            
        elif i == num:
            mean = numpy.mean(temp)
            std = numpy.std(temp)
            
        else:
            
            if abs(point - mean) >= 3*std*num:
                return i, mean



delta_t0, _, ch20, err = csv_extract(path + file1)
delta_t1, _, ch21, err = csv_extract(path + file2)
delta_t2, _, ch22, err = csv_extract(path + file3)

# ch20 = list(map(lambda x: x/ 100, ch20))
# ch21 = list(map(lambda x: x/ 50 , ch21))
# ch22 = list(map(lambda x: x/ 10 , ch22))

i0, m0 = detect_growth_ground(ch20)
i1, m1 = detect_growth_ground(ch21)
i2, m2 = detect_growth_ground(ch22)

ch20 = list(map(lambda x: x - m0, ch20))
ch21 = list(map(lambda x: x - m1, ch21))
ch22 = list(map(lambda x: x - m2, ch22))

ch20 = ch20[i0:]
ch21 = ch21[i1:]
ch22 = ch22[i2:]

time0 = numpy.arange(stop = len(ch20)) * delta_t0
time1 = numpy.arange(stop = len(ch21)) * delta_t1
time2 = numpy.arange(stop = len(ch22)) * delta_t2

curve, = pyplot.plot(time0, ch20)
curve.set_label("Scarica 100$\mu$s")
curve, = pyplot.plot(time1, ch21)
curve.set_label("Scarica 50$\mu$s")
curve, = pyplot.plot(time2, ch22)
curve.set_label("Scarica 10$\mu$s")


tau = 100_000 * 0.000_000_010
sqrt5 = numpy.sqrt(5)

from numpy import sinh, exp
g = lambda t: 2/tau/sqrt5 * exp(-3*t/2/tau) * sinh(sqrt5*t/2/tau)

llim, rlim = pyplot.xlim()
pyplot.autoscale(False)

dummy_t = numpy.linspace( start= llim, stop= rlim, num= 500)
dummy_g = list(map(lambda t: g(t) * .000_1*4.8, dummy_t))

pyplot.grid(visible= True, which= "both")
pyplot.axhline(linewidth = .8, color = "k")
pyplot.axvline(linewidth = .8, color = "k")

curve, = pyplot.plot(dummy_t, dummy_g)
curve.set_label("Predizione teorica 100$\mu$s")

pyplot.title("Scarica passa basso tradizionale", size = 16, weight = "roman")
pyplot.xlabel("Tempo [s]")
pyplot.ylabel("Tensione [V]")

legend = pyplot.legend()
legend.set_loc("upper right")

pyplot.show()

# ch20 = numpy.array(ch20)
# ch21 = numpy.array(ch21)
# ch22 = numpy.array(ch22)

# # V_dummy = numpy.linspace(min(Vdiodo), max(Vdiodo), num= 100)


# a = time > .01
# a = a[0:7000]
# time = time[0:7000]
# ch20 = ch20[0:7000]
# ch21 = ch21[0:7000]
# ch22 = ch22[0:7000]

# time = time[a]
# ch20  = ch20[a]
# ch21  = ch21[a]
# ch22  = ch22[a]

# # ch1 = list(map(lambda x: x/33, ch1))




# from scipy.optimize import curve_fit

# gplus = lambda t, A, t0: A*g(t - t0)

# (A, t0) , (_) = curve_fit(
#     f= gplus,
#     xdata= time,
#     ydata= ch20
# )

# # dummy_t = numpy.linspace(start=0.01, stop = len(ch1)* delta_t, num=100)
# ggraph = lambda t: gplus(t, A, t0)
# dummy_v = list(map(lambda t: gplus(t, -0.000001, 0.015), time))

# # pyplot.plot(time, ch1)
# pyplot.plot(time, ch20)
# pyplot.plot(time, ch21)
# pyplot.plot(time, ch22)
# # pyplot.plot(time, dummy_v)
# pyplot.show()
