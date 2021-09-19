from kivy.lang.builder import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineListItem
from kivy.uix.recycleview import RecycleView
from kivy.event import EventDispatcher

import requests

Builder.load_file('styles/group_select.kv')

class GroupNumber(MDTextField, EventDispatcher):
	def __init__(self):
		super().__init__()
		self.register_event_type('on_enter_text')

	def insert_text(self, substring, from_undo=False):
		super().insert_text(substring, from_undo)
		self.dispatch('on_enter_text')

	def do_backspace(self):
		super().do_backspace()
		self.dispatch('on_enter_text')
		
	def on_enter_text(self):
		pass
		
class GroupsList(RecycleView, EventDispatcher):
	def __init__(self):
		super().__init__()
		self.register_event_type('on_select')
		response = requests.get('https://timetable.tspu.ru/grs.php')
		groups_response_list = response.json()
		self._groups_widgets = list()
		
		for group in groups_response_list:
			group_number = group['gruppa']
			second_text = ', '.join((group['fakultet'], group['course']))
			
			list_item = TwoLineListItem(text=group_number, secondary_text=second_text)
			list_item.bind(on_release=self.on_pressed)
			self._groups_widgets.append(list_item)
		self.update_list(self._groups_widgets)
			
	def get_list_widgets(self):
		return self._groups_widgets
		
	def update_list(self, groups):
		self.ids.list.clear_widgets()
		for wid in groups:
			self.ids.list.add_widget(wid)		
			
	def on_pressed(self, e):
		self.dispatch('on_select', e)
		
	def on_select(self, *e):
		pass
