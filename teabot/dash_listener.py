from scapy.all import sniff, ARP
from expiringdict import ExpiringDict

from server_communicator import ServerCommunicator

server_link = ServerCommunicator()

dash_mac_address = [
    'ac:63:be:e5:d0:71',
    '50:f5:da:83:38:38',
    'ac:63:be:04:39:99',
    '50:f5:da:c9:fa:8c',
    'ac:63:be:ee:36:8e',
    'ac:63:be:4c:e8:00',
    'ac:63:be:3c:e5:1e',
    'ac:63:be:10:3d:76',
    '50:f5:da:53:1c:20',
    '50:f5:da:c2:12:12']

dash_requests_cache = ExpiringDict(max_len=100, max_age_seconds=60)


dash_requests_counts = dict()


def listen_for_dash(pkt):
    """Listens for dash mac address via ARP requests and request teapot endpoint

    Args:
        pkt - Network Packet Object - Network packet.
    """
    if pkt[ARP].hwsrc in dash_mac_address:
        if not _arp_request_filter(pkt[ARP].hwsrc):
            result = server_link.send_flip_teapot_request(pkt[ARP].hwsrc)
            dash_requests_cache[pkt[ARP].hwsrc] = True
            print result


def _arp_request_filter(dash_mac_address):
    if not dash_requests_counts.get(dash_mac_address):
            return False
    return True


sniff(prn=listen_for_dash, filter="arp", store=0, count=0)
