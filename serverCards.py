from http.server import BaseHTTPRequestHandler, HTTPServer

port = 23659

class server(BaseHTTPRequestHandler):

    playerList = []
    hands = {}
    table = []
    bets = {}


    def do_GET(self):
        content_len = int(self.headers.get('Content-Length'))
        print(content_len)
        post_body = self.rfile.read(content_len)
        body = str(post_body)
        print(body)
        replyString = ""
        try:
            if(post_body[0:11] == "~newPlayer:"):
                i0 = 12
                i1 = post_body.find(":", i0)

                newPlayerName = post_body[i0, i1]

                playerList.append[newPlayerName]
                outString = "New player:" + newPlayerName
                print(outString)
                if(replyString == "")
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