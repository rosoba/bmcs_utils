'''
Matplotlib enhanced with interactive plotting using ipywidgets.

 - The IPWInteract class can generate a simple interface to a model that
   inherits from InteractiveModel. The parameters specified in `param_names`
   are included in the interactive interface.

   Further, the order of param_names can be used to transform the traits
   of the model into a tuple that calls that can be called the lambdified
   functions. This feature is useful for direct integration of function
   derived symbolically using sympy.

   @todo: define param_names as
   - ipw_interact = ['a', 'b'] as a specifier which values are to be included in the interaction
   - ipw_observe = ['d', 'e' ]

   @todo: use ipwidget metadata attribute to overload the ipw_map
'''

import ipywidgets as ipw
import ipytree as ipt
import traits.api as tr
import matplotlib.pylab as plt
import k3d
import traitlets as tl

from bmcs_utils.model_tab import ModelTab
from bmcs_utils.i_interactive_model import IInteractiveModel

class BMCSNode(ipt.Node):
    view = tl.Any

class InteractiveWindow(tr.HasTraits):
    '''Container class synchronizing the interactionjup elements with plotting area.
    It is equivalent to the traitsui.View class
    '''
    models = tr.List(IInteractiveModel)

    ipw_model_tabs = tr.List

    figsize = tr.Tuple(8, 3)

    def __init__(self, models, **kw):
        super(InteractiveWindow, self).__init__(**kw)
        if not (type(models) in [list, tuple]):
            models = [models]
        self.models = models
        self.ipw_model_tabs = [
            ModelTab(model=model, interactor=self, index=i)
            for i, model in enumerate(models)
        ]
        self.output = ipw.Output()

        self.plot_backend = self.models[0].plot_backend
        if self.plot_backend == 'mpl':
            with self.output:
                f = plt.figure(figsize=self.figsize, constrained_layout=True)
            f.canvas.toolbar_position = 'top'
            f.canvas.header_visible = False
            self.fig = f
            self.axes = self.models[0].subplots(self.fig)
        elif self.plot_backend == 'k3d':
            self.k3d_plot = k3d.plot()
            self.output.append_display_data(self.k3d_plot)
            self.models[0].subplots(k3d.plot())
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

    def __del__(self):
        plt.close(self.fig)

    plot_pane_layout = tr.Property
    @tr.cached_property
    def _get_plot_pane_layout(self):
        return ipw.Layout(
            border='solid 1px black',
            margin='0px 5px 5px 0px',
            padding='1px 1px 1px 1px',
            width="100%"
        )

    def interact(self):
        left_pane_layout = ipw.Layout(
            border='solid 1px black',
            margin='0px 5px 5px 0px',
            padding='1px 1px 1px 1px',
            width="200px",
            flex_grow="1",
        )
        left_pane = ipw.VBox([self.tree, self.edit_frame],
                             layout=left_pane_layout)
        self.output.layout = self.plot_pane_layout
        vb = ipw.HBox([left_pane, self.output])
        display(vb)

    def app(self):
        left_pane_layout = ipw.Layout(
            border='solid 1px black',
            margin='0px 5px 5px 0px',
            padding='1px 1px 1px 1px',
            width="200px",
            flex_grow="1",
        )
        left_pane = ipw.VBox([self.tree, self.edit_frame],
                             layout=left_pane_layout)
        self.output.layout = self.plot_pane_layout
        vb = ipw.HBox([left_pane, self.output],
                      label=ipw.Layout(width="100%"))

        self.tool_bar = ipw.HBox(layout=ipw.Layout(
            height="40px", width="100%",
            border='solid 1px black',
            margin='0px 5px 5px 0px',
            padding='1px 1px 1px 1px',
        ))
        app = ipw.VBox([self.tool_bar, vb],
                      label=ipw.Label(align_items="stretch",
                                      width="100%"))
        display(app)

    tree = tr.Property # might depend on the model
    @tr.cached_property
    def _get_tree(self):
        # provide a method scanning the tree of the model
        # components
        tree_layout = ipw.Layout(display='flex',
                            flex_flow='column',
                            align_items='flex-start',
                            width='100%')
        tree = ipt.Tree(layout=tree_layout)
        for elem in self.ipw_model_tabs:
            node = BMCSNode(elem.model.name, view=elem)
            node.observe(self.select_node, 'selected')
            tree.add_node(node)
        return tree

    edit_frame = tr.Property # should depend on the model
    @tr.cached_property
    def _get_edit_frame(self):
        return ipw.Box()

    def select_node(self, event):
        node = event['owner']
        elem = node.view
        self.elem = elem
        self.tool_bar = elem.tool_bar
        widget_container = elem.widget_container
        self.edit_frame.children = widget_container.children
        self.replot(elem.model)

    def replot(self, model):
        # clean k3d
        if self.plot_backend == 'mpl':
            self.update_plot(model)
        if self.plot_backend == 'k3d':
            # TODO: why the first loop is not removing all the objects! clean this!
            for obj in self.k3d_plot.objects:
                self.k3d_plot -= obj
            for obj in self.k3d_plot.objects:
                self.k3d_plot -= obj
            model.plot_k3d(self.k3d_plot)

    def update_plot(self, model):
        if self.plot_backend == 'mpl':
            """update the visualization with updated bmcs_utils"""
            self.fig.clf()
            self.axes = model.subplots(self.fig)
            _axes = self.axes
            if not hasattr(_axes, '__iter__'):
                _axes = [_axes]
            for ax in _axes:
                ax.clear()
            model.update_plot(self.axes)
            # if len(self.tab.children) > index:
            #     self.tab.selected_index = index
            self.fig.canvas.draw()
        elif self.plot_backend == 'k3d':
            # TODO: why the first loop is not removing all the objects! clean this!
            model.update_plot(self.k3d_plot)
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

