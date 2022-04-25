
import traits.api as tr
from .controller import Controller

class ModelTreeNodeMixin(tr.HasTraits):
    """Base class for interactive bmcs_utils
    """

    name = tr.Str("<unnamed>")

    tree = []

    def get_tree_items(self):
        return self.tree

    tree_submodels = tr.Property(depends_on='graph_changed')
    @tr.cached_property
    def _get_tree_submodels(self):
        submodels = []
        for key in self.get_tree_items():
            trait = self.trait(key)
            if trait == None:
                raise ValueError('trait %s not found in %s' % (key, self))
            if trait.is_mapped:
                submodels.append(getattr(self, key + '_'))
            else:
                submodels.append(getattr(self, key))
        return submodels

    def get_tree_subnode(self, name):
        # Construct a tree structure of instances tagged by `tree`
        submodels = self.tree_submodels
        tree_subnodes = [
            submodel.get_tree_subnode(node_name)
            for node_name, submodel in zip(self.tree, submodels)
        ]
        return (name, self, tree_subnodes)

    as_tree_node = get_tree_subnode

