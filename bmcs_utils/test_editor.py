from bmcs_utils.trait_types import \
    Float, Int, Bool, FloatRangeEditor, Range
from bmcs_utils.interactive_model import InteractiveModel
from bmcs_utils.item import Item
from bmcs_utils.view import View
import numpy as np
import time

class ExampleModel(InteractiveModel):
    name = 'Example'

    a = Float(0, desc=r'first material parameter')
    b = Int(5, desc='input parameter')
    c = Bool(True)
    t = Float(0)
    t_max = Float(10)

    ipw_view = View(
        Item('a', editor=FloatRangeEditor(low=0, high=10)),
        Item('b', latex=r'\beta', readonly=True),
        Item('t', latex=r'\theta', editor=FloatRangeEditor(low=0, high_name='t_max')),
        Item('t_max', latex=r'\theta'),
        Item('c', latex=r'\gamma'),
        simulator='run',
        time_variable='t',
        time_max='t_max',
        reset_simulator='reset'
    )

    def run(self):
        print('where are you')
        self.a += 1
        t_arr = np.linspace(0, self.t_max, 10)
        for t in t_arr:
            time.sleep(1)
            self.t = t

    def reset(self):
        print('reset called')
        self.trait_set(a=0, b=5, c=True, t=0)

    def update_plot(self, axes):
        print('update_plot called')
        trait_names = self.trait_names()
        print(self.trait_get(trait_names))

# ex = ExampleModel()
# ex.interact()
# ex.run()
