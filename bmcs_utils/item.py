
import traits.api as tr

class Item(tr.HasTraits):
    """Item of interaction with a model
    """
    name = tr.Str
    latex = tr.Str
    readonly = tr.Bool

    editor = None
    '''Overload the editor defined in the trait type'''

    def __init__(self, name, **traits):
        self.name = name
        tr.HasTraits.__init__(self, **traits)

    def get_editor(self, value, trait, model):
        if self.editor:
            editor = self.editor
        elif trait.trait_type.editor_factory is None:
            raise TypeError(f'no editor attribute {self.name} in {model}, maybe not declared?')
        else:
            editor = trait.trait_type.editor_factory()
        # use the editor supplied in the item defintion and set its attributes
        editor.name = self.name

        if not editor.label:
            editor.label = r'\(%s\)' % self.latex if self.latex else self.name
        editor.tooltip = desc if (desc := trait.desc) else self.name
        editor.value = value
        editor.trait = trait
        editor.model = model
        editor.disabled = self.readonly
        return editor
