import traits.api as tr
import ipywidgets as ipw

class EditorFactory(tr.HasTraits):
    name = tr.Str
    model = tr.WeakRef
    tooltip = tr.Str
    value = tr.Any
    trait = tr.Trait
    label = tr.Str
    disabled = tr.Bool(False)
    ui_pane = tr.WeakRef


class FloatEditor(EditorFactory):
    def render(self):
        return ipw.FloatText(description=self.label, value=self.value,
                             tooltip=self.tooltip, disabled=self.disabled)


class IntEditor(EditorFactory):
    def render(self):
        return ipw.IntText(description=self.label, value=self.value,
                           tooltip=self.tooltip, disabled=self.disabled)


class BoolEditor(EditorFactory):
    def render(self):
        return ipw.Checkbox(description=self.label, value=self.value,
                            tooltip=self.tooltip, disabled=self.disabled)


class FloatRangeEditor(EditorFactory):
    low = tr.Float
    high = tr.Float
    low_name = tr.Str
    high_name = tr.Str
    n_steps = tr.Int(20)
    n_steps_name = tr.Str
    continuous_update = tr.Bool(False)
    readout = tr.Bool(True)
    readout_format = tr.Str

    def render(self):
        if self.low_name:
            self.low = getattr(self.model, str(self.low_name))
        if self.high_name:
            self.high = getattr(self.model, str(self.high_name))
        if self.n_steps_name:
            self.n_steps = getattr(self.model, str(self.n_steps_name))
        step = (self.high - self.low) / self.n_steps

        if not self.readout_format:
            self.readout_format = self.get_readout_format(self.low, self.high, self.n_steps)

        # There's a bug in FloatSlider for very small step, see https://github.com/jupyter-widgets/ipywidgets/issues/259
        return ipw.FloatSlider(
            value=self.value,
            min=self.low,
            max=self.high,
            step=step,
            tooltip=self.tooltip,
            continuous_update=self.continuous_update,
            description=self.label,
            disabled=self.disabled,
            readout=self.readout,
            readout_format=self.readout_format
        )

    def get_readout_format(self, low, high, n_steps):
        magnitude_n_steps = self.get_order_of_magnitude(n_steps)
        magnitude_low = self.get_order_of_magnitude(low)
        magnitude_high = self.get_order_of_magnitude(high)
        min_magnitude = min(magnitude_low, magnitude_high)
        if min_magnitude >= 0:
            req_decimals = 2
        else:
            req_decimals = abs(min_magnitude) + magnitude_n_steps
        return '.' + str(req_decimals) + 'f'

    def get_order_of_magnitude(self, num):
        sci_num = '{:.1e}'.format(num)
        sci_num_suffix = sci_num.split('e')[1]
        return int(sci_num_suffix)


class ButtonEditor(EditorFactory):
    icon = tr.Str('check')

    def render(self):
        button = ipw.Button(
            description=self.label,
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip=self.tooltip,
            icon=self.icon  # (FontAwesome names without the `fa-` prefix)
        )

        def button_clicked(change):
            setattr(self.model, self.name, True)

        button.on_click(button_clicked)
        return button
