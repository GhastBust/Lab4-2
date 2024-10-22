from extract import csv_extract

path = "C:\\Workspace\\python\\Lab4-2\\data\\4\\"

files = [
    "opamp_2_2_d_saw.csv",
    "opamp_2_2_d_sin.csv",
    "opamp_2_2_d_sqr.csv",
    "opamp_2_2_d_tri.csv"]

names = [
"onda a sega",
"onda sinusoidale",
"onda quadra",
"onda triangolare"]

def get_derivative( ys: list[float], delta_x: float ) -> list[float]:
    
    y_prime = []
    y_prev = ys[0]
    
    for y in ys:
        y_prime.append((y-y_prev)/delta_x)
        y_prev = y
        
    return y_prime





for file, name in zip(files,names) :
    
    (delta_t, ch1, ch2, err) = csv_extract(path + file)
    ch1der = get_derivative(ch1, delta_t*10000)
    
    from scipy.optimize import curve_fit
    import numpy
    
    def func(i, A) -> float:
        return - numpy.array(ch1der)[i.astype(int)] * A
    
    A, errA = curve_fit(
        f = func,
        xdata= numpy.arange(len(ch2)),
        ydata= ch2
    )
    
    print(A, errA)
    
    t_range = numpy.arange(stop=len(ch1)) * delta_t
    
    from matplotlib import pyplot
    
    curve0 = pyplot.plot(t_range, ch1,    ls = ":", c = "#4d70ff")[0]
    curve0.set_label("Curva originale")
    
    curve1 = pyplot.plot(t_range, ch1der, ls = "-", c = "#ff7230")[0]
    curve1.set_label("Derivata calcolata [x$10^{-4}$]")
    
    ch2 = list(map(lambda x: -x, ch2))    
    curve2 = pyplot.plot(t_range, ch2,    ls = "-", c = "#518c50")[0]
    curve2.set_label("Derivata dall\'OPAmp")
    
    legend = pyplot.legend()
    legend.set_loc("upper right")
    
    axes = pyplot.gca()
    axes.grid(visible= True, which= "both")
    pyplot.axhline(linewidth = .8, color = "k")
    
    axes.set_xlabel("Tempo [s]")
    axes.set_ylabel("Tensione [V]")
    
    pyplot.title("Plot della derivata dell\'" + name, size = 16, weight = "roman")
    
    pyplot.show()