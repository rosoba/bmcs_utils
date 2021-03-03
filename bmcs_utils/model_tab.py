import traits.api as tr
from bmcs_utils.i_interactive_model import IInteractiveModel
import ipywidgets as ipw


class ModelTab(tr.HasTraits):
    '''Base class for tabs within an interaction window.'''

    index = tr.Int

    model = tr.Instance(IInteractiveModel)

    interactor = tr.WeakRef

    def set_interactor(self, interactor):
        self.interactor = interactor

    n_steps = tr.Int(20)

    freeze_editors = tr.Bool(False)

    def ipw_editor_changed(self, change):
        if self.freeze_editors:
            return

        name = change.owner.name
        val = change.new
        keyval = {name: val}
        self.model.trait_set(**keyval)
        ipw_view = self.model.ipw_view
        if not ipw_view.simulator:
            # If there is a simulator defined within the model
            # do not automatically update the plot. The plot event
            # is then triggered by the simulator itself.
            self.interactor.update_plot(self.model)

    def notify_change(self, event):
        value = event.new
        ipw_editor = self.ipw_editors[event.name]
        self.freeze_editors = True
        ipw_editor.value = value
        self.freeze_editors = False

    tool_bar = tr.Property
    @tr.cached_property
    def _get_tool_bar(self):
        ipw_view = self.model.ipw_view
        return ipw_view.get_tool_bar(model=self.model, ui_pane=self)

    widget_container = tr.Property
    @tr.cached_property
    def _get_widget_container(self):
        return self.widget_layout()

    def widget_layout(self):
        ipw_view = self.model.ipw_view
        frame, ipw_editors = ipw_view.get_view_layout(model=self.model,
                                                      ui_pane=self)
        self.ipw_editors = ipw_editors
        return frame

    def xwidget_layout(self):

        vlist = []

        editors = self.model.ipw_view.get_editors(self.model, self)

        self.ipw_editors = {}
        for name, editor in editors.items():
            ipw_editor = editor.render()
            ipw_editor.name = name
            ipw_editor.observe(self.ipw_editor_changed, 'value')
            self.ipw_editors[name] = ipw_editor
            editor.model.observe(self.notify_change, name)

        # Originally, the interactive_output widget was used
        # here. But in this way, the update method was called
        # earlier than the tab change observer of the interactor
        # This caused problems if axes object did not correspond
        # to the model's update_plot method. Therefore,
        # slider observer is now used , augmented with the trait name.
        # out = ipw.interactive_output(self.update, sliders);

        ipw_view = self.model.ipw_view
        item_names = ipw_view.item_names
        ipw_editors_list = [self.ipw_editors[name] for name in item_names]
        layout = ipw.Layout(grid_template_columns='1fr 1fr', padding='6px', width='100%')
        grid = ipw.GridBox(ipw_editors_list, layout=layout)

        vlist.append(grid)
        frame = ipw.VBox(vlist)
        return frame

    def plot_k3d(self, k3d_plot):
        self.model.plot_k3d(k3d_plot)

    def subplots(self, fig):
        return self.model.subplots(fig)

    def update_plot(self, axes):
        self.model.update_plot(axes)
