import numpy
import scipy
import scipy.optimize
from myutils import phypot, bsci_err
from matplotlib import lines
import matplotlib.pyplot as plt
import itertools
# from ex2.plot import gamma_vs_V



L =    [ 10,    20,	    30,	    40  ]
t1 =   [ 3.40,  3.40,	3.50,	3.50]
t2 =   [ 104.80,206,    309,	409 ] # ns -> us -> ms -> m
t_err =[ 0.10,	0.20,	0.50,	1   ]
V1 =   [ 2.38,	2.38,	2.38,	2.38]
V2 =   [ 2.08,	1.82,	1.60,	1.40]


R_gen = 50
R = [0,	10,	20,	30,	40,	50,	60,	70,	80,	90,	100, 110.10, 140, 170, 187.30]
V_rifl = numpy.array([-1.98, -1.32, -0.95, -0.48, -0.28, 0.01, 0.12, 0.26, 0.41, 0.52, 0.62, 0.71, 0.93, 1.06, 1.14])
V_gen = numpy.ones_like(V_rifl) * 2.38
V_err = numpy.ones_like(V_rifl) * 0.01


def frac_simm_err( a: float, b: float, sigma: float) -> float:
    
    return sigma * phypot( 1/b, a/b**2 )


def prod_err( a: float, sigma_a: float, b: float, sigma_b: float ) -> float :
    
    return phypot( a * sigma_b, b * sigma_a )



def extract() : 
    
    delta_t = numpy.array(t2) - numpy.array(t1) # in ns
    delta_t /= 1_000_000_000
    sigma = numpy.array(t_err) / numpy.sqrt(12) / 1_000_000_000
    
    lenght = lambda dt, v: v * dt
    
    v2, v_err2 = scipy.optimize.curve_fit( 
        lenght,
        xdata= delta_t,
        ydata= L,
        sigma= sigma,
        p0= 200_000_000
    )
    
    v       = v2 * 2
    v_err   = numpy.sqrt(v_err2) * 2

    lenghtt= lambda dt : lenght(dt, v)
    
    display = bsci_err(float(v), float(v_err))
    print("v nel medio =", display)
    
    # --------------------------------------------------------------------------
    
    C_norm, C_norm_err = get_normalization_contant(V1, V2)
    
    gamma_from_V, gamma_from_V_err = get_gamma_from_V(
        V_rifl, V_gen, V_err,
        C_norm, C_norm_err
    )
    
    
    gamma_f = lambda z_L, z : (z_L - z) / (z_L + z)
    
    z_fit, z_fit_err = scipy.optimize.curve_fit(
        gamma_f,
        xdata= R,
        ydata= gamma_from_V,
        sigma= gamma_from_V_err,
        p0= 50
    )
    
    gamma_ff = lambda z_L: gamma_f(z_L, z_fit)
    
    gamma_vs_V(gamma_from_V, gamma_from_V_err, R, gamma_ff )
    
    display = bsci_err( float(z_fit), float(numpy.sqrt(z_fit_err)) )
    print("Z =", display)
    
    print(get_chi2(R, gamma_from_V, gamma_from_V_err, gamma_ff)/12)
    
    
def get_chi2( x, y, dy, model):

    x = numpy.array(x)
    y = numpy.array(y)
    dy = numpy.array(dy)

    return numpy.sum((y - model(x))**2 / (dy*20)**2)

def graph_points(y, y_err, x) :
    pass


def graph_line() :
    pass


def get_gamma_from_V(V_rifl, V_gen, V_err, C_norm, C_norm_err):
    
    gamma_from_V = V_rifl / V_gen / C_norm
    gamma_from_V_err = []
    
    for Vg, Vr, Ve in zip(V_gen, V_rifl, V_err) :
        temp = Vr / Vg
        temp_err = frac_simm_err(Vr, Vg, Ve / numpy.sqrt(12))
        
        err = prod_err( temp, temp_err, C_norm, C_norm_err )
        
        gamma_from_V_err.append(err)
        
    return gamma_from_V,gamma_from_V_err


def get_normalization_contant(V1, V2):
    
    C_norm  = V2[0] / V1[0]
    C_norm_err = frac_simm_err(V2[0], V1[0], 0.02 / numpy.sqrt(12))
    
    return C_norm, C_norm_err



y = numpy.log10(numpy.array(V2) / numpy.array(V1))/10
# y[0] = 0.921
x = numpy.array(L)
y_errs = numpy.ones_like(y) * 0.0005
f = lambda x, m, q: x * m + q

(m_val, q_val), err = scipy.optimize.curve_fit(
    f = f,
    xdata= x,
    ydata= y,
)

# y_errs = list(map(lambda x: x*5000000, y_errs))
# y = list(map(lambda x: 1000000*x, y))

err_bar = plt.errorbar(x= x, y= y, yerr= y_errs, fmt= ".", color = "#8a0900")
# err_bar = list(map(lambda x, x.,err_bar))
err_bar.set_label("Dati empirici")

axes = plt.gca()
axes.grid(visible= True, which= "both")
    
f_prime = lambda x: f(x, m_val, q_val)

xaxis = numpy.linspace( max(x), min(x), 100 )
yaxis = list(map(f_prime, xaxis))

fit_curve = plt.plot(xaxis, yaxis, marker = "")[0]
fit_curve.set_label("Curva del fit")
fit_curve.set_color("#ff695e")

plt.axhline(linewidth = .8, color = "k")
plt.axvline(linewidth = .8, color = "k")

legend = plt.legend()

legend.set_label("Legenda")
legend.set_loc("upper right")

# plt.rcParams['text.usetex'] = True

axes.set_xlabel("Lunghezza del cavo [m]")
axes.set_ylabel( "Attenuazione [dB]" )

# axes.set_xticks()

title = plt.title("Fit per l'attenuazione" , size = 16, weight = "roman")

plt.show()

err = numpy.sqrt(numpy.diag(err))

m_err = err[0]
q_err = err[1]

print("m =" + bsci_err(m_val, m_err))
print("q =" + bsci_err(q_val, q_err))

print(get_chi2(x, y, y_errs, f_prime))
