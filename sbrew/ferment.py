"""Model Fermentation."""
from .recipe import Recipe,MissingParam
from .ingredient import Ingredient
from .quantity import Quantity
from .property import Property

# Good sources for formulas
# http://www.primetab.com/formulas.html

class Ferment(Recipe):
    """A fermentation is a simple recipe with no sub-steps."""

    DEFAULT_NAME='ferment'

    def __init__(self, **kwargs):
        """Initialize Ferment object."""
        super(Ferment, self).__init__(**kwargs)

    def import_forward(self):
        """Import properties from previous step."""
        self.import_property('OG')
        self.import_property('IBU')
        self.import_property('SRM')

    def import_backward(self):
        """Import desired properties from next step."""
        self.import_property('FG',source='output')

    def solve(self):
        """Calculate the ABV and attenuation based on OG and FG."""
        if ('OG' in self.properties and
            'FG' in self.properties ):
            self.property('ABV', Quantity(self.abv(),'%ABV') )
            self.property('atten', ((self.property('OG').to('sg')-self.property('FG').to('sg'))/(self.property('OG').to('sg')-1.0)*100.0), '%atten' )
        elif ('OG' in self.properties and
              'atten' in self.properties):
            fg = 1.0 + (self.property('OG').to('sg')-1.0) * ( 1.0 - self.property('atten').to('%atten') / 100.0 )
            self.property('FG', Quantity(fg,'sg') )
            self.property('ABV', Quantity(self.abv(),'%ABV') )
        elif ('ABV' in self.properties and
              'atten' in self.properties):
            fatten = self.property('atten').to('%atten') / 100.0
            ogp = self.property('ABV').to('%ABV') / ( fatten * 105 * 1.25 )
            fgp = ( 1.0 - fatten ) * ogp
            self.property('OG', Quantity(1.0+ogp,'sg') )
            self.property('FG', Quantity(1.0+fgp,'sg') )
        else:
            raise MissingParam("Cannot solve ferment, have %s properties" % (self.properties.keys()))

    
    def abv(self):
        """Calculate the ABV and attenuation based on OG and FG.

        The Complete Joy of Home Brewing, 3rd ed, p43
        ABW = OG-FG * 105, (where OG and FG in specific gravity)
        ABV = ABW * 1.25
        """
        return( (self.property('OG').to('sg') - self.property('FG').to('sg')) * 105 * 1.25 )

    def end_state_str(self):
        """Description of end state of fermantion.

        Includes the ABV and, if available, the apparent attenuation.
        """
        try:
            self.solve()
        except:
            pass
        if (not 'ABV' in self.properties):
            return('?')
        s = str(self.property('ABV').quantity)
        if ('atten' in self.properties):
            s += ' (' + str(self.property('atten').quantity) + ')'
        return(s)
