
import traits.api as tr
from bmcs_utils.app_window import AppWindow
from bmcs_utils.i_model import IModel
from .controller import Controller

@tr.provides(IModel)
class Model(tr.HasTraits):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    def __init__(self,*args,**kw):
        super().__init__(*args, **kw)
        self.update_observers()

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

    @tr.observe('+tree')
    def _notify_tree_change(self, event):
        self.tree_changed = True
        self.update_observers()

    tree_changed = tr.Event

    def get_sub_node(self, name):
        # Construct a tree structure of instances tagged by `tree`
        node_dict = self.traits(tree=True)
        sub_nodes = []
        for node_name, trait in node_dict.items():
            if trait.is_mapped:
                sub_model = getattr(self, node_name + '_')
            else:
                sub_model = getattr(self, node_name)
            sub_nodes.append(sub_model.get_sub_node(node_name))
        return (name, self, sub_nodes)

    as_node = get_sub_node

    @tr.observe('+MAT,+CS,+BC,+ALG, +FE, +DSC, +GEO')
    def notify_state_change(self, event):
        print('state_change', self)
        self.state_changed = True

    state_changed = tr.Event

    def update_observers(self):
        name, model, nodes = self.as_node('root')
        for sub_name, sub_model, sub_nodes in nodes:
            sub_model.observe(model.notify_state_change,'state_changed')

# backward compatibility
InteractiveModel = Model