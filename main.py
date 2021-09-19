from kivy.storage.dictstore import DictStore
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from week import Week
from group_select import GroupsList, GroupNumber
from datetime import datetime

DAYS = (
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье'
    )

STORE = DictStore('data.pickle')


class Main(MDApp):
    def build(self):
        if STORE.store_exists('settings'):
            self._group = STORE.get('settings')['group']
            
            self._main_screen = Builder.load_file('styles/main_screen.kv')
            height_num = self._main_screen.height - self._main_screen.ids.toolbar.height
            y_num = self._main_screen.height - self._main_screen.ids.toolbar.height - self._main_screen.ids.day_name.height - 70
            week_swiper = Week(
                                self._group,
                                datetime.today(),
                                height = height_num,
                                y = y_num
                            )
                            
            week_swiper.bind(on_swipe=self.on_day_swipe)
            self._main_screen.add_widget(week_swiper)
            self.on_day_swipe(week_swiper) #to set day name title
        else:
            self._main_screen = Builder.load_file('styles/select_screen.kv')
            group_number_field = GroupNumber()
            group_number_field.bind(on_enter_text=self.on_enter_text)
            self._main_screen.ids.view.add_widget(group_number_field)
            self.groups_list = GroupsList()
            self.groups_list.bind(on_select=self.on_select)

            self._main_screen.ids.view.add_widget(self.groups_list)
            
            
        return self._main_screen
        
    def on_day_swipe(self, e):
        new_index = e.get_current_index()
        date_text = e.get_week_dates()[new_index]
        new_text = ', '.join((DAYS[new_index], date_text[8:].lstrip('0')))
        self._main_screen.ids.day_name.text = new_text
        
    def on_enter_text(self, *e):
        number = e[0].text
        filter_function = lambda x: x.text.lower().startswith(number.strip().lower()) 
        groups = list(filter(filter_function, self.groups_list.get_list_widgets()))

        self.groups_list.update_list(groups)

    def on_select(self, *e):
        selected_group = e[1].text
        STORE.put('settings', group=selected_group)
        self.restart()
        
    def restart(self):
        self._main_screen.clear_widgets()
        MDApp.get_running_app().run()
        

if __name__ == '__main__':
    Main().run()
