from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from mash import Mash

class InfusionMash(Mash):
    """A single step infusion mash

    m =  Mash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print m
    """

    def __init__(self, **kwargs):
        super(Mash, self).__init__(**kwargs)
        #self.subname=( name if name else 'mash' )
        if ('start' in kwargs):
            # Initialize from previous mash step
            m = kwargs['start']
            self.property('t_initial',m.property('temp').quantity)
            self.property('hc_initial',m.property('hc_total').quantity)

    def solve(self):
        """Solve for unknowns
        
        Will barf unless we have the following properties:
        """
        t_mash = self.property('temp').quantity.to('F')
        #
        shc_water=Quantity("1Btu/lb/F")
        volume_water=self.total_water()
        mass_water=Quantity(volume_water.to('pt'),'lb') #1lb == 1pt
        hc_water=Quantity(mass_water.to('lb')*shc_water.to('Btu/lb/F'),'Btu/F')
        if (self.property('hc_initial') is not None):
            hc_initial=self.property('hc_initial').quantity
            t_initial=self.property('t_initial').quantity
        else:
            # fudge for starting with mashtun and grain
            mass_grain=self.total_grains()
            shc_grain =Quantity("0.3822Btu/lb/F")
            hc_grain=Quantity(mass_grain.to('lb')*shc_grain.to('Btu/lb/F'),'Btu/F')
            shc_stainless=Quantity("0.120Btu/lb/F")
            mass_mashtun=Quantity("9.5lb")
            hc_mashtun=Quantity(mass_mashtun.to('lb')*shc_stainless.to('Btu/lb/F'),'Btu/F')
            hc_initial=hc_grain+hc_mashtun
            t_initial = self.property('t_mashtun').quantity
        hc_total=hc_water+hc_initial
        t_strike=Quantity( ((hc_total.value*t_mash - hc_initial.value*t_initial.to('F')) / hc_water.value), 'F')
        self.property('t_strike',t_strike,'F')
        self.property('hc_total',hc_total)
