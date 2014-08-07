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
import random, os, time
import record


CHICKEN_SOUNDS_MAX_NO = 21
COCK_SOUNDS_MAX_NO = 1

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
			on_press: root.anySound('chicken', '../media/')
		Button:
			text: 'View my tapes'
			on_press: root.manager.current = 'tapes'
			on_press: root.anySound('chicken', '../media/')
		Button:
			text: 'Record native-speaker'
			on_press: root.manager.current = 'record'
			on_press: root.anySound('chicken', '../media/')
        Button:
            size_hint: 1,1
            text: 'Quit'
            on_release: app.stop()
            
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
			on_press: root.anySound('chicken', '../media/')
		Button:
			text: 'bla bla'
			on_press: root.anySound('chicken', '../media/')
		Button:
			text: 'Back'
			on_press: root.manager.current = 'main'
			on_press: root.anySound('chicken', '../media/')

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
			on_press: self.text = 'Recording...'
			on_release: root.recordAndSave(filetext.text)
			on_release: playback.disabled = False
			on_release: root.mostRecentFile = filetext.text
			on_release: self.text = 'Record'
		Button:
			id: playback
			text: 'Play back recording'
			disabled: True
			on_press: root.anySound(root.mostRecentFile, '../recordings/')
		Button:
			text: 'Back'
			on_press: root.manager.current = 'main'
			on_press: root.anySound('chicken', '../media/')


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
            on_press: root.anySound('cock', '../media/')	
		Button:
			text: 'Back to main menu'
			on_press: root.manager.current = 'main'
			on_press: root.anySound('chicken', '../media/')


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

		BoxLayout:
    		orientation: 'horizontal'
    		
	        Button:
    	    	text: 'The right answer'
    	    	id: moo
				disabled: True
		    	on_press: root.needNewSound = True
		    	on_press: root.remaining -=1; root.correct +=1
		    	on_press: 
		    		if root.remaining ==1: root.anySound('ooh', '../media/')
		    		else: root.anySound('correct bell short', '../media/')
				on_release: play.text = 'Play next'
				on_release: self.disabled = True; quack.disabled = True
				on_release: 
					if root.remaining ==0: root.sleep(2); root.manager.current = 'menu'; root.remaining = 20; root.correct = 0
			Button:
				text: 'The wrong answer'
				id: quack
				disabled: True
				on_press: root.needNewSound = True
				on_press: root.remaining -=1
		    	on_press: 
		    		if root.remaining ==1: root.anySound('ooh', '../media/')
		    		else: root.anySound('quack wrong', '../media/')
				on_release: play.text = 'Play next'
				on_release: self.disabled = True; moo.disabled = True
				on_release: 
					if root.remaining ==0: root.sleep(2); root.manager.current = 'menu'; root.remaining = 20; root.correct = 0
        
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
			on_press: root.anySound('chicken', '../media/')
""")

# Try using:
# on_press: root.manager.switch_to(/the screen in question/, direction='left')
# ...to get sliding left when going back


class ChickenScreen(Screen):

	def sleep(self, seconds):
		time.sleep(seconds)
	
	def anySound(self, filename, location):
		filenum = ''
		if location == '../media/':
			if filename == 'chicken':
				filenum = str(random.randint(0, CHICKEN_SOUNDS_MAX_NO))
			elif filename == 'cock':
				filenum = str(random.randint(0, COCK_SOUNDS_MAX_NO))
			
		self.sound = SoundLoader.load(location + filename + filenum + '.wav')
		self.sound.play()	
		

class MainScreen(ChickenScreen):
	pass


class TapeScreen(ChickenScreen):
	pass
	
	
class RecordScreen(ChickenScreen):
	mostRecentFile = StringProperty('')
	
	def recordAndSave(self, filename):
		record.record(filename)
		# This appears to lag by about 1 second the first time it is used.
		# A hackish but workable solution would probably be to use this function once on start-up, to 'warm it up'.
		# Then the user would never experience a problem with the lag, 
		# as it would have already passed by the time the user tried to make a recording.


class MenuScreen(ChickenScreen):
	pass


class TrainingScreen(ChickenScreen):
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