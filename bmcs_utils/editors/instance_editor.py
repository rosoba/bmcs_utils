

import traits.api as tr
from .editors import EditorFactory
import ipywidgets as ipw

class InstanceEditor(EditorFactory):
    def render(self):
        ipw_view = self.value.ipw_view
        frame, editors = ipw_view.get_view_layout(self.value, self.ui_pane)
        return frame
