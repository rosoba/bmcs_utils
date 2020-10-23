import traits.api as tr
import ipywidgets as ipw


class EditorFactory(tr.HasTraits):
    model = tr.WeakRef
    value = tr.Any
    trait = tr.Trait
    label = tr.Str


class FloatEditor(EditorFactory):
    def render(self):
        return ipw.FloatText(description=self.label, value=self.value)


class IntEditor(EditorFactory):
    def render(self):
        return ipw.IntText(description=self.label, value=self.value)


class BoolEditor(EditorFactory):
    def render(self):
        return ipw.Checkbox(description=self.label, value=self.value)


class FloatRangeEditor(EditorFactory):
    label = tr.Str
    low = tr.Float
    high = tr.Float
    low_name = tr.Str
    high_name = tr.Str
    n_steps = tr.Int(20)

    def render(self):
        if self.low_name:
            self.low = getattr(self.model,self.low_name)
        if self.high_name:
            self.high = getattr(self.model,self.high_name)
        step = (self.high - self.low) / self.n_steps
        return ipw.FloatSlider(
            value=self.value,
            min=self.low,
            max=self.high,
            step=step,
            continuous_update=False,
            description=r'\(%s\)' % self.label
        )
