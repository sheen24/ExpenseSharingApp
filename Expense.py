import csv
import kivy
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen




class ExpenseGrid(GridLayout):
    data=[]
    def __init__(self,**kwargs):
        super(ExpenseGrid,self).__init__()
        self.cols=2
#label 1
        self.add_widget(Label(text="Name:",font_size=30))
        self.s_name=TextInput(multiline=False,font_size=30)
        self.add_widget(self.s_name)
#label 2
        self.add_widget(Label(text="Category:",font_size=30))
        self._category=TextInput(multiline=False,font_size=30)
        self.add_widget(self._category)
    
#label 3        
        self.add_widget(Label(text="Amount:",font_size=30))
        self.s_amount=TextInput(multiline=False,font_size=30)
        self.add_widget(self.s_amount)

        
        self.press=Button(text="Add Data",font_size=32,size_hint=(1,1),pos_hint= {"x": 1, "y": 1})
        self.press.bind(on_press=self.click_me)
        self.add_widget(self.press)
        
        self.press=Button(text="Show Data",font_size=32,size_hint=(0.5,1))
        self.press.bind(on_press=self.click_me2)
        self.add_widget(self.press)


    def click_me(self,instance):
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.s_name.text,self._category.text,self.s_amount.text])
            
        print("Name:"+self.s_name.text)
        print("Category:"+self._category.text)
        print("Amount:"+self.s_amount.text)
        print("You have entered your details successfully")

    
   
    
    def click_me2(self, instance):
        with open('data.csv', 'r') as file:
            csv_reader = csv.reader(file)
            self.data = list(csv_reader)

    
        app = App.get_running_app()
        app.root.transition.direction = 'up'  # Specify the transition direction
        app.root.current = 'display'
        app.root.get_screen('display').display_data(self.data)
        


   
      
    

class SplitGrid(GridLayout):
    def __init__(self,**kwargs):
        super(SplitGrid,self).__init__()
        self.cols=2
#label 1
        self.add_widget(Label(text="Enter the amount of the bill:",font_size=30))
        self.s_billamt=TextInput(multiline=False, font_size=20,foreground_color=(0, 0, 255))
        self.add_widget(self.s_billamt)
#label 2
        self.add_widget(Label(text="Enter the percentage of tip :",font_size=30,))
        self._per=TextInput(multiline=False, font_size=20, foreground_color=(0, 0, 255))
        self.add_widget(self._per)
    
#label 3        
        self.add_widget(Label(text="How many people to split the bill:",font_size=30))
        self.s_people=TextInput(multiline=False, font_size=20, foreground_color=(0, 0, 255))
        self.add_widget(self.s_people)

        
        # Button to calculate and display split amounts
        self.calculate_button = Button(text="Calculate Split", font_size=20, size_hint=(0.5, 0.1))
        self.calculate_button.bind(on_press=self.calculate_split)
        self.add_widget(self.calculate_button)

        # Label to display split amounts
        self.result_label = Label(text="", font_size=20)
        self.add_widget(self.result_label)

    def calculate_split(self, instance):
        try:
            bill_amount = float(self.s_billamt.text)
            tip_percentage = float(self._per.text)
            num_people = int(self.s_people.text)

          
            total_amount = bill_amount * (1 + tip_percentage / 100)

            split_amount = total_amount / num_people

            # Display result
            self.result_label.text = ("Each person owes: Rs.",split_amount)
        except ValueError:
            self.result_label.text = "Invalid input. Please enter valid numbers."


        
          
       


class HomeWindow(Screen):
    pass
class FirstWindow(Screen):
    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)
        self.add_widget(ExpenseGrid())
class DisplayWindow(Screen):
     def display_data(self, data):
        
        data_display = GridLayout(cols=3, spacing=10)

      
        data_display.add_widget(Label(text='Name', font_size=20))
        data_display.add_widget(Label(text='Category', font_size=20))
        data_display.add_widget(Label(text='Amount', font_size=20))

        
        for row in data:
            for col in row:
                data_display.add_widget(Label(text=col, font_size=16))

        
        self.clear_widgets()

       
        self.add_widget(data_display)
        
        go_back_button = Button(text="Go Back", font_size=20, size_hint=(1, 0.1))
        go_back_button.bind(on_press=self.go_back)
        self.add_widget(go_back_button)

     def go_back(self, instance):
        app = App.get_running_app()
        app.root.transition.direction = 'down'
        app.root.current = 'first'  
class SecondWindow(Screen):
    def __init__(self,**kwargs):
        super(SecondWindow,self).__init__(**kwargs)
        self.add_widget(SplitGrid())
    

class WindowManager(ScreenManager):
    pass



kv = Builder.load_file('new_window.kv')

class ExpenseApp(App):
    def build(self):
        return kv

if __name__=='__main__':
    ExpenseApp().run()
