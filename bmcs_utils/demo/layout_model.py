from bmcs_utils.trait_types import \
    Float, Int, Bool, FloatRangeEditor, Instance, Range, ProgressEditor, FloatEditor
from bmcs_utils.model import Model
from bmcs_utils.item import Item
from bmcs_utils.view import View
import numpy as np
import time
import traits.api as tr

class LayoutModel(Model):
    """Example model of a cross sectional area"""
    name = 'Layout'

    n = Int(5, desc='number of layers')
    A = Float(2, desc='area')

    ipw_view = View(
        Item('n', latex=r'n'),
        Item('A', latex=r'A'),
    )

    def subplots(self, fig):
        axes = fig.subplots(1,1)
        return axes

    def update_plot(self, axes):
        x = np.linspace(0,1,self.n)
        axes.plot(x,np.zeros_like(n),marker='o')

