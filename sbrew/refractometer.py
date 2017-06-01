"""Implementation of refractometer calculations.

Sources:
http://www.primetab.com/formulas.html
http://byo.com/stories/item/1313-refractometers

Online calculators:

http://www.northernbrewer.com/refractometer-calculator/
"""
from .quantity import Quantity

def brix_to_starting_gravity(brix):
    """Brix reading to starting gravity.

    Formula was derived from the 69th edition (1988-1989) of the CRC Handbook of 
    Chemistry and Physics, "Concentrative Properties of Aqueous Solutions:
    Conversion Tables", Table 88 Sucrose
    
    MathCAD was used to curvefit the data for Degrees Brix @ 20 C (% sucrose 
    by weight) and specific gravity @ 15 C
    
        sg = 1.000898 + 0.003859118*B + 0.00001370735*B*B + 0.00000003742517*B*B*B
    
    where:

        B  = measured refractivity in Brix
        sg = calculated specific gravity at 15 C
    """
    b = brix.to("Brix")
    sg = 1.000019 + 0.003865613*b +\
         0.00001296425*b*b + 0.00000005701128*b*b*b
    return(Quantity(sg,'sg'))

def starting_gravity_to_brix(starting_gravity):
    """Starting gravity to expected brix reading (plato).
    
    Reference: Manning, M.P., Understanding Specific Gravity and Extract, Brewing Techniques, 1,3:30-35 (1993)
    
        Plato = -676.67 + 1286.4*sg - 800.47*sg*sg + 190.74*sg*sg*sg
    """
    sg = starting_gravity.to('SG')
    b = -676.67 + 1286.4*sg - 800.47*sg*sg + 190.74*sg*sg*sg
    return(Quantity(b, 'Brix'))
