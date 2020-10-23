
import traits.api as tr
from bmcs_utils.models.editors import \
    IntEditor, BoolEditor, FloatEditor, FloatRangeEditor

## Specialized traits
class Int(tr.BaseInt):
    editor_factory = IntEditor

class Bool(tr.BaseBool):
    editor_factory = BoolEditor

class Float(tr.BaseFloat):
    editor_factory = FloatEditor

class RengeEditor(tr.BaseFloat):
    editor_factory = FloatRangeEditor
