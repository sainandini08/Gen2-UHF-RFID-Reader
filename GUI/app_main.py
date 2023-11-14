from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import zmq


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
        self.btn_receive_data = Button(text="Click Me to Receive Data Now!", size_hint=(0.3, 0.2), on_press=self.on_receive_data, background_color=(0, 1, 0, 1))
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
            # self.send_email(fake_epc, fake_rssi)
        except Exception as e:
            print(f"Error in on_receive_data: {e}")
        finally:
            socket.close()
            context.term()

    # def send_email(self, epc, rssi):
    #     # Email configuration
    #     sender_email = 'fyp.nandini@gmail.com'
    #     receiver_email = 'cute.nandini22@yahoo.com.sg'
    #     password = 'nusfyp123'
    #
    #     # Create the MIME object
    #     message = MIMEMultipart()
    #     message['From'] = sender_email
    #     message['To'] = receiver_email
    #     message['Subject'] = 'Received Data'
    #
    #     # Attach the received data to the email body
    #     body = f"EPC: {epc}\nRSSI: {rssi}"
    #     message.attach(MIMEText(body, 'plain'))
    #
    #     # Connect to the SMTP server and send the email
    #     with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #         server.starttls()
    #         server.login(sender_email, password)
    #         text = message.as_string()
    #         server.sendmail(sender_email, receiver_email, text)

if __name__ == '__main__':
    MyApp().run()

# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
#
# class PetWaterContainerApp(App):
#     def build(self):
#         #BoxLayout with a vertical orientation
#         layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
#
#         # Label for the title
#         title_label = Label(text="Welcome to your Pet's Water Container Tracking App!", font_size=26, color=(1, 1, 0, 1))
#
#         # Label widget to display the water status (Will update text according to "update_water_status" func)
#         self.water_status_label = Label(text="Status: Initializing...", font_size=20)
#
#         # Adding labels to the layout
#         layout.add_widget(title_label)
#         layout.add_widget(self.water_status_label)
#
#         return layout
#
#     #have to integrate this with RFID tag values
#     #can also include last refilled time to track how often water is being refilled
#     def update_water_status(self, has_enough_water):
#         if has_enough_water:
#             self.water_status_label.text = "Status: There is enough water in your container"
#         else:
#             self.water_status_label.text = "Status: There is not enough water in your container. Please refill your container."
#
#
# if __name__ == '__main__':
#     app = PetWaterContainerApp()
#     app.run()
