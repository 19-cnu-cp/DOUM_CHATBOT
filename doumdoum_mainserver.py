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
from chatbotpack.nlubringer import goNlu
from chatbotpack.dialog import DialogManager
from doumdoum_dialog import DoumdoumDialogStrategy


class DoumdoumHTTPHandler(BaseHTTPRequestHandler):

    _dialogManager = DialogManager( DoumdoumDialogStrategy() )

    def postRoot(self):
        self._responseOfJson({'name':'여기는 루트 디렉토리입니다.', 'your_url':self.path})
    
    def postChat(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        #Request는 JSON으로 이루어져야 하므로.
        if ctype != 'application/json':
            self.send_response(400) #Bad request
            self.end_headers()
            self.wfile.write("json으로 request되지 않았습니다.".encode() )
            return
            
        # 이제 request 내용을 chatbotWork에게 넘겨주어야 한다.
        try:
            length = int(self.headers.get('content-length'))
            payload_string = self.rfile.read(length).decode('utf-8')
            payload = json.loads(payload_string) if payload_string else None
            drDict = self._chatbotWork(payload) #DialogResponse as dict
            self._responseOfJson(drDict)
        except:
            self.send_response(500) #Internal Server Error
            self.end_headers()
            self.wfile.write("챗봇 처리과정에서 착오가 생겼습니다.".encode() )
            raise

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

    # 우리의 임무
    def _chatbotWork (self, payload):
        '''
        사용자의 요청을 받아 응답을 dict로 돌려준다.
        응답 = {'text':..., 'meta':...}
        '''
        if not (payload and 'qtext' in payload and 'meta' in payload):
            raise ValueError('The payload should have \'meta\' and \'qtext\'')
        qtext = payload['qtext']
        meta = payload['meta']
        print("qtext = %s" % qtext)
        print("meta = %s" % meta)

        ni = goNlu(qtext)
        dr = self._dialogManager.goDialog(meta, ni) #dr = DialogResponse 객체
        
        # 'meta' (경우에 따라 구현 안될 수도 있음)
        # ='fin' : 챗봇과 대화 끝남. e.g. Slot-filling할 필요 없음.
        # ='ctd' : 챗봇과 대화가 이어질 필요 있음. e.g. Slot-filling할 필요 있음.
        return {'text':dr.text(), 'meta':dr.meta()}
        

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

    

def main():
    server_addr = ('', 5566)
    httpd = HTTPServer(server_addr, DoumdoumHTTPHandler)
    print('Doumdoum main server.')
    print('Listening on :5566...')
    httpd.serve_forever()

if __name__ == "__main__":
    main()
