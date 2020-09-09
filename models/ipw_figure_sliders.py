import ipywidgets as ipw
import traits.api as tr
import matplotlib.pylab as plt

get_params_tuple = lambda param_names, **kw: tuple(kw[name] for name in param_names)


class IInteractiveModel(tr.Interface):
    '''Interface of interactive models'''


@tr.provides(IInteractiveModel)
class InteractiveModel(tr.HasTraits):
    '''Base class for interactive models'''

    name = tr.Str("<unnamed>")

    param_names = tr.List(tr.Str,[])

    def get_params(self):
        param_dict = self.trait_get(param=True)
        params = get_params_tuple(self.param_names, **param_dict)
        return params

    def subplots(self):
        return plt.subplots(1, 1, figsize=(7, 4), tight_layout=True)


class IPWElement(tr.HasTraits):
    '''Base class for interaction elements.'''
    index = tr.Int

class IPWInteract(tr.HasTraits):
    '''Container class synchronizing the interaction elements with plotting area.
    '''
    models = tr.List(InteractiveModel)

    ipw_elements = tr.List(IPWElement)

    figsize = tr.Tuple(8,3)

    def __init__(self, models, **kw):
        super(IPWInteract, self).__init__(**kw)
        if not (type(models) in [list, tuple]):
            models = [models]
        self.models = models
        self.ipw_elements = [
            IPWModelSliders(model=model, interactor=self, index=i)
            for i, model in enumerate(models)
        ]
        self.fig = plt.figure(figsize=self.figsize,
                              constrained_layout=True)
        self.axes = self.models[0].subplots(self.fig)

    def interact(self):
        tab = self.widget_layout()
        display(tab)

    def widget_layout(self):
        self.tab = ipw.Tab()
        keyval = [(elem.model.name, elem) for elem in self.ipw_elements]
        self.tab.children = tuple(value.widget_layout() for _, value in keyval)
        [self.tab.set_title(i, key) for i, (key, val) in enumerate(keyval)]
        self.tab.observe(self.change_tab,'selected_index')
        self.change_tab()
        return self.tab

    def change_tab(self, change=None):
        index = self.tab.selected_index
        self.fig.clf()
        self.axes = self.models[index].subplots(self.fig)
        self.update_plot(index)

    def update_plot(self, index):
        '''update the visualization with updated models'''
        _axes = self.axes
        if not hasattr(_axes,'__iter__'):
            _axes = [_axes]
        for ax in _axes:
            ax.clear()
        self.ipw_elements[index].update_plot(self.axes)
        if len(self.tab.children) > index:
            self.tab.selected_index=index


class IPWModelSliders(IPWElement):
    '''Model showing the max of the quadratic function'''

    model = tr.Instance(IInteractiveModel)

    interactor = tr.WeakRef

    def set_interactor(self, interactor):
        self.interactor = interactor

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
        self.interactor.update_plot(self.index)

    def widget_layout(self):
        sliders = self.get_sliders()
        out = ipw.interactive_output(self.update, sliders);
        layout = ipw.Layout(grid_template_columns='1fr 1fr')
        param_names = self.model.param_names
        param_sliders_list = [sliders[name] for name in param_names]
        grid = ipw.GridBox(param_sliders_list, layout=layout)
        box = ipw.VBox([grid, out])
        return box

    def subplots(self):
        return self.model.subplots()

    def update_plot(self, axes):
        self.model.update_plot(axes)

