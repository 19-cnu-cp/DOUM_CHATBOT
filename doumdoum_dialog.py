from chatbotpack.dialog import DialogStrategy, DialogResponse
from datetime import datetime, timedelta
from doumdoum_knowledge import DoumdoumKnowledgeManager


# Todo : nickname from givenMetaInfo
# e.g.: nickname = 'doumdoum_webpage_@_어쩌구아이피'
# e.g.: nickname = 'doumdoum_gigagenie_@_어쩌구아이피'

class DoumdoumDialogStrategy(DialogStrategy):
    def __init__(self):
        self._ctxDict = dict() #맥락(DoumdoumContext)을 저장해둔다.
        self._intentDict = self.setupIntentDict() #Intent 당 책임Function 매핑.
        self._km = DoumdoumKnowledgeManager()

    def setupIntentDict(self) :
        return {
            'recruit.reperNm':      self.drReperNm,
            'recruit.yrSalesAmt':   self.drYrSalesAmt
        }

    # --- Dialog Response Creator ---

    def drReperNm(self, ctx, nlu):  #대표자명 물어보기
        corpNm = nlu.slots()['corpNm'] #회사명
        reprNm = self._km.getReprNm(corpNm)
        return DialogResponse().setText('%s의 대표자명은 %s입니다.' % (corpNm, reprNm))

    def drYrSalesAmt(self, ctx, nlu):
        raise NotImplementedError()

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