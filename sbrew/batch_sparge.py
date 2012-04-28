from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from lauter import Lauter

class BatchSparge(Lauter):
    """Batch sparge, a special type of lauter

    """

    def __init__(self, **kwargs):
        print "batch sparge __init__" + str(kwargs)
        super(BatchSparge, self).__init__(**kwargs)
        self.name='batch sparge'


