from quantity import Quantity

extracts = { 'corn_sugar' : 42.0,
             'cane_sugar' : 46.0 }

def extract_ppg(ingredient):
   """Look up expected extract in point/pound/gallon for
   a given ingredient
   """
   e = Quantity();
   e.value=extracts[ingredient]
   e.unit='ppg'
   return(e)

def gravity(ingredient, ingredient_mass, water_volume):
    """Caulculate gravity from ingredient

    Given an ingredient and amount and the volume of water it is added
    to, what is the resulting specific gravity?
    """
    ppg=extract_ppg(ingredient)
    points=ingredient_mass.to('lb') * ppg.value / water_volume.to('gal')
    return(1.0 + points/1000.0)
