from chatbotpack.dialog import DialogStrategy, DialogResponse
from datetime import datetime, timedelta
from doumdoum_knowledge import DoumdoumKnowledgeManager
from 

# Todo : nickname from givenMetaInfo
# e.g.: nickname = 'doumdoum_webpage_@_어쩌구아이피'
# e.g.: nickname = 'doumdoum_gigagenie_@_어쩌구아이피'

class DoumdoumDialogStrategy(DialogStrategy):
    def __init__(self):
        self._ctxDict = dict() #맥락(DoumdoumContext)을 저장해둔다.
        self._intentDict = self.setupIntentDict() #Intent 당 책임Function 매핑.
        self._km = DoumdoumKnowledgeManager()

    def __del__(self):
        # DoumdoumKnowledgeManager는 사용 후 반드시 close해 주어야 한다고 했다.
        print("DoumdoumDialogStrategy.__del__")
        self._km.close()

    def setupIntentDict(self) :
        return {
            'recruit.reperNm':      self.drReperNm,
            'recruit.yrSalesAmt':   self.drYrSalesAmt,
            'recruit.corpAddr':     self.drCorpAddr,
        }


    # --- Dialog Response Creator ---
    # 모든 dr함수는 그 매개변수가 (self, ctx, nlu)로 이루어져야 한다.
    # 단, dr함수 외에 헬퍼 함수를 둘 수도 있다.

    # (회사명)의 대표자 성함이 뭐야?
    def drReperNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 슬롯이 비었으니 
            return DialogResponse().setText('죄송합니다. 회사 대표자를 물어보는 것으로 이해했습니다만 어느 회사에 대해 물어보는 지 알 수 없었습니다.')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['reprNm'] : #corp이 테이블에 존재하고, DB상 reprNm칼럼 값이 NULL이 아니었으면.
            reprNm = corp['reprNm']
            return DialogResponse().setText('%s의 대표자명은 %s입니다.' % (corpNm, reprNm))
        else :
            return DialogResponse().setText('죄송합니다. %s의 대표자명을 아직 알고 있지 않습니다.' % corpNm)


    # (회사명)의 연매출액은 얼마야?
    def drYrSalesAmt(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            return DialogResponse().setText('죄송합니다. 연매출액을 물어보는 것으로 이해했습니다만 어느 회사에 대해 물어보는 지 알 수 없었습니다.')
        # 2. 지식 확인 
        corp = self._km.getCorpByName(corpNm)
        print(corp)
        if corp and corp['yrSalesAmt'] :
            amt = corp['yrSalesAmt']  # 단위: 천원
            amt_hr = self.helper_humanReadableYrSalesAmt(amt)
            return DialogResponse().setText('%s의 연 매출액은 %s입니다.' % (corpNm, amt_hr))
        else :
            return DialogResponse().setText('죄송합니다. %s의 연 매출액을 알고 있지 않습니다.' % corpNm)

    def helper_humanReadableYrSalesAmt(self, amt):
        return "얼마얼마원"

    # (회사명)의 위치는 어디니?
    def drCorpAddr(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            return DialogResponse().setText('죄송합니다. 회사주소를 물어보는 것으로 이해했습니다만 어느 회사에 대해 물어보는 지 알 수 없었습니다.')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['addr'] :
            corpAddr = corp['addr']
            return DialogResponse().setText('%s의 주소는 %s입니다.' % (corpNm, corpAddr))
        else :
            return DialogResponse().setText('죄송합니다. %s의 주소를 아직 알고 있지 않습니다.' % corpNm)

    # (회사명)의 위치는 어디니?
    def drCorpAddr(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            return DialogResponse().setText('죄송합니다. 회사주소를 물어보는 것으로 이해했습니다만 어느 회사에 대해 물어보는 지 알 수 없었습니다.')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['addr'] :
            corpAddr = corp['addr']
            return DialogResponse().setText('%s의 주소는 %s입니다.' % (corpNm, corpAddr))
        else :
            return DialogResponse().setText('죄송합니다. %s의 주소를 아직 알고 있지 않습니다.' % corpNm)

    # ------
    

    def makeDialogResponse(self, givenMetaInfo, givenNluInfo):
        # Meta info vs. Context (둘 다 맥락 정보)
        # Meta info: 사용자가 주는 것 (더 적음)
        # Context: 사용자가 줄 수 없는 내부 분석정보까지 있음 (더 많음)
        nlu = givenNluInfo
        intent = nlu.intent()
        ctx = None
        if 'nickname' in givenMetaInfo :
            nick = givenMetaInfo['nickname']
            # 1. nickname에 해당하는 Context를 가져오고
            
            # 2. 없으면 만들어라.
        
        else : print('DoumdoumDialogStrategy.makeDialogResponse: No nickname?')

        # 3. 응답을 하자
        if intent in self._intentDict :
            # 3.1. 정상 흐름.
            return self._intentDict[intent](ctx, nlu)
        else :
            # 3.2. 주어진 Intent를 처리할 수 없을 때 응답.
            return self.drFallback(ctx, nlu)

    def drFallback(self, ctx, nlu):
        print('DoumdoumDialogStrategy.drFallback: %s' % nlu.intent())
        return DialogResponse().setText('죄송합니다. 말씀하신 의도를 파악하지 못 했습니다.')


class DoumdoumContext:
    '''
    대화 맥락 정보
    '''
    def __init__(self, givenMetaInfo):
        self._timestamp = datetime.now()
        if 'nickname' in givenMetaInfo :
            self._nickname = givenMetaInfo['nickname']
        else :
            print('DoumdoumContext.__init__: No nickname?')

    def createdAt(self):
        return self._timestamp

    def isPastSecond(self, sec):
        '''만들어진 지 sec초가 지났는가?'''
        # tiemdelta
        # https://docs.python.org/3/library/datetime.html#timedelta-objects
        l_given = timedelta(seconds=sec)
        l_this = datetime.now() - self._timestamp
        return l_this >= l_given