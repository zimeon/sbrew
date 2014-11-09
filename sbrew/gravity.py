from quantity import Quantity;
import numpy

# Data from documentation with True Brue #6800 hydrometer
# t_data = temps in F
# c_data = specific gravity corrects to ADD 
t_data = [50,60,70,77,84,95,105,110,113,118] 
c_data = [-0.0005,0.0,0.001,0.002,0.003,0.005,0.007,0.008,0.009,0.010]

class Gravity(Quantity):

    def hydrometer_correction(self, temp='60F'):
        # get specific gravity correction
        tval = Quantity(temp).to('F')
        # barf if outside range
        if (tval<t_data[0] or tval>t_data[-1]):
            raise NameError('Temperature out of range for hydrometer, must be within 50 - 118F')
        correction = numpy.interp(tval,t_data,c_data)
        sg = self.to('sg') + correction
        return Quantity(sg,'sg')

