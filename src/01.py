from matplotlib import pyplot
from scipy import optimize
import numpy
from extract import csv_extract


files = ["opamp_2_1a.csv", "opamp_2_1b.csv"]






for file in files:
    
    (delta_t, ch1, ch2, err) = csv_extract("C:\\Workspace\\python\\Lab4-2\\data\\4\\" + file)
    err /= numpy.sqrt(12)
    
    
    sinf = lambda t, A, t0: (
        A * numpy.sin((t - t0) * 1_000)
    )
    
    t_range = numpy.arange(stop=len(ch1)) * delta_t
    
    (A1, _), (err1) = optimize.curve_fit(
        f= sinf, 
        xdata= t_range,
        ydata= ch1,
        sigma= err)
    
    (A2, _), (err2) = optimize.curve_fit(
        f= sinf, 
        xdata= t_range,
        ydata= ch2,
        sigma= err)
    
    err1 = numpy.sqrt(numpy.diag(err1))[0]
    err2 = numpy.sqrt(numpy.diag(err2))[0]
    
    # print(A1, A2)
    
    from myutils import bsci_err
    
    tot_err = numpy.hypot(err2/A1, err1*A2/A1**2)
    # print(A2/A1)
    # print(tot_err)
    print("G = " + str(bsci_err(A2/A1, tot_err)) ) 
    
    
    # pyplot.plot(ch1)
    # pyplot.plot(ch2)
    
    # pyplot.show()
