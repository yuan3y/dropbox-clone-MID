from socket import *

packet_content_raw={'id':'ABCDEAAA','version':1,'tcp':30412}
packet_content=bytes(str(packet_content_raw),"utf-8")
cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
cs.sendto(packet_content, ('255.255.255.255', 53000))