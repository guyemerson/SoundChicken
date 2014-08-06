from kivy.app import App
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
#from kivy.uix.spinner import Spinner
#from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, StringProperty
import random, os
import record


Builder.load_string("""
<MainScreen>:
	BoxLayout:
		orientation: 'vertical'
		padding: 20
		
		Label:
			text: 'Main Menu'
			bold: True
			font_size: 30
		Button:
			text: 'Training'
			on_press: root.manager.current = 'menu'
		Button:
			text: 'View my tapes'
			on_press: root.manager.current = 'tapes'
		Button:
			text: 'Record native-speaker'
			on_press: root.manager.current = 'record'
        Button:
            size_hint: 1,1
            text: 'Quit'
            on_press: app.stop()
            
<TapeScreen>:
	BoxLayout:
		orientation: 'vertical'
		padding: 20
		
		Label:
			text: 'Tapes'
			bold: True
			font_size: 30
		Button:
			text: 'bla'
		Button:
			text: 'bla bla'
		Button:
			text: 'Back'
			on_press: root.manager.current = 'main'

<RecordScreen>:
	BoxLayout:
		orientation: 'vertical'
		padding: 20
		
		Label: 
			text: 'Record Menu'
			bold: True
			font_size: 30
		TextInput:
			id: filetext
			multiline: False
			text: '<your filename here>'
		Button:
			text: 'Record'
			on_press: root.recordAndSave(filetext.text)
			on_press: playback.disabled = False
			on_press: root.mostRecentFile = filetext.text
		Button:
			id: playback
			text: 'Play back recording'
			disabled: True
			on_press: root.playback(root.mostRecentFile)
		Button:
			text: 'Back'
			on_press: root.manager.current = 'main'


<MenuScreen>:
    BoxLayout:
    	orientation: 'vertical'
    	padding: 20
    	
    	Label:
    		text: 'Training Menu'
    		bold: True
    		font_size: 30
    	Spinner:
    		background_normal: "white"
    		background_color: 0.0, 1.0, 0.0, 0.75
    		bold: True
        	color: 0.8, 0.0, 0.8, 0.9
    		size_hint: 1,1
    		text: 'Choose language'
    		values: 'British English', 'Standard German'
    		on_press: contrastSpinner.disabled = False
    	Spinner:
    		id: contrastSpinner
    		disabled: True
    		background_normal: "white"
    		background_color: 0.0, 0.0, 1.0, 0.75
    		italic: True
    		size_hint: 1,1
    		text: 'Choose contrast'
    		values: 'My favourite contrast', 'Your favourite contrast'
			on_press: goButton.disabled = False
        Button:
        	id: goButton
            disabled: True
        	background_normal: "white"
        	background_color: 1.0, 0.0, 0.0, 0.75
        	font_size: 16
        	bold: True
        	size_hint: 1,1
            text: 'Go!'
            on_press: root.manager.current = 'training'
		Button:
			text: 'Back to main menu'
			on_press: root.manager.current = 'main'			


<TrainingScreen>:
    BoxLayout:
    	orientation: 'vertical'
    	padding: 20
    	
    	BoxLayout:
    		orientation: 'horizontal'
    		
    		BoxLayout:
    			orientation: 'vertical'
	    		Label:
    				text: 'Correct'
    			Label:
    				text: str(root.correct)
			BoxLayout:
				orientation: 'vertical'
	    		Label:
    				text: 'Remaining'
    			Label:
    				text: str(root.remaining)
    	
        Button:
            text: 'Moo'
            id: moo
            disabled: True
            on_press: root.needNewSound = True
            on_press: 
        		if root.remaining ==1: root.manager.current = 'menu'; root.remaining = 20; root.correct = 0
        		else: root.remaining -=1; root.correct +=1
        	on_press: play.text = 'Play next'
        	on_press: self.disabled = True; quack.disabled = True
        Button:
        	text: 'Quack'
        	id: quack
        	disabled: True
            on_press: 
        		if root.remaining ==1: root.manager.current = 'menu'; root.remaining = 20; root.correct = 0
        		else: root.remaining -=1
        	on_press: play.text = 'Play next'
        	on_press: self.disabled = True; moo.disabled = True
        Button:
        	id: play
        	text: 'Play next'
        	on_release:
        		if self.text == 'Play next': root.playSound(True); self.text = 'Play again'
        		elif self.text == 'Play again': root.playSound(False)
        	on_release: moo.disabled = False; quack.disabled = False
        Button:
            text: 'Back to training menu'
            on_press: root.manager.current = 'menu'
""")

# Try using:
# on_press: root.manager.switch_to(/the screen in question/, direction='left')
# ...to get sliding left when going back


class MainScreen(Screen):
	pass
#	def stop(self):
#		App.get_running_app().stop()


class TapeScreen(Screen):
	pass
	
	
class RecordScreen(Screen):
	mostRecentFile = StringProperty('')
	
	def recordAndSave(self, filename):
		record.record(filename)
	
	def playback(self, filename):
		self.sound = SoundLoader.load('../recordings/' + filename + '.wav')
		self.sound.play()


class MenuScreen(Screen):
	pass


class TrainingScreen(Screen):
	correct = NumericProperty(0)
	remaining = NumericProperty(20)
	
	def playSound(self, needNew):
		if needNew == True:
			filename = random.choice([f for f in os.listdir('../sample data') if f.endswith(".wav")])
			print filename
			self.sound = SoundLoader.load('../sample data/' + filename)
		self.sound.play()



sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(TapeScreen(name='tapes'))
sm.add_widget(RecordScreen(name='record'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(TrainingScreen(name='training'))


class MyApp(App):
    def build(self):
        return sm
        

if __name__ == '__main__':
    MyApp().run()