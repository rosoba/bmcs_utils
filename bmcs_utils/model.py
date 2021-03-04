
import traits.api as tr
from bmcs_utils.app_window import AppWindow
from bmcs_utils.i_model import IModel
from .controller import Controller

import k3d

@tr.provides(IModel)
class Model(tr.HasTraits):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    def get_controller(self, app_window):
        return Controller(model=self, app_window=app_window)

    plot_backend = 'mpl'
    """"plot_backend = 'mpl' or 'k3d'"""

    def subplots(self, fig):
        if self.plot_backend == 'mpl':
            return fig.subplots(1, 1)
        elif self.plot_backend == 'k3d':
            return fig
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

    def plot(self, axes):
        """Alias to update plot - to be overloaded by subclasses"""
        self.update_plot(axes)

    def update_plot(self, axes):
        raise NotImplementedError()

    def interact(self,**kw):
        return AppWindow(self,**kw).interact()

    def app(self,**kw):
        return AppWindow(self,**kw).interact()

# backward compatibility
InteractiveModel = Model