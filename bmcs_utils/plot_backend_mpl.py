from .plot_backend import PlotBackend
import matplotlib.pylab as plt
import ipywidgets as ipw

class MPLBackend(PlotBackend):
    """Plotting backend for matplotlib
    """
    def __init__(self, *args, **kw):
        super().__init__(*args,**kw)

        # To prevent additional figure from showing in Jupyter when creating figure the first time with plt.figure
        plt.ioff()

        fig = plt.figure(tight_layout=True, *args, **kw)

        fig.canvas.toolbar_position = 'top'
        fig.canvas.header_visible = False
        self.plot_widget = ipw.Output(layout=ipw.Layout(width="100%",height="100%"))
        with self.plot_widget:
            fig.show()

        self.plot_fig = fig

    def clear_fig(self):
        pass
    def show_fig(self):
        self.plot_fig.show()
    def setup_plot(self, model):
        pass
    def update_plot(self, model):
        # plt.close() # suggestion: maybe needed to clear last openned fig from memory in jupyter
        self.plot_fig.clf()
        self.axes = model.subplots(self.plot_fig)
        model.update_plot(self.axes)
