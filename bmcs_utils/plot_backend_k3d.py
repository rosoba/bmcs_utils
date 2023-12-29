from .plot_backend import PlotBackend
import ipywidgets as ipw

class K3DBackend(PlotBackend):
    """Plotting backend for k3d
    """
    def __init__(self, *args, **kw):
        super().__init__(*args,**kw)
        self.plot_widget = ipw.Output(layout=ipw.Layout(width="100%", height="100%"))
        import k3d
        self.plot_fig = k3d.Plot()
        self.plot_fig.layout = ipw.Layout(width="100%",height="100%")
        # with self.plot_widget:
        #     self.plot_fig.display()
        self.plot_fig.outputs.append(self.plot_widget)
        self.objects = {}

    def clear_fig(self):
        self.objects = {}
        # while self.plot_fig.objects:
        #     self.plot_fig -= self.plot_fig.objects[-1]

        self.plot_fig.objects = []
        self.plot_fig.object_ids = []

    def clear_object(self, object_key):
        obj = self.objects[object_key]
        if isinstance(obj, list):
            objs = obj
            for ob in objs:
                self.plot_fig -= ob
        else:
            self.plot_fig -= obj
        self.objects.pop(object_key)

    def show_fig(self):
        with self.plot_widget:
            self.plot_fig.display()

    def setup_plot(self, model):
        model.setup_plot(self)

    def update_plot(self, model):
        model.update_plot(self)
