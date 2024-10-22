
def csv_extract( file: str ) -> tuple[
    float,      # delta_t
    list[float],# channel 1
    list[float],# channel 2
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
    ch2: list[float] = []
    
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
                current_v2 = float(row[2])
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
            ch2.append(current_v2)
    
    return delta_t, ch1, ch2, err