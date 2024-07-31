# log_processor.py
import threading
import time
import socket


class LogProcessor:
    def __init__(self, mqtt_client, config):
        self.mqtt_client = mqtt_client
        self.config = config
        self.thread = None
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.tcp_socket.connect((self.config['TCP']['host'], int(self.config['TCP']['port'])))

    def start(self):
        self.thread = threading.Thread(target=self._read_log_file, daemon=True)
        self.thread.start()

    def _read_log_file(self):
        with open(self.config['LOG']['file_path'], 'r') as log_file:
            while True:
                line = log_file.readline()
                if not line:
                    # End of file reached
                    print("End of file reached. Waiting for new data...")
                    time.sleep(float(self.config['LOG']['read_interval']))
                    log_file.seek(0, 2)  # Move to the end of the file
                    continue                
                # Split the line into timestamp and data parts
                data_part = line.split(': b', 1)
                print(data_part)   
                if data_part[1].startswith("'$"):
                # It's an NMEA sentence
                    nmea_message = data_part[1].strip().strip("'")
                    print(nmea_message)    
                    # Parse the line and publish to MQTT
                    self.mqtt_client.publish("ship/log", nmea_message)

                     # Send via UDP
                    self.udp_socket.sendto(nmea_message.encode(), 
                                           (self.config['UDP']['host'], int(self.config['UDP']['port'])))
                    
                    # Send via TCP
                    # self.tcp_socket.sendall(nmea_message.encode())