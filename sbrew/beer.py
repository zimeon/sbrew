"""Model for Beer, the end product."""
from .recipe import Recipe
from .ingredient import Ingredient
from .quantity import Quantity
from .property import Property


class Beer(Recipe):
    """A placeholder recipe to express final details of beer."""

    DEFAULT_NAME = 'beer'

    def __init__(self, name=None, **kwargs):
        """Initialize Beer object."""
        super(Beer, self).__init__(**kwargs)

    def import_forward(self):
        """Import properties from previous step."""
        self.import_property('OG')
        self.import_property('IBU')
        self.import_property('ABV')
        self.import_property('SRM')

    def solve(self):
        """Calculate the ABV and attenuation based on OG and FG."""
        pass

    def end_state_str(self):
        """Summary string."""
        self.solve()
        s = ''
        if ('ABV' in self.properties):
            s += str(self.property('ABV').quantity)
        return(s)
