
import traits.api as tr
from bmcs_utils.item import Item
import ipywidgets as ipw
import time

class View(tr.HasTraits):
    """Container of IPWItems
    """
    content = tr.List(Item)
    item_names = tr.List(tr.Str)

    # -------------------------------------------------------------------------
    #  Initializes the object:
    # -------------------------------------------------------------------------

    def __init__(self, *values, **traits):
        """ Initializes the object.
        """
        tr.HasTraits.__init__(self, **traits)
        for item in values:
            self.content.append(item)
            self.item_names.append(item.name)


    def get_editors(self, model, ui_pane):
        """Return a list of editors linked to a model ordered
        according to the view specification"""
        item_names = self.item_names
        items = self.content
        # The traits named in ipw_view are fetched from the model
        # one could directly call `traits` - but then also transient
        # traits like properties would be accessed. This would disable
        # lazy evaluation of properties.
        # Using the self.traits(transient=is_none) does not work either
        # as then no Buttons could be used - they are also transient.
        # The result is a three step retrieval
        # 1) - use trait_get to obtain the values, transient values are empty
        values = [model.trait_get(name) for name in item_names]
        # 2) - convert the list of dictionaries to a single dictionary
        val_dict = {k: v for d in values for k, v in d.items()}
        # 3) - construct a list ordered according to `item_names` with
        #      values of transient traits set to none
        values_ = [val_dict.get(name, None) for name in item_names]
        # 4) - order the corresponding traits according item_names
        traits_ = [model.trait(name) for name in item_names]
        # construct a dictionary of editors that can be rendered
        editors = {
            item.name: item.get_editor(value_, trait_, model)
            for (item, trait_, value_) in
            zip(items, traits_, values_)
        }
        for editor in editors.values():
            editor.ui_pane = ui_pane
        return editors

    def get_view_layout(self, model, ui_pane):
        vlist = []
        editors = self.get_editors(model, ui_pane)
        ipw_editors = {}
        for name, editor in editors.items():
            ipw_editor = editor.render()
            ipw_editor.name = name
            ipw_editor.observe(ui_pane.ipw_editor_changed, 'value')
            ipw_editors[name] = ipw_editor
            editor.model.observe(ui_pane.notify_change, name)

        # Originally, the interactive_output widget was used
        # here. But in this way, the update method was called
        # earlier than the tab change observer of the interactor
        # This caused problems if axes object did not correspond
        # to the model's update_plot method. Therefore,
        # slider observer is now used , augmented with the trait name.
        # out = ipw.interactive_output(self.update, sliders);

        item_names = self.item_names
        ipw_editors_list = [ipw_editors[name] for name in item_names]
        box_layout = ipw.Layout(display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            width='100%')

        items_layout = ipw.Layout(width='auto')  # override the default width of the button to 'auto' to let the button grow
        for ipw_editor in ipw_editors_list:
            ipw_editor.layout = items_layout

        box = ipw.VBox(ipw_editors_list, layout=box_layout)

        vlist.append(box)
        frame = ipw.VBox(vlist, layout=box_layout)
        return frame, ipw_editors

    def get_tool_bar(self, model, ui_pane):
        return


class SimView(View):

    simulator = tr.Str
    """Name of the method running the model simulation
    """

    reset_simulator = tr.Str
    """Name of the method resetting the model simulation
    """

    time_change_notifier = tr.Str
    """Name of a trait that can be used by the ui 
    to register time update method
    """

    time_range_change_notifier = tr.Str
    """Name of a trait that can be used by the ui 
    to register time range update method
    """

    def get_tool_bar(self, model, ui_pane):
        pass