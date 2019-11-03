import requests

'''NLU Prediction Server를 운용하는 URL. %s에 질의문이 오게 한다.'''
NLU_INPUT_URL = 'http://0.0.0.0:5555/nlu?text=%s'

class NluInfo:
    
    def __init__(self, text=None, intent=None, slots=None):
        self._text = text
        self._intent = intent
        self._slots = slots

    def setup(self, nluDict):
        self._text = nluDict['text']
        self._intent = nluDict['nlu']['intent'][0]['tag']
        self._slots = slotsFromBio(self._text, nluDict['nlu']['slot']['tags'])

    def text(self):
        '''e.g. 컴투스 무슨 전공 필요하나'''
        return self._text

    def intent(self):
        '''e.g. \'recruit.major\''''
        return self._intent

    def slots(self):
        '''e.g. {슬롯이름:슬롯값텍스트, ...}'''
        return self._slots



def goNlu (text) :
    '''
    NLU 정보(NluInfo)를 준다.
    return된 객체에서 여러가지 메소드로 필요한 정보에 접근할 수 있다.
    '''
    info = NluInfo()
    info.setup(getNluFromServer(text))
    return info

def getNluFromServer (text) :
    '''
    NLU 서버에 text를 제출하여 얻은 데이터를 가져온다.
    return: dictionary nlu = {'meta': {'domain': 'recrui'}, 'text': ...
    root: 'meta', 'text', 'nlu', 'elapsed_time'
    'nlu': 'intent', 'slot'
    '''
    r = requests.get(NLU_INPUT_URL % text)
    if r.status_code != 200 : raise Exception('NLU server status_code != 200')
    return r.json()


def slotsFromBio (text, bioTags) :
    '''
    BIO태그로만 되어있어 슬롯을 뽑아내기 어려움을 해결하기 위한 Function.
    return: dictionray slots = {슬롯이름:텍스트, ...}
    return None: 슬롯을 뽑아내는 데 실패한 경우.
    '''
    # State
    # 0: O, 1: B+I, 2: Error (미사용), 3: Finish (미사용)
    state = 0
    slotName = ''
    slotTextStack = []
    slots = dict()

    assert len(text) == len(bioTags)
    for i in range(len(bioTags)) :
        bioTag = bioTags[i][0] #B, I, O
        if state == 0 : #State O
            if bioTag == 'B' : #New input is 'B'
                # 새로운 슬롯의 시작
                state = 1
                slotName = bioTags[i][2:]
                slotTextStack.append(text[i])
            elif bioTag == 'I' : #New input is 'I'
                # Error
                state = 2
                return None
            #elif bioTag == 'O' : #New input is 'O'
                # Do nothing.
                #state = 0
        elif state == 1 : #State B + I
            if bioTag == 'B' : 
                # 지금까지의 슬롯은 완료, 새로운 슬롯의 시작
                state = 1
                slots[slotName] = ''.join(slotTextStack)
                slotName = bioTags[i][2:]
                slotTextStack = []
                slotTextStack.append(text[i])
            elif bioTag == 'I' :
                # 글자 하나를 더 넣는다.
                state = 1
                slotTextStack.append(text[i])
            elif bioTag == 'O' :
                # 지금까지의 슬롯은 완료
                state = 0
                slots[slotName] = ''.join(slotTextStack)
                slotName = ''
                slotTextStack = []
        #if state == 2 : #State Error
    # New input is 'End-of-Sequence'
    #if state == 0:
        #state = 3
    #elif state == 1:
        #state = 3
    if state == 1: #State B + I
        # 지금까지의 슬롯은 완료
        slots[slotName] = ''.join(slotTextStack)
        slotName = '' 
        slotTextStack = []
    state = 3
    
    return slots
