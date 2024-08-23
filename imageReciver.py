import socket
import threading
import struct
import signal
import sys
import traceback
bind_ip = '192.168.56.3'
bind_port = 8846

class JpegReceiver(object):
    def __init__(self, panel):
        self.panel = panel
        self.server = None
        self.is_run = True
        self.client_sock = None

        signal.signal(signal.SIGINT, self.sigIntHandler)

    def sigIntHandler(self, signal, frame):
        self.shutdown()
        sys.exit(0)
    # 接收数据启动线程，接收数据函数
    def startReceiving(self):
        self.thread_hdr = threading.Thread(
            target=self.receiveThread,
        )
        self.thread_hdr.start()

    def receiveThread(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((bind_ip, bind_port))
        self.server.listen(1)


        while True:
            print ("Start Accepting..")
            try:
                self.client_sock, address = self.server.accept()
            except:
                print ("Exception is occured..")
                break

            print ('Accepted connection from {}:{}'.format(address[0], address[1]))

            jpgsize_bytes = self.client_sock.recv(4)
            jpgsize = struct.unpack('<I', jpgsize_bytes)[0]
            print ("jpgsize = " + str(jpgsize))

            jpg_data = ''.encode('utf-8')
            #####
           # 定义bytes类型，xuyu
            #####
            jpg_data_len = 0

            retry_count = 0
            max_retry_count = 300

            while jpg_data_len < jpgsize:
                try:
                    tmp_jpg_data = self.client_sock.recv(jpgsize - jpg_data_len)
                    print("bytes jpg len:",len(tmp_jpg_data))
                    # tmp_jpg_data = str(tmp_jpg_data)
                    # print("str jpg len:",len(tmp_jpg_data))

                    # print ("compare the length")
                    # print("jpg len:",len(tmp_jpg_data),  "jpgsize:" , jpgsize)
                    if not self.is_run:
                        print ("unset is_run")
                        print ("if ont self,is run\n")
                        break
                    
                    if len(tmp_jpg_data) == 0:
                        
                        retry_count -= 1
                        if retry_count <= 0:
                            print ("Client did not send data..")
                            break
                    else:
                        retry_count = max_retry_count
                        # print("jpg2  ",len(jpg_data)    )
                        # print("jpg2  len",jpg_data_len  )
                        jpg_data += tmp_jpg_data
                        # print ("tmp3   len =%d\n",len(tmp_jpg_data)   )
                        # print("jpg3  ",len(jpg_data)   )
                        # print("jpg3  len",jpg_data_len  )
                    
                    jpg_data_len = len(jpg_data)
                    # print("jpg4  ",len(jpg_data)   )
                    # print("jpg4  len",jpg_data_len     )

                except:
                    print ("Client socket is gone...")
                    # print ("size",jpg_data_len,jpgsize)
                    traceback.print_exc()
                    break

                # print("len first  size next",jpg_data_len    ,jpgsize)
                if jpg_data_len == jpgsize:
                    # fname = self.panel.getNextFileName()
                    fname = "result.jpg"
                    print ("Received Jpeg file! then save it to " + fname)
                    try:
                        f = open(fname, 'wb')
                        f.write(jpg_data)
                        f.close()

                        print ("   Update Picture")
                    except:
                        print ("Any error occured in file write.")
                        traceback.print_exc()

            print ("Closing client_socket")
            self.client_sock.close()
            self.client_sock = None

        return

    def shutdown(self):
        self.is_run = False
        if self.client_sock != None:
            print ("  waiting join...")
            # self.client_sock.close()
            self.client_sock.shutdown(2)

        if self.server != None:
            self.server.shutdown(2)
            self.thread_hdr.join()
            print ("  joined..")
        else:
            print ("self.server is None...")

if __name__ == "__main__":

    rcver = JpegReceiver(None)
    rcver.startReceiving()

    test_no = 1

    if test_no == 0:
        import time
        time.sleep(1)
        print ("Waiting Server..")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.56.3', bind_port))

        print ("Sending 12554")
        s.send(struct.pack('<I', 12554))

        s.close()
        time.sleep(10)
        rcver.shutdown()

    elif test_no == 1:
        import time
        time.sleep(1)
        print ("Waiting Server..")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.56.3', bind_port))

        print ("Sending 12554")
        s.send(struct.pack('<I', 12554))

        print ("Loop forever")
        while True:
            pass
        

    else:
        import time
        time.sleep(3)
        print ("Waiting shutdown....")
        rcver.shutdown()
        print ("shutdown.!")
 

