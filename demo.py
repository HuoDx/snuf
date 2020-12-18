from snuf import SNUF
from utils.networking import send_dict

server = SNUF()

@server.on_message
def callback(msg):
    # do callback stuff here
    pass
    
if __name__ == '__main__':
    server.run()