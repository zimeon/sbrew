import re

class Quantity:
    """Base class for all quantities.

    All quantities have a value and a unit.
    """

    conversions = { 
        '%ABW' : { '%ABV' : 1.25 },
        'oz'  : { 'lb' : 1.0/16.0,
                  'kg' : 0.0283495231,
                  'g'  : 28.3495231 },
        'gal' : { 'pt' : 8.0 },
        'J'   : { 'Joule' : 1.0,
                  'kJ' : 0.001,
                  'Btu' : 0.0009478 },
        'points' : { },
        'Btu/lb/F' : { 'kJ/kg/F' : 2.324444 },
        'h'   : { 'min' : 60,
                  's'   : 3600 },
        }

    display_fmt = {
        '%ABV' : '%.1f',
        '%ABW' : '%.1f',
        'Btu/F' : '%.2f',
        'F' : '%.1f',
        'gal' : '%.2f',
        'psi' : '%.1f',
        'points' : '%.1f',
        'min' : '%d',
        'sg' : '%.3f',
        }

    all_conv = None

    def __init__(self, value=None, unit=None):
        """Create a Quantity

        May be initialized in a number of ways:
        1) empty: qty = Quantity()
        2) copy: qty2 = Quantity(qty1) #creates new object with same value and unit
        3) split: qty = Quantity(value, unit)
        4) unit only: qty = Quanityt(None, unit)
        5) string: qyt = Quantity('1gal')
        """
        #
        if (value is None):
            self.value = None
            self.unit = unit
        elif (isinstance(value, Quantity)):
            self.value = value.value
            self.unit = value.unit
        elif (unit is None):
            # try to parse value and unit from string
            m = re.match('\s*([-+]?\d+(\.\d*)?)\s*([A-Za-z%][\w/%]*)\s*$', value)
            if (m):
                self.value=float(m.group(1))
                self.unit=m.group(3)
            else:
                self.value = float(value)
                self.unit = unit
        else:
            self.value = float(value)
            self.unit = unit

    def __str__(self):
        if (self.value is None):
            return("QuantityNotDefined")
        elif (self.unit is None):
            return(str(self.value) + " (dimensionless)")
        elif (self.unit in Quantity.display_fmt):
            return( (Quantity.display_fmt[self.unit] % self.value) + " " + str(self.unit))
        else:
            return(str(self.value) + " " + str(self.unit))

    def __repr__(self):
        if (self.value is None):
            return("QuantityNotDefined")
        elif (self.unit is None):
            return(str(self.value))
        else:
            return(str(self.value) + str(self.unit))

    def to(self,new_unit):
        """Get value of this quantity in a specific unit.

        Used conversions in conversions dictionary of dictionaries
        to look up conversion factors. At present not smart enough
        to find a chain between two units but that should be possible
        add.

        e.g. lbs = weight.to('lb')
             temp=Quantity('10C')
             f = temp.to('F')
        """
        if (self.unit==new_unit):
            return(self.value)
        elif (self.unit in Quantity.conversions and
                new_unit in Quantity.conversions[self.unit]):
            return(self.value*Quantity.conversions[self.unit][new_unit])
        elif (new_unit in Quantity.conversions and
                self.unit in Quantity.conversions[new_unit]):
            #inverse
            return(self.value/Quantity.conversions[new_unit][self.unit])
        else:
            return(self.value * self.find_conversion(self.unit,new_unit))

    def convert_to(new_unit):
        """Convert internal value to the new unit

        Piggbybacks on the to() method but changes the internal
        representation. Returns self.
        """
        self.value = self.to(new_unit)
        self.unit = new_unit
        return(self)

    def __add__(self,other):
        """Add two quantities, return result in units of first.
        """
        sum=self.value+other.to(self.unit)
        return(Quantity(sum,self.unit))

    def __sub__(self,other):
        """Subtract one quantity from another, return result in units of first.
        """
        sum=self.value-other.to(self.unit)
        return(Quantity(sum,self.unit))

    @staticmethod
    def find_conversion(from_unit,to_unit):
        """Function to see whether we can fo from_unit->to_unit

        Raises and exception if not, otherwise returns factor that the value
        in from_unit is multiplied by to get a value in to_unit
        """
        if (from_unit==to_unit):
            return(1.0);
        if (Quantity.all_conv is None):
            Quantity.build_all_conv()
        if (not (from_unit in Quantity.all_conv)):
            raise LookupError('unknown original unit in conversion requested from %s to %s' % (from_unit, to_unit))
        if (not (to_unit in Quantity.all_conv)):
            raise LookupError('unknown destination unit in conversion requested from %s to %s' % (from_unit,to_unit))
        if (not (to_unit in Quantity.all_conv[from_unit])):
            raise LookupError('unknown conversion requested from %s to %s' % (from_unit,to_unit))
        return(Quantity.all_conv[from_unit][to_unit])

    def test_find_conversion():
        assert Quantity.find_conversion('kg','g') == 0.001

    @staticmethod
    def build_all_conv():
        # Expand tree of all conversions (include sanity check to 
        # avoid possible cycles)
        #
        # Build local self.conv with data from Quantity.conversions and inverses
        Quantity.all_conv={}
        for f in Quantity.conversions:
            Quantity.all_conv[f]={}
            for t in Quantity.conversions[f]:
                Quantity.all_conv[f][t]=Quantity.conversions[f][t]
                if (not (t in Quantity.conversions)):
                    Quantity.all_conv[t]={}
                if (not (f in Quantity.all_conv[t])):
                    Quantity.all_conv[t][f]= 1.0 / Quantity.all_conv[f][t] #inverse
        # Now expand tree by repeatedly adding two-step paths as one
        for s in Quantity.all_conv.keys():
            for m in Quantity.all_conv[s].keys():
                for e in Quantity.all_conv[m]:
                    if (not (e in Quantity.all_conv[s])):
                        Quantity.all_conv[s][e] = Quantity.all_conv[s][m] * Quantity.all_conv[m][e]
                        Quantity.all_conv[e][s] = 1.0 / Quantity.all_conv[s][e]
