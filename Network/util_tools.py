from html.entities import name2codepoint
import re
import xml.etree.ElementTree as ET
import socket


class util:

    def decode_xml_replacer(self, match):
      name=match.group(1)
      if(name.startswith("#")):
        return chr(int(name[1:],16))
      return chr(name2codepoint.get(name,'?'))

    def decode_xml_string(self,s):
        st=re.sub("&(.*?);",self.decode_xml_replacer,s)
        return st

    def clean_xml(self,message):
        msg = self.decode_xml_string(message)
        char_to_remove = 0
        for elem in msg:
            if elem == '<':
                break
            char_to_remove += 1

        msg_g = msg[char_to_remove:]
        tree = ET.ElementTree(ET.fromstring(msg_g))
        return tree


    def send_udp_message(self, host, port, msgFromClient):
        # msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient,"utf-8")
        serverAddressPort = (host, port)
        bufferSize = 1024
        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        try:
            # Send to server using created UDP socket
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        except:
            print("Exception")


    def get_contents(self,xml_msg,xml_path):
        root = xml_msg.getroot()
        result=""
        for form in root.findall(xml_path):
            result += form.text
        return result

    def get_contents_id_user(self,xml_msg,xml_path):
        root = xml_msg.getroot()
        result=""
        for form in root.findall(xml_path):
            result = form.text
        return result

