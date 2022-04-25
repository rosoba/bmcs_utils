
import traits.api as tr

class ModelNotifyMixin(tr.HasTraits):
    """Mixin for notifications
    """

    name = tr.Str("<unnamed>")

    depends_on = tr.List(tr.Str, [])

    children = tr.List(tr.Str, [])

    parents = tr.Set(tr.WeakRef, {})

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.register_in_children()

    state_change_debug = tr.Bool(False)

    @tr.observe('+TIME,+MESH,+MAT,+CS,+BC,+ALG,+FE,+DSC,+GEO,+ITR')
    def notify_value_change(self, event):
        if self.state_change_debug:
            print('value_changed', self, event)
        self.value_changed = True
        self.state_changed = True
        self.notify_parents_value_changed()

    def notify_graph_change(self, event):
        if self.state_change_debug:
            print('graph_changed', self, event)
        self.graph_changed = True
        self.state_changed = True
        self.notify_parents_graph_changed()

    value_changed = tr.Event
    graph_changed = tr.Event
    state_changed = tr.Event

    """Event used in model implementation to notify the need for update"""

    children_traits = tr.Property()
    @tr.cached_property
    def _get_children_traits(self):
        children_traits = {}
        for key in self.children:
            trait = self.trait(key)
            if trait is None:
                raise ValueError('trait %s not found in %s' % (key, self))
            if trait.is_mapped:
                children_traits[key] = getattr(self, key + '_')
            else:
                children_traits[key] = getattr(self, key)
        return children_traits

    def register_in_children(self):
        for key, child_trait in self.children_traits.items():
            child_trait.parents.add(self)
            self.observe(lambda event: self.change_parent(event), key)

    def change_parent(self, event=None):
        if self.state_change_debug:
            print('parent %s changing child from child %s to %s' % (self, event.old, event.new))
        event.old.parents.remove(self)
        event.new.parents.add(self)
        self.notify_graph_change('Notification from child %s' % event.new)

    def notify_parents_graph_changed(self):
        for parent in self.parents:
            if parent: # ignore if parent is garbage collected
                parent.notify_graph_change('Notification from child %s' % self)

    def notify_parents_value_changed(self):
        for parent in self.parents:
            if parent: # ignore if parent is garbage collected
                parent.notify_value_change('Notification from child %s' % self)

    def __del__(self):
        if self.state_change_debug:
            print('deleting %s', self)