from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from main_updated import ZMQ_Sender
import zmq

class WaterStatusApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]

        self.title_label = Label(text="Water Status Tracker App", font_size=18)
        self.add_widget(self.title_label)

        self.label = Label(text="Received Data: ", font_size='20sp')
        self.add_widget(self.label)

        self.last_tracked_label = Label(text="Last Tracked:", font_size=16)
        self.add_widget(self.last_tracked_label)

        self.button = Button(text="Water Status", size_hint=(None, None), size=(161, 51), font_size=18, background_color=(0, 1, 0, 1))
        self.add_widget(self.button)

        self.button.bind(on_press=self.send_message)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:5556")
        self.socket.subscribe(b'')
        print("Connected to PySide!")  # Print statement when connected to PySide

    def send_message(self, instance):
        print("Button clicked!")
        self.label.text = "Button Clicked!"

    def on_receive_data(self, instance):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://127.0.0.1:5556")
        try:
            message = socket.recv_multipart()
            fake_epc = message[0].decode('utf-8')
            fake_rssi = float(message[1].decode('utf-8'))
            self.label.text = f"Received Data: EPC={fake_epc}, RSSI={fake_rssi}"
            self.send_values_to_sender(fake_epc, fake_rssi)
            # self.send_email(fake_epc, fake_rssi)
        except Exception as e:
            print(f"Error in on_receive_data: {e}")
        finally:
            socket.close()
            context.term()

    def send_values_to_sender(self, fake_epc, fake_rssi):
        # Use ZMQ_Sender to send data to the sender.py script
        try:
            sender = ZMQ_Sender()
            sender.send_data(fake_epc, fake_rssi)
            sender.close_socket()
        except Exception as e:
            print(f"Error in send_values_to_sender: {e}")


class MyApp(App):
    def build(self):
        return WaterStatusApp()

if __name__ == "__main__":
    MyApp().run()



# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# import zmq
#
# class WaterStatusApp(BoxLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.orientation = 'vertical'
#         self.padding = [10, 10, 10, 10]
#
#         self.title_label = Label(text="Water Status Tracker App", font_size=18)
#         self.add_widget(self.title_label)
#
#         self.label = Label(text="Received Data: ", font_size='18sp')
#         self.add_widget(self.label)
#
#         self.last_tracked_label = Label(text="Last Tracked:", font_size=16)
#         self.add_widget(self.last_tracked_label)
#
#         self.button = Button(text="Water Status", size_hint=(None, None), size=(161, 51), font_size=18)
#         self.add_widget(self.button)
#
#         self.button.bind(on_press=self.send_message)
#
#         self.context = zmq.Context()
#         self.socket = self.context.socket(zmq.SUB)
#         self.socket.connect("tcp://127.0.0.1:5556")
#         self.socket.subscribe(b'')
#         print("Connected to PySide!")  # Print statement when connected to PySide
#
#     def send_message(self, instance):
#         print("Button clicked!")
#
#     def on_receive_data(self, instance):
#         try:
#             message = self.socket.recv_multipart()
#             epc = message[0].decode('utf-8')
#             rssi = float(message[1].decode('utf-8'))
#             print(f"Received data: EPC={epc}, RSSI={rssi}")
#             self.last_tracked_label.text = f"Last Tracked: {epc}"
#         except Exception as e:
#             print(f"Error in receiving data: {e}")
#
# class MyApp(App):
#     def build(self):
#         return WaterStatusApp()
#
# if __name__ == "__main__":
#     MyApp().run()



# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
# from kivy.uix.label import Label
# import zmq
#
#
# class WaterStatusApp(BoxLayout):
#     def __init__(self, **kwargs):
#         super(WaterStatusApp, self).__init__(**kwargs)
#         # context = zmq.Context()
#         # self.socket = context.socket(zmq.SUB)
#         # self.socket.bind("tcp://*:5556")
#         # self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
#         self.orientation = 'vertical'
#         self.padding = [10, 10, 10, 10]
#
#         self.title_label = Label(text="Water Status Tracker App", font_size=18)
#         self.add_widget(self.title_label)
#
#         # Create the label to display received data
#         self.label = Label(text="Received Data: ", font_size='18sp')
#         self.add_widget(self.label)
#
#         self.button = Button(text="Water Status", size_hint=(None, None), size=(161, 51), font_size=18)
#         self.add_widget(self.button)
#
#         self.last_tracked_label = Label(text="Last Tracked:", font_size=16)
#         self.add_widget(self.last_tracked_label)
#
#     def send_message(self, instance):
#         # Placeholder function for button press event
#         pass
#
#     def update_last_tracked(self, epc):
#         # Update the last tracked label with received EPC
#         self.last_tracked_label.text = f"Last Tracked: {epc}"
#         self.text_input.text = epc
#     # def on_start(self):
#     #     Clock.schedule_interval(self.receive_data, 1)  # Schedule receive_data method to run every second
#
#     # def receive_data(self, dt):
#     #     try:
#     #         data = self.socket.recv_multipart(flags=zmq.NOBLOCK)
#     #         epc = data[0].decode('utf-8')
#     #         rssi = float(data[1].decode('utf-8'))
#     #         print(f"Received data from PySide: EPC={epc}, RSSI={rssi}")
#     #         self.text_input.text = epc
#     #         # Update your Kivy GUI with the received data here
#     #     except zmq.ZMQError as e:
#     #         if e.errno != zmq.EAGAIN:
#     #             print(f"Error in receiving data from PySide: {e}")
#     def on_receive_data(self, instance):
#         self.context = zmq.Context()
#         self.socket = self.context.socket(zmq.SUB)
#         self.socket.connect("tcp://127.0.0.1:5556")
#         self.socket.subscribe(b'')
#         try:
#             message = self.socket.recv_multipart()
#             epc = message[0].decode('utf-8')
#             rssi = float(message[1].decode('utf-8'))
#             print(f"Received data from PySide: EPC={epc}, RSSI={rssi}")
#             return epc, rssi
#         except Exception as e:
#             print(f"Error in receiving data from PySide: {e}")
#             return None, None
#         # finally:
#         #     socket.close()
#         #     context.term()
#
# class MyApp(App):
#     def build(self):
#         return WaterStatusApp()
#
#
# if __name__ == "__main__":
#     MyApp().run()
