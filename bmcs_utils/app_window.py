'''
Application Window for as a user interface to implemented models within Jupyter

 - The AppWindow class can generate a user interface to a model.
   It generates the interface based on the specified views and handlers
   provided by the model.

'''

import ipywidgets as ipw
import ipytree as ipt
import traits.api as tr
import matplotlib.pylab as plt
import k3d
from .tree_node import BMCSNode

from bmcs_utils.i_model import IModel

class AppWindow(tr.HasTraits):
    '''Container class synchronizing the interactionjup elements with plotting area.
    It is equivalent to the traitsui.View class
    '''
    model = tr.Instance(IModel)

    figsize = tr.Tuple(8, 3)

    def __init__(self, model, **kw):
        super(AppWindow, self).__init__(**kw)
        self.model = model
        self.output = ipw.Output()

        self.plot_backend = self.model.plot_backend
        if self.plot_backend == 'mpl':
            with self.output:
                f = plt.figure(figsize=self.figsize, constrained_layout=True)
            f.canvas.toolbar_position = 'top'
            f.canvas.header_visible = False
            self.fig = f
            self.axes = self.model.subplots(self.fig)
        elif self.plot_backend == 'k3d':
            self.k3d_plot = k3d.plot()
            self.output.append_display_data(self.k3d_plot)
            self.model.subplots(k3d.plot())
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

    def __del__(self):
        plt.close(self.fig)

    # Shared layouts
    left_pane_layout = tr.Instance(ipw.Layout)
    def _left_pane_layout_default(self):
        return ipw.Layout(
            #border='solid 1px black',
            margin='0px 0px 0px 0px',
            padding='0px 0px 0px 0px',
            width="300px",
            flex_grow="1",
        )

    right_pane_layout = tr.Instance(ipw.Layout)
    def _right_pane_layout_default(self):
        return ipw.Layout(
            border='solid 1px black',
            margin='0px 0px 0px 5px',
            padding='1px 1px 1px 1px',
            width="100%",
            flex_grow="1",
        )

    output_pane_layout = tr.Instance(ipw.Layout)
    def _output_pane_layout_default(self):
        return ipw.Layout(
            margin='0px 0px 0px 0px',
            padding='1px 1px 1px 1px',
            width="100%"
        )

    def interact(self):
        left_pane = ipw.VBox([self.tree_pane, self.model_editor_pane],
                             layout=self.left_pane_layout)
        self.output.layout = self.output_pane_layout
        right_pane = ipw.VBox([self.output, self.time_editor_pane],
                               layout=self.right_pane_layout)
        app = ipw.HBox([left_pane, right_pane],
                        layout=ipw.Layout(align_items="stretch",
                                          width="100%"))
        display(app)

    def get_tree(self):
        tree = self.model.get_sub_node(self.model.name)
        return self.get_tree_entries(tree)

    def get_tree_entries(self, node):
        name, model, sub_nodes = node
        bmcs_sub_nodes = [
            self.get_tree_entries(sub_node) for sub_node in sub_nodes
        ]
        node_ = BMCSNode(name, nodes=tuple(bmcs_sub_nodes),
                         controller=model.get_controller(self))
        node_.observe(self.select_node, 'selected')
        def update_node(event):
            '''upon tree change - rebuild the subnodes'''
            new_node = model.get_sub_node(model.name)
            new_node_ = self.get_tree_entries(new_node)
            node_.nodes = new_node_.nodes
            # are the original nodes deleted? memory leak?
        model.observe(update_node, 'tree_changed')
        return node_

    tree_pane = tr.Property # might depend on the model
    @tr.cached_property
    def _get_tree_pane(self):
        # provide a method scanning the tree of the model
        # components
        tree_layout = ipw.Layout(display='flex',
                                 overflow_y='scroll',
                                 flex_flow='column',
                                 border='solid 1px black',
                                 margin='0px 5px 5px 0px',
                                 padding='1px 1px 1px 1px',
                                 align_items='stretch',
                                 flex_grow="2",
                                 height="40%",
                                 width='100%')

        tree_pane = ipt.Tree(layout=tree_layout)
        root_node = self.get_tree()
        tree_pane.nodes = (root_node,)
        root_node.selected = True
        return tree_pane

    model_editor_pane = tr.Property # should depend on the model
    @tr.cached_property
    def _get_model_editor_pane(self):
        editor_pane_layout = ipw.Layout(
            display='flex',
            border='solid 1px black',
            overflow_y='scroll',
            justify_content='space-between',
            flex_flow='column',
            padding='5px 5px 5px 5px',
            margin='0px 5px 0px 0px',
            align_items='flex-start',
            height="60%", width='100%')
        return ipw.VBox(layout=editor_pane_layout)

    time_editor_pane_layout = tr.Instance(ipw.Layout)
    def _time_editor_pane_layout_default(self):
        return ipw.Layout(
            height="35px", width="100%",
            margin='0px 0px 0px 0px',
            padding='0px 0px 0px 0px',
        )

    time_editor_pane = tr.Property # should depend on the model
    @tr.cached_property
    def _get_time_editor_pane(self):
        return ipw.VBox(layout=self.time_editor_pane_layout)

    def select_node(self, event):
        node = event['owner']
        controller = node.controller
        self.controller = controller
        time_editor = controller.time_editor
        self.time_editor_pane.children = time_editor
        model_editor = controller.model_editor
        self.model_editor_pane.children = model_editor.children
        # with self.output:
        #     print('update plot', node)
        self.replot(controller.model)

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
            # with self.output:
            #     print('model.update', model)
            model.update_plot(self.axes)
            # if len(self.tab.children) > index:
            #     self.tab.selected_index = index
            self.fig.canvas.draw()
        elif self.plot_backend == 'k3d':
            # TODO: why the first loop is not removing all the objects! clean this!
            model.update_plot(self.k3d_plot)
        else:
            raise NameError(self.plot_backend + ' is not a valid plot_backend!')

# backward compatibility
InteractiveWindow = AppWindow