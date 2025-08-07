import matplotlib.pyplot as plt
import numpy as np
from itertools import accumulate 
import random
from scipy.stats import cauchy



def intersect(curve1, curve2):
    """Return the intersection point of two step curves"""
    
    points1 = [(curve1[i, 0], curve1[i, 1]) if j == 0 else (curve1[i, 0], curve1[i + 1, 1]) for i in range(curve1.shape[0] - 1) for j in range(2)]
    points2 = [(curve2[i, 0], curve2[i, 1]) if j == 0 else (curve2[i, 0], curve2[i + 1, 1]) for i in range(curve2.shape[0] - 1) for j in range(2)]
    
    for i in range(len(points1)-1):
        p1, p2 = points1[i], points1[i+1]
        x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
        for j in range(len(points2)-1):
            p3, p4 = points2[j], points2[j+1]
            x3, y3, x4, y4 = p3[0], p3[1], p4[0], p4[1]
            
            delta = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
            
            if delta != 0:
                
                t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / delta
                u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / delta
                
                if 0 <= t <= 1 and 0 <= u <= 1:
                   # Calcul des coordonnées d'intersection
                   x = x1 + t * (x2 - x1)
                   y = y1 + t * (y2 - y1)
                   
                   return(x, y)
               
    return None
                   
                  
def supply_demand_curve(sup, dem):
            
    fig, ax1 = plt.subplots()
    
    
    ax1.step(sup[0], sup[1], where='pre', label='Merit-order', color='b')
    ax1.step(dem[0], dem[1], where='pre', label='Demand', color='r')
    ax1.set_xlabel('GWh')
    ax1.set_ylabel('Prix (€/MWh)', color='b')
    #ax1.set_xticks(np.arange(0, max((sup[0], dem[0])), ))
    #ax1.set_yticks(np.arange(0, 230, 10))
    ax1.tick_params(axis='y', labelcolor='b')
    plt.grid(visible=True)
    
    

def marginal_price(bids, asks):
    """Input: supply curve of supply and demand, shaped as: [(quantity1, price1), (quantity2, price2), ...]"""
    
    bids = sorted(bids, key=lambda x:x[1])
    asks = sorted(asks, key=lambda x:x[1])
    
    cum_bids = list(accumulate(x[0] for x in bids))
    cum_asks = list(accumulate(x[0] for x in asks))
    
    supply = np.array([(cum_bids[i], bids[i][1]) for i in range(len(bids))])
    demand = np.array([(cum_asks[j], asks[j][1]) for j in range(len(asks))])
    
    marginal = intersect(supply, demand)
    
    
    supply = np.transpose(supply)
    demand = np.transpose(demand)

    
    supply_demand_curve(supply, demand)
    
    return marginal








        

        

