

import traits.api as tr
from .editors import EditorFactory
import ipywidgets as ipw

class EitherTypeEditor(EditorFactory):
    def render(self):
        option_tuples = self.trait.options
        option_keys = [key for key, _ in option_tuples]
        value = getattr(self.model, self.name)
        key = value._key
        drop_down = ipw.Dropdown(description=self.label, value=key,
                                 tooltip=self.tooltip, options=option_keys)
        drop_down.observe(self._selection_changed,'value')
        self.instance_pane = ipw.VBox(self._render_instance())
        return ipw.VBox([drop_down, self.instance_pane])

    def _render_instance(self):
        app_window = self.controller.app_window
        submodel = getattr(self.model, self.name)
        instance_controller = submodel.get_controller(app_window=app_window)
        model_editor = instance_controller.model_editor
        return [model_editor]

    def _selection_changed(self, event):
        setattr(self.model, self.name, event['new'])
        self.instance_pane.children = self._render_instance()
