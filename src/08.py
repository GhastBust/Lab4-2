file = "opamp_2_1c_25deg_bat.csv"
path = "C:\\Workspace\\python\\Lab4-2\\data\\4\\"

# from extract import csv_extract


def csv_extract( file: str ) -> tuple[
    float,      # delta_t
    list[float],# channel 1
    float       # error in channels
] :    
    
    if not file.endswith(".csv"):
        raise ValueError("file ext was ." + file.split(".")[-1])
    
    from typing import Optional
    
    t0      : Optional[float] = None
    delta_t : Optional[float] = None
    
    prev_v  : Optional[float] = None
    err     : Optional[float] = None
    delta_v : float           = 0
    
    ch1: list[float] = []
    # ch2: list[float] = []
    
    import csv
    
    with open(file) as csvfile :
        
        reader = csv.reader(csvfile)
        
        for i, row in enumerate(reader):
            
            #* salta i primi 4 valori
            if i <= 3:
                continue
            
            
            #* valida i risultati nella corrente riga
            try:
                current_t  = float(row[0])
                current_v1 = float(row[1])
                # current_v2 = float(row[2])
            except ValueError:
                continue
            
            
            #* determina delta_t dai primi 2 valori di t
            if t0 == None:
                t0 = current_t  
                
            elif delta_t == None:
                delta_t = current_t - t0
                
                
            #* determina l'errore sulla tensione: il più piccolo scalino
            if prev_v != None :
                
                delta_v = abs(prev_v - current_v1)

                if err == None or delta_v < err:
                    err = delta_v
                
            prev_v = current_v1
            
            
            #* colleziona i dati di v1 e v2
            ch1.append(current_v1)
            # ch2.append(current_v2)
    
    return delta_t, ch1, err


delta_t, ch1, err = csv_extract(path+file)

from matplotlib import pyplot
from scipy.optimize import curve_fit
from numpy import cos, pi
import numpy

time = numpy.arange(len(ch1)) * delta_t

func = lambda t, A, f1, f2, t0: -A*cos(f1*2*pi*(t-t0))*cos(f2*2*pi*(t-t0))

# t0 = 0.59
A = 5.5
funcc = lambda t, f1, f2, t0: func(t, A, f1, f2, t0)

# pyplot.plot(time, ch1, ".")
# pyplot.show()

# (f1, f2, t0), (_) = curve_fit( 
#     f = funcc,
#     xdata= time,
#     ydata= ch1,
#     # p0= (999.5, 0.5),
#     bounds= (
#         [
#             # 4,
#             999.49,
#             0.5,
#             0.5
#         ],
#         [
#             # 6,
#             999.51,
#             0.51,
#             0.7
#         ]
#     ),
#     sigma= 0.05/numpy.sqrt(12)
# )

dummy_t = numpy.linspace(min(time), max(time), num=1200)
# dummy_v = list(map(lambda t: func(t, A, f1, f2, t0), dummy_t))
dummy_v = list(map(lambda t: 5*cos(2*pi*0.5*(t-0.599759)), dummy_t))


# print(A)
# print(f1)
# print(f2)
# print(t0)

pyplot.plot(time, ch1, ".")
pyplot.plot(dummy_t, dummy_v)


pyplot.show()