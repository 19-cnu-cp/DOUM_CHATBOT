'''
Doumdoum: The main server.
사용자의 발화를 입력으로 받아 챗봇의 응답을 출력으로 보내는 일을 한다.
- Park Jongkuk
- Kim Sangwon
- Lee Cheolju
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi

class DoumdoumHTTPHandler(BaseHTTPRequestHandler):

    def postRoot(self):
        self._responseOfJson({'name':'여기는 루트 디렉토리입니다.', 'your_url':self.path})
    
    def postChat(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        self._responseOfJson({'name':'대충 챗봇 결과입니다.', 'your_url':self.path})

    def postFallback(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write("올바르지 못한 주소로 접속하셨습니다.".encode() )

    def _responseOfJson(self, d):
        ''' d = json.dumps될 수 있는 객체 '''
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write( json.dumps(d, ensure_ascii=False).encode() )

    def do_GET(self):
        self._responseOfJson({'name':'죄송합니다. GET 구현은 아직 되지 않았습니다.'})

    def do_POST(self):
        pathPostMap = {
            '/'         :self.postRoot,
            '/api/chat'    :self.postChat
        }
        if self.path in pathPostMap :
            pathPostMap[self.path]()
        else :
            self.postFallback()


def chatbotWork ():
    raise Exception('There must be \'qtext\'')


def main():
    server_addr = ('', 5566)
    httpd = HTTPServer(server_addr, DoumdoumHTTPHandler)
    print('Doumdoum main server.')
    print('Listening on :5566...')
    httpd.serve_forever()

if __name__ == "__main__":
    main()
