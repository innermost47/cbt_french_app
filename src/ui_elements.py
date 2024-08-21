import os
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.core.text import LabelBase

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
font_dir = os.path.join(project_root, "fonts")

LabelBase.register(
    name="Roboto",
    fn_regular=os.path.join(font_dir, "Roboto-Regular.ttf"),
    fn_bold=os.path.join(font_dir, "Roboto-Bold.ttf"),
)


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            self.parent.select_with_touch(self.index, touch)
            return True

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            session = rv.data[index]["session"]
            rv.parent.parent.show_session_details(session)
