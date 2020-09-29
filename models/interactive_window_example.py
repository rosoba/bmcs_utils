
from interactive_window import InteractiveModel, View, Item, InteractiveWindow
import traits.api as tr

class Model(InteractiveModel):

    a = tr.Float(20)
    b = tr.Float(80)

    ipw_view = View(
        Item('a', minmax=(0, 10), latex='a'),
        Item('b', minmax=(0, 10), latex='b')
    )

m = Model()
ii = InteractiveWindow(m)
print(
    ii.ipw_model_tabs[0].get_sliders()
)