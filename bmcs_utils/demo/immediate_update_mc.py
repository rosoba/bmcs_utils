from bmcs_utils.trait_types import \
    Float, Int, Bool, FloatRangeEditor, Instance, Range, ProgressEditor, FloatEditor
from bmcs_utils.interactive_model import InteractiveModel
from bmcs_utils.item import Item
from bmcs_utils.view import View
import numpy as np
import time
import traits.api as tr

class InterimModelComponent(InteractiveModel):
    """Example model with a cross sectional shape"""
    name = 'Inbetween'

    b = Int(5, desc='input parameter')
    c = Bool(True)
    t = Float(0)
    t_max = Float(10)
    sim_stop = Bool(False)

    a = Float(0.0, desc=r'first material parameter')
    kappa_slider = Float(0.0000001)

    ipw_view = View(
        Item('b', latex=r'\beta', readonly=True),
        Item('t_max', latex=r'\theta'),
        Item('c', latex=r'\gamma'),
        Item('a', latex=r'a', editor=FloatRangeEditor(low=0, high=20, n_steps=100)),
        Item('kappa_slider', latex='\kappa', editor=FloatRangeEditor(low=0, high=20, n_steps=100)),
        Item('shape'),  # editor=SelectionEditor(options_trait='options')),
    )

    def subplots(self, fig):
        axes = fig.subplots(1,1)
        axes.set_ylim(ymin=-1.05, ymax=1.05)
        axes.set_xlim(xmin=0, xmax=self.t_max)
        return axes

    def update_plot(self, axes):
        t_arr = np.linspace(0, self.t, 100)
        axes.plot(t_arr, np.sin(t_arr) )

