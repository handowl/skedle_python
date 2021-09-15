from kivy.lang.builder import Builder
from kivy.properties import ColorProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.behaviors.magic_behavior import MagicBehavior

from datetime import datetime, timedelta
import requests
import time

Builder.load_file('styles/week.kv')

COLORS = {
	"#e5ffd5":  (.79, .63, .86, 1), #lection
	"white":    (.77, .89, .52, 1), #facult
	"#d5f6ff":  (.99, .74, .73, 1), #prac
	"#d7d7f4":  (.99, .54, .69, 1), #labor
}


class DayTitle(MagicBehavior, MDLabel):
	pass


class Subject(MDCard):
	bg_color = ColorProperty()
	group = StringProperty()
	place = StringProperty()
	teacher = StringProperty()
	time = StringProperty()
	title = StringProperty()
	
	def __init__(self, **info):
		super().__init__()
		self.bg_color = COLORS[info['color']]
		self.group = info['group']
		self.place = info['class']
		self.teacher = info['teacher']
		self.title = info['title']
		self.time = '-'.join((info['start_time'][:-3], info['end_time'][:-3]))


class Week(MDSwiper):
	def __init__(self, group, date, height=100, y=100):
		super().__init__(height=height, y=y)
		self._group = group
		self.current_weekdate = self.init_date = date
		
		*_, dow = self.init_date.isocalendar()
		self.create_timetable(goto_index=dow-1)

	def create_timetable(self, goto_index=0):
		response = requests.get(f'https://timetable.tspu.ru/rasp_teacher.php?group={self._group}')
		timetable = self._validate_data(response.json())
		week_days = self.get_week_dates()
		
		week_subjects = self.get_current_week_subjects(week_days, timetable)
		
		for item in self.get_items():
			item.ids.subjects.clear_widgets()
		
		self.set_current(goto_index)
		
		for day, date in zip(self.get_items(), week_days):
			day.date = date
			
			if len(week_subjects[date]) > 0:
				for subject_info in week_subjects[date]:
					day.ids.subjects.add_widget(Subject(**subject_info))

			
	def _validate_data(self, data):
		for subject in data:
			start = subject['start']
			subject['start'], subject['start_time'] = start.split(' ')
			
			end = subject['end']
			subject['end'], subject['end_time'] = end.split(' ')
			
			title = subject['title']
			subject['type'], subject['title'] = title.split(' ', 1)
			subject['type'].strip('.')
			
			subject['group'] += subject['subgroup']
			
		return data
		
	def get_week_dates(self):
		year, week, dow = self.current_weekdate.isocalendar()
		week_days = (datetime.strptime('-'.join([str(year), str(week), str(x)]), '%Y-%W-%w').strftime('%Y-%m-%d') for x in range(7))
		week_days = sorted(week_days, key=lambda x: tuple(map(int, x.split('-'))))
		
		return week_days
		
	def get_current_week_subjects(self, week_days, timetable):
		subjects = dict.fromkeys(week_days, [])
		for date in subjects.keys():
			subjects[date] = tuple(subject for subject in timetable if subject['start'] == date)
			
		return subjects
		
	def on_swipe(self):
		index = self.get_current_index()
		self.ids[f'day_{index}'].shake()
		
	def on_overswipe_right(self):
		self.current_weekdate += timedelta(days=7)
		self.create_timetable(goto_index=0)
		
	def on_overswipe_left(self):
		self.current_weekdate -= timedelta(days=7)
		self.create_timetable(goto_index=6)
