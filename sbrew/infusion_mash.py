from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from mash import Mash

class InfusionMash(Mash):
    """A single step infusion mash

    m =  InfusionMash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print m
    """

    def __init__(self, **kwargs):
        super(InfusionMash, self).__init__()
        # Initialize from previous mash step
        self.import_property(kwargs, 'temp', 't_initial')
        self.import_property(kwargs, 'hc_total', 'hc_initial')
        if ('start' in kwargs):
            self.ingredient('grain','from prior mash',kwargs['start'].total_grains())
            self.ingredient('water','from prior mash',kwargs['start'].total_water())

    def solve(self):
        """Solve for unknowns
        
        Will barf unless we have the following properties:
        """
        t_mash = self.property('temp').quantity.to('F')
        #
        shc_water=Quantity("1Btu/lb/F")
        if (self.has_properties('hc_initial','t_initial')):
            # starting from a prior mash
            volume_water=self.ingredient('water','strike')
            hc_initial=self.property('hc_initial').quantity
            t_initial=self.property('t_initial').quantity
        else:
            # fudge for starting with mashtun and grain
            volume_water=self.total_water()
            mass_grain=self.total_grains()
            shc_grain =Quantity("0.3822Btu/lb/F")
            hc_grain=Quantity(mass_grain.to('lb')*shc_grain.to('Btu/lb/F'),'Btu/F')
            shc_stainless=Quantity("0.120Btu/lb/F")
            mass_mashtun=Quantity("9.5lb")
            hc_mashtun=Quantity(mass_mashtun.to('lb')*shc_stainless.to('Btu/lb/F'),'Btu/F')
            hc_initial=hc_grain+hc_mashtun
            t_initial = self.property('t_mashtun',default='60F').quantity
        #
        mass_water=Quantity(volume_water.to('pt'),'lb') #1lb == 1pt
        hc_water=Quantity(mass_water.to('lb')*shc_water.to('Btu/lb/F'),'Btu/F') 
        # sanity check
        if (hc_water.value<0.000000001):
            raise Exception("hc_water zero which won't work")
        hc_total=hc_water+hc_initial
        t_strike=Quantity( ((hc_total.value*t_mash - hc_initial.value*t_initial.to('F')) / hc_water.value), 'F')
        self.property('t_strike',t_strike,'F')
        self.property('hc_total',hc_total)

        # set output values
        self.property('total_water', self.total_water())
        self.property('total_grain', self.total_grains())
        self.property('total_points', self.total_points())
