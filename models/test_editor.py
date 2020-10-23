from traits.api import Float, BaseFloat, HasTraits, TraitError


class XFloat(BaseFloat):

    def create_editor(self):
        print('xxx')


f = XFloat()
f.create_editor()


class ExampleModel(HasTraits):
    a = XFloat(0)


example_model = ExampleModel()
print(example_model.trait('a'))
print(example_model.trait('a').trait_type)
example_model.trait('a').trait_type.create_editor()
