from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import zmq
from PySide6.QtCore import Signal, QObject
from main_updated import ZMQ_Sender


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create welcome message
        welcome_label = Label(text="Welcome to the Pet Water Container Tracking App!", font_size='20sp')
        layout.add_widget(welcome_label)

        # Create description
        description_label = Label(text="Let's see your water level now:", font_size='16sp')
        layout.add_widget(description_label)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        layout.add_widget(anchor_layout)
        # Create the receive data button
        self.btn_receive_data = Button(text="Click Me to Receive Data Now!", size_hint=(0.3, 0.2), background_color=(0, 1, 0, 1))
        anchor_layout.add_widget(self.btn_receive_data)

        # Create the label to display received data
        self.label = Label(text="Received Data: ", font_size='18sp')
        layout.add_widget(self.label)

        # self.label = Label(text="Received Data: ", font_size='20sp', color=(1, 1, 1, 1))
        # self.btn_receive_data = Button(text="Receive Data", on_press=self.on_receive_data,
        #                                background_color=(0.2, 0.6, 1, 1))
        # Create the main layout
        # self.label = Label(text="Received Data: ")
        # self.btn_receive_data = Button(text="Receive Data", on_press=self.on_receive_data)
        #
        # layout = BoxLayout(orientation='vertical')
        # layout.add_widget(self.label)
        # layout.add_widget(self.btn_receive_data)

        return layout

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


if __name__ == '__main__':
    MyApp().run()

