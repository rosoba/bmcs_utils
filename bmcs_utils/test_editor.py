from bmcs_utils.trait_types import \
    Float, Int, Bool, FloatRangeEditor, Range, ProgressEditor
from bmcs_utils.interactive_model import InteractiveModel
from bmcs_utils.item import Item
from bmcs_utils.view import View
import numpy as np
from traits.api import Event
import time

class ExampleModel(InteractiveModel):
    name = 'Example'

    a = Float(0, desc=r'first material parameter')
    b = Int(5, desc='input parameter')
    c = Bool(True)
    t = Float(0)
    t_max = Float(10)
    sim_stop = Bool(False)

    ipw_view = View(
        Item('t', editor=ProgressEditor(run_simulator='run',
                                        reset_simulator='reset',
                                        interrupt_simulator='sim_stop',
                                        time_variable='t',
                                        time_max='t_max',
                                        )
             ),
        Item('a', editor=FloatRangeEditor(low=0, high=10)),
        Item('b', latex=r'\beta', readonly=True),
        Item('t_max', latex=r'\theta'),
        Item('c', latex=r'\gamma'),
    )

    def run(self):
        self.a += 1
        t_arr = np.linspace(self.t, self.t_max, 50)
        for t in t_arr:
            # allow for the interference by the editor
            if self.sim_stop:
                break
            time.sleep(0.1)
            self.t = t

    def reset(self):
        self.trait_set(a=0, b=5, c=True, t=0)

    def subplots(self, fig):
        axes = fig.subplots(1,1)
        axes.set_ylim(ymin=-1.05, ymax=1.05)
        axes.set_xlim(xmin=0, xmax=self.t_max)
        return axes

    def update_plot(self, axes):
        t_arr = np.linspace(0, self.t, 100)
        axes.plot(t_arr, np.sin(t_arr) )

