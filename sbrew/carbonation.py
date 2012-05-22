from quantity import Quantity

def psi_required(temp, vol):
   """Pressure required for CO2 volumes at given temparature.

   From:
   http://www.homebrewtalk.com/f128/formula-dissolved-co2-152427/

   -16.6999 - 0.0101059 * T + 0.00116512 * T ^2 + 
   0.173354 * T * Vol +4.24267 * Vol - 0.0684226 * Vol ^2

   where T is degrees F and Vol is volumes of CO2 you want. but I 
   do agree that that is just a best fit equation.

   This formula agrees with the value in the table on p184 of Papazian,
   The Home Brewer's Companion.
   """
   t=temp.to('F')
   v=vol.value
   p=(-16.6999 - 0.0101059*t + 0.00116512*t*t + \
      0.173354*t*v + 4.24267*v - 0.0684226*v*v)
   return(Quantity(p,'psi'))
