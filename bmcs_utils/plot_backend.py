
import traits.api as tr
import ipywidgets as ipw

class PlotBackend(tr.HasTraits):
    plot_widget = tr.Instance(ipw.Output)
    plot_fig = tr.Any
