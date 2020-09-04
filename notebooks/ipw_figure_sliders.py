import ipywidgets as ipw
import traits.api as tr

class IInteractiveModel(tr.Interface):
    '''Base class for interactive models'''

@tr.provides(IInteractiveModel)
class InteractiveModel(tr.Interface)

class IPWFigureWithSliders(tr.HasTraits):
    '''Model showing the max of the quadratic function'''

    model = tr.Instance(IInteractiveModel)

    def __init__(self, *args, **kw):
        super(IPWFigureWithSliders, self).__init__(*args, **kw)
        self.model.init_plot()

    def interact(self):
        sliders = self.get_sliders()
        out = ipw.interactive_output(self.update, sliders);
        self.widget_layout(out, sliders)

    n_steps = tr.Int(20)

    def get_sliders(self):
        param_names = self.model.param_names
        traits = self.model.traits(param=True)
        vals = self.model.trait_get(param=True)
        val_ = [vals[name] for name in param_names]
        minmax_ = [getattr(traits[name], 'minmax', 2) for name in param_names]
        latex_ = [getattr(traits[name], 'latex', r'<none>') for name in param_names]
        return {name: ipw.FloatSlider(
            value=val, min=minmax[0], max=minmax[1],
            step=(minmax[1] - minmax[0]) / self.n_steps,
            continuous_update=False,
            description=r'\(%s\)' % latex)
            for (name, val, latex, minmax) in
            zip(param_names, val_, latex_, minmax_)
        }

    def update(self, **values):
        self.model.trait_set(**values)
        self.model.update_plot()

    def widget_layout(self, out, sliders):
        layout = ipw.Layout(grid_template_columns='1fr 1fr')
        param_names = self.model.param_names
        param_sliders_list = [sliders[name] for name in param_names]
        grid = ipw.GridBox(param_sliders_list, layout=layout)
        box = ipw.VBox([grid, out])
        display(box)

    def init_plot(self):
        self.model.init_plot()

    def update_plot(self):
        self.model.update_plot()