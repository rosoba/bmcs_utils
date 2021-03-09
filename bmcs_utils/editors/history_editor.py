
import traits.api as tr
from .editors import EditorFactory
import ipywidgets as ipw

import time
from threading import Thread


class HistoryEditor(EditorFactory):
    """
    Progress bar running between 0 and 1 by default
    """
    label = 'history'
    time_var = tr.Str('t')
    time_max_var = tr.Str('t_max')

    tooltip = tr.Property(depends_on='time_var, time_max_var')
    @tr.cached_property
    def _get_tooltip(self):
        return 'history slider 0 -> %s -> %s' % (self.time_var, self.time_max_var)


    def render(self):
        history_bar_widgets = []

        t_max = getattr(self.model, self.time_max_var)

        history_slider = ipw.FloatSlider(
            value=self.value,
            min=0,
            max=t_max,
            step=0.01,
            tooltip=self.tooltip,
            continuous_update=False,
            description=self.label,
            # disabled=self.disabled,
            # readout=self.readout,
            # readout_format=self.readout_format
            layout = ipw.Layout(display='flex', width="100%")
        )

        def change_time_var(event):
            t = event['new']
            setattr(self.model, self.time_var, t)

        history_slider.observe(change_time_var,'value')

        def change_t_max(event):
            print(event)
            t_max = event.new
            history_slider.max = t_max

        self.model.observe(change_t_max, self.time_max_var)

        history_bar_widgets.append(history_slider)
        history_box = ipw.HBox(history_bar_widgets,
                                layout=ipw.Layout(padding='0px'))
        history_box.layout.align_items = 'center'
        return history_box

