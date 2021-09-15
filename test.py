from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.adapters.listadapter import ListAdapter

from kivymd.uix.textfield import MDTextField


class DemoApp(MDApp):

	def build(self):
		screen = Screen()

		# Creating a Simple List
		scroll = ScrollView()
		mdlist = MDList()

		list_view = MDList()
		for i in range(20):

			# items = ThreeLineListItem(text=str(i) + ' item',
			#                          secondary_text='This is ' + str(i) + 'th item',
			#                          tertiary_text='hello')

			icons = IconLeftWidget(icon="android")
			items = OneLineIconListItem(text=str(i) + ' item')
			items.add_widget(icons)
			list_view.add_widget(items)

		scroll.add_widget(list_view)
		# End List
		aAdapter = ListAdapter(data=[1, 2, 3])
		text = MDTextField()
		screen.add_widget(mdlist)
		screen.add_widget(text)
		return screen


DemoApp().run()
