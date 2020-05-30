from http.server import BaseHTTPRequestHandler, HTTPServer

port = 23659

class server(BaseHTTPRequestHandler):

    playerList = []
    hands = {}
    table = []
    bets = {}


    def do_GET(self):
        global playersList
        content_len = int(self.headers.get('Content-Length'))
        print(content_len)
        post_body = str(self.rfile.read(content_len))
        body = post_body[2:]
        print(body)
        replyString = ""
        try:
            
            if(body[0:11] == "~newPlayer:"):
                i0 = 11
                i1 = body.find(":", i0)
                print(i0, i1)
                newPlayerName = body[i0:i1]
                print(newPlayerName)
                
                outString = "New player:" + newPlayerName
                print(outString)
                if(replyString == ""):
                    replyString = outString
                else:
                    replyString = replyString + ":" + outString
        except:
            print("error in new player")


        if(replyString == ""):
            replyString = "Error, no match"

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header('Content-Length',len(replyString))
        self.end_headers()
        self.wfile.write(bytes(replyString, "utf-8"))
        print("get")

try:
    # Create a web server and define the handler to manage the
    # incoming request
    ser = HTTPServer(('', port), server)
    print ('Started httpserver on port ' , port)

    # Wait forever for incoming http requests
    ser.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()
