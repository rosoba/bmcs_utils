
import traits.api as tr
from bmcs_utils.app_window import AppWindow
from bmcs_utils.view import View
from bmcs_utils.i_model import IModel
from .controller import Controller

@tr.provides(IModel)
class ModelNotifyMixin(tr.HasTraits):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    children = tr.List(tr.Str, [])

    parents = tr.Set(tr.WeakRef, {})

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.register_in_children()

    state_change_debug = tr.Bool(False)

    @tr.observe('+TIME,+MESH,+MAT,+CS,+BC,+ALG,+FE,+DSC,+GEO,+ITR')
    def notify_state_change(self, event):
        if self.state_change_debug:
            print('state_changed', self, event)
        self.state_changed = True
        self.notify_parents()

    state_changed = tr.Event
    """Event used in model implementation to notify the need for update"""

    children_traits = tr.Property()
    @tr.cached_property
    def _get_children_traits(self):
        children = {}
        for key in self.children:
            trait = self.trait(key)
            if trait is None:
                raise ValueError('trait %s not found in %s' % (key, self))
            if trait.is_mapped:
                children[key] = getattr(self, key + '_')
            else:
                children[key] = getattr(self, key)
        return children

    def register_in_children(self):
        for key, child_trait in self.children_traits.items():
            child_trait.parents.add(self)
            self.observe(lambda event: self.change_parent(event), key)

    def change_parent(self, event=None):
        if self.state_change_debug:
            print('parent %s changing child from child %s to %s' % (self, event.old, event.new))
        event.old.parents.remove(self)
        event.new.parents.add(self)

    def notify_parents(self):
        for parent in self.parents:
            parent.notify_state_change('Notification from child %s' % self)

    def __del__(self):
        if self.state_change_debug:
            print('deleting %s', self)