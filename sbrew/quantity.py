import re

class ConversionError(Exception):
    pass;

class Quantity:
    """Base class for all quantities.

    All quantities have a value and a unit.
    """

    CONVERSIONS = { 
        '%ABW' : { '%ABV' : 1.25 },
        'oz'  : { 'lb' : 1.0/16.0,
                  'kg' : 0.0283495231,
                  'g'  : 28.3495231 },
        'gal' : { 'pt' : 8.0,
                  'qt' : 4.0,
                  'l'  : 3.78541,
                  'dl' : 37.8541,
                  'cl' : 378.541,
                  'ml' : 3785.41 },
        'J'   : { 'Joule' : 1.0,
                  'kJ' : 0.001,
                  'Btu' : 0.0009478 },
        'points' : { },
        'Btu/lb/F' : { 'kJ/kg/F' : 2.324444 },
        'h'   : { 'min' : 60,
                  's'   : 3600 },
        }

    DISPLAY_FMT = {
        '%ABV' : '%.1f',
        '%ABW' : '%.1f',
        '%atten' : '%.1f',
        'Btu/F' : '%.2f',
        'F' : '%.1f',
        'gal' : '%.2f',
        'psi' : '%.1f',
        'points' : '%.1f',
        'min' : '%d',
        'og' : '%.3f',
        'sg' : '%.3f',
        'oz' : '%.2f',
        'IBU' : '%.1f',
        }

    CANONICAL_UNIT = {
        'gal/hour': 'gal/h',
        'hour'    : 'h',
        }

    ALL_CONV = None

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
        elif (self.unit in Quantity.DISPLAY_FMT):
            return( (Quantity.DISPLAY_FMT[self.unit] % self.value) + " " + str(self.unit))
        else:
            return(str(self.value) + " " + str(self.unit))

    def __repr__(self):
        if (self.value is None):
            return("QuantityNotDefined")
        elif (self.unit is None):
            return(str(self.value))
        else:
            return(str(self.value) + str(self.unit))

    @staticmethod
    def canonical_unit(unit):
        """Convert unit string to canonical form if recognized but in another form"""
        if (unit in Quantity.CANONICAL_UNIT):
            return Quantity.CANONICAL_UNIT[unit]
        return unit

    def to(self,new_unit):
        """Get value of this quantity in a specific unit.

        Uses conversions in CONVERSIONS dictionary of dictionaries
        to look up conversion factors. At present not smart enough
        to find a chain between two units but that should be possible
        add.

        e.g. lbs = weight.to('lb')
             temp=Quantity('10C')
             f = temp.to('F')
        """
        # Make sure new_unit is canonical
        new_unit=self.canonical_unit(new_unit)
        # Convert
        if (self.unit==new_unit):
            return(self.value)
        elif (self.unit in Quantity.CONVERSIONS and
                new_unit in Quantity.CONVERSIONS[self.unit]):
            return(self.value*Quantity.CONVERSIONS[self.unit][new_unit])
        elif (new_unit in Quantity.CONVERSIONS and
                self.unit in Quantity.CONVERSIONS[new_unit]):
            #inverse
            return(self.value/Quantity.CONVERSIONS[new_unit][self.unit])
        else:
            return(self.value * self.find_conversion(self.unit,new_unit))

    def convert_to(self,new_unit):
        """Convert internal value to the new unit

        Piggbybacks on the to() method but changes the internal
        representation. Returns self.
        """
        # Make sure new_unit is canonical
        new_unit=self.canonical_unit(new_unit)
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
        if (Quantity.ALL_CONV is None):
            Quantity.build_ALL_CONV()
        if (not (from_unit in Quantity.ALL_CONV)):
            raise ConversionError('unknown original unit in conversion requested from %s to %s' % (from_unit, to_unit))
        if (not (to_unit in Quantity.ALL_CONV)):
            raise ConversionError('unknown destination unit in conversion requested from %s to %s' % (from_unit,to_unit))
        if (not (to_unit in Quantity.ALL_CONV[from_unit])):
            raise ConversionError('unknown conversion requested from %s to %s' % (from_unit,to_unit))
        return(Quantity.ALL_CONV[from_unit][to_unit])

    @staticmethod
    def build_ALL_CONV():
        # Expand tree of all CONVERSIONS (include sanity check to 
        # avoid possible cycles)
        #
        # Build local self.conv with data from Quantity.CONVERSIONS and inverses
        Quantity.ALL_CONV={}
        for f in Quantity.CONVERSIONS:
            Quantity.ALL_CONV[f]={}
            for t in Quantity.CONVERSIONS[f]:
                Quantity.ALL_CONV[f][t]=Quantity.CONVERSIONS[f][t]
                if (not (t in Quantity.CONVERSIONS)):
                    Quantity.ALL_CONV[t]={}
                if (not (f in Quantity.ALL_CONV[t])):
                    Quantity.ALL_CONV[t][f]= 1.0 / Quantity.ALL_CONV[f][t] #inverse
        # Now expand tree by repeatedly adding two-step paths as one
        for s in Quantity.ALL_CONV.keys():
            for m in Quantity.ALL_CONV[s].keys():
                for e in Quantity.ALL_CONV[m]:
                    if (not (e in Quantity.ALL_CONV[s])):
                        Quantity.ALL_CONV[s][e] = Quantity.ALL_CONV[s][m] * Quantity.ALL_CONV[m][e]
                        Quantity.ALL_CONV[e][s] = 1.0 / Quantity.ALL_CONV[s][e]

