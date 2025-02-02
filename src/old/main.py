from const import *
from ex1.extract_data import extract
from my_file import myFile
from ex1.process_data import fit_for_tau, fit_for_c, fit_for_l, get_v_in_medium
from ex1.plot import linear
import myutils as myutils
from ex2 import extract_data
from matplotlib import pyplot as plt


def ex1():

    data_files : list[myFile] = extract()
    
    # for file in data_files:
    #     file.print()
    
    # data_files[0].print()
    
    # print(data_files)
    
    # y1, y2 = data_files[0].ch1, data_files[0].ch2
    
    results: dict[str, list[tuple[int, float, float]]] = fit_for_tau(data_files)
    
    # pprint.pprint(results)
    
    C_prime, C_err = fit_for_c(results["C"], 10_000)
    L_prime, L_err = fit_for_l(results["L"], 47)

    
    display_C = myutils.bsci_err(C_prime, C_err)
    display_L = myutils.bsci_err(L_prime, L_err)
    
    print( "C' =", display_C )
    print( "L' =", display_L )
    
    v, v_err = get_v_in_medium(C_prime, C_err, L_prime, L_err)
    display_v = myutils.bsci_err(v, v_err)
    
    print( "v  =", display_v )
    
    
    
    
    
def ex2() :
    
    extract_data.extract()
    
    pass
    


if __name__ == "__main__":
    
    # ex1()
    ex2()