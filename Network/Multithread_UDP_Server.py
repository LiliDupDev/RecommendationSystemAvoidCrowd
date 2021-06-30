import socket
import os
import threading
from .util_tools import util
from algorithm.Recommendation import Recommendation

class UDP_Server:
    # app_id = "ummisco.gama.network.common.CompositeGamaMessage"
    # bytes_to_receive
    # content_path: XML path / "./contents/string"

    def __init__(self, host, server_port, client_host ,client_port, bytes_to_receive):
        self.host = host
        self.port = server_port
        self.udp_host = client_host
        self.udp_port = client_port
        self.ThreadCount = 0
        self.ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.bytes_to_receive = bytes_to_receive
        self.tool = util()
        self.create_socket()
        self.recommendation = None

#   Create Recommendation instance
    def create_recommendation_instance(self,centers,cluster):
        self.recommendation = Recommendation(centers, cluster, 0.4, 0.6)

#   Call recommendation
    def get_recommendation(self, latitude, longitude):
        rec_list = self.recommendation.get_recommendation_list(3, longitude, latitude)
        self.recommendation.update_congestion(self.recommendation.estimate_congestion(rec_list, 1, 0.3))

        result = ""
        for place in rec_list:
            result += str(place.X)+","+str(place.Y)+";"

        return result

    def call_recommendation(self, data):
        clean_data = data.replace("{","").replace("}","") # TODO: Hay una mejor forma asi que cambialo
        coordinate_set = clean_data.split(",")
        if len(coordinate_set)==3:
            return self.get_recommendation(float(coordinate_set[0]),float(coordinate_set[1]))
        else:
            return ""

#   Network stuff
    def create_socket(self):
        try:
            self.ServerSocket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))


    def threaded_rec(self, data):
        try:
            # data=1;{-103.234545,20.5646,0}
            data_sp_1 = (data.replace('{','').replace('}',''))
            data_array=data_sp_1.split(";")

            if len(data_array)==2:
                id=data_array[0]
                content=data_array[1]
                # print("Content: " + data)
                place_list = self.call_recommendation(content)
                reply = id+";"+place_list
                print("Reply: "+reply)
                # Response
                self.tool.send_udp_message( self.udp_host, self.udp_port, reply)
            else:
                print("Else: "+data)
        except:
            print("----------------------------------------------")



    def run_server(self):
        print('UDP - Waiting for a Connection...')

        while True:
            bytesAddressPair =  self.ServerSocket.recvfrom(self.bytes_to_receive)
            message = bytesAddressPair[0].decode('utf-8')
            address = bytesAddressPair[1]
            rec_thread = threading.Thread(target=self.threaded_rec,args=(message,))
            rec_thread.start()

        self.ServerSocket.close()
