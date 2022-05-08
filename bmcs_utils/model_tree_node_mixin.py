
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
        for name in self.get_tree_items():
            trait = self.trait(name)
            name_ = trait.trait_type.get_name_(name)
            trait_ = getattr(self, name_, None)
            if trait_ == None:
                raise ValueError('trait %s not found in %s' % (name_, self))
            submodels.append(trait_)
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

