from chatbotpack.dialog import DialogStrategy, DialogResponse
from chatbotpack.nlubringer import NluInfo
from datetime import datetime, timedelta
from doumdoum_knowledge import DoumdoumKnowledgeManager
import re

# Todo : nickname from givenMetaInfo
# e.g.: nickname = 'doumdoum_webpage_@_어쩌구아이피'
# e.g.: nickname = 'doumdoum_gigagenie_@_어쩌구아이피'

class DoumdoumDialogStrategy(DialogStrategy):
    def __init__(self):
        self._ctxDict = dict() #맥락(DoumdoumContext)을 저장해둔다.
        self.setupIntentDict() #Intent 당 책임Function 매핑.
        self._km = DoumdoumKnowledgeManager()

    def setupIntentDict(self) :
        self._intentDict = {
            'recruit.reperNm'           : self.drReperNm,
            'recruit.yrSalesAmt'        : self.drYrSalesAmt,
            'recruit.corpAddr'          : self.drCorpAddr,

            'recruit.jobsNm'            : self.drJobsNm,

            'recruit.slotExtra.corpNm'  : self.drSlotExtra_corpNm
        }

    def __del__(self):
        # DoumdoumKnowledgeManager는 사용 후 반드시 close해 주어야 한다고 했다.
        print("DoumdoumDialogStrategy.__del__")
        self._km.close()


    # --- Dialog Response Creator ---
    # 모든 dr함수는 그 매개변수가 (self, ctx, nlu)로 이루어지며, 반환은 객체 DialogResponse여야 한다.

    # (회사명)의 대표자 성함이 뭐야?
    def drReperNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm') #drSlotExtra_corpNm에서 corpNm에 대해 처리해주길 바라는 거임.
            return DialogResponse().setText('무슨 회사의 대표자를 말하십니까?')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['reprNm'] : #corp이 테이블에 존재하고, DB상 reprNm칼럼 값이 NULL이 아니었으면.
            # 정상흐름
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
        if corp and corp['yrSalesAmt'] :
            amt = corp['yrSalesAmt']  # 단위: 천원
            amt_hr = self.helper_humanReadableYrSalesAmt(amt)
            return DialogResponse().setText('%s의 연 매출액은 %s입니다.' % (corpNm, amt_hr))
        else :
            return DialogResponse().setText('죄송합니다. %s의 연 매출액을 알고 있지 않습니다.' % corpNm)

    def helper_humanReadableYrSalesAmt(self, amt):
        if amt < 0 : return "적자"
        if amt == 0 : return "0원"
        # 0:만, 1:억...
        maan = ['만', '억', '조', '경', '해', '자', '양']
        # amt는 천단위이므로 마지막 숫자는 천, 마지막에서 둘째...다섯째는 만이다.
        samt = str(int(amt))
        i = len(samt) - 1 #for samt
        result = ([samt[-1] + "천"] if samt[-1] != '0' else [])
        if i <= 0 : return result[0]
        mi = 0 #for maan
        while True :
            if i-4 <= 0 : break
            if samt[i-4:i] != '0000' :
                result.append(re.sub(r"^0*", "", samt[i-4:i]) + maan[mi])
            i = i-4
            mi += 1
        result.append(samt[0:i] + maan[mi])
        result.reverse()
        return " ".join(result) + " 원"


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
            return DialogResponse().setText('%s의 주소를 아직 알고 있지 않습니다. 죄송합니다.' % corpNm)


    # (회사명)의 모집직종이 어떻게 되?
    def drJobsNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('무슨 회사에 대해서 말하십니까?')
        # 2. 지식 확인
        wanted = self._km.getWantedByCorpnm(corpNm)[0] #[0]이 있는 것에 주의
        if wanted and wanted['jobsNm']:
            jobsNm = wanted['jobsNm']
            return DialogResponse().setText('%s의 모집직종은 %s입니다.' % (corpNm, jobsNm))
        else :
            return DialogResponse().setText('%s의 모집직종은 알려져 있지 않습니다. 죄송합니다.' % corpNm)

    
    # (회사명)이야.
    def drSlotExtra_corpNm(self, ctx, nlu):
        # 슬롯 필링이 요구될 때만 
        if not ctx.wasExpectedLast('corpNm') :
            return DialogResponse().setText('죄송합니다. 무슨 의도로 말하셨는지 모르겠습니다.')
        # 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm']
        else :
            return DialogResponse().setText('죄송합니다. 회사 이름을 말하신 것 같은데 제대로 알아듣지 못 했습니다.')
        # 이제 분기를 하자. 전 대화가 무슨 Intent였냐에 따라 분기된다.
        def reperNm():
            return self.drReperNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def jobsNm():
            return self.drJobsNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def fallback():
            return DialogResponse().setText('죄송합니다. 전에 하셨던 질문에 대해 아직 어떻게 답해야 할 지 모르겠습니다.')
        mySwitch = { #반드시 DialogResponse를 리턴해야 한다.
            'recruit.reperNm': reperNm,
            'recruit.jobsNm': jobsNm
        }
        lastIntent = ctx.whatGivenIntentLast()
        if not lastIntent in mySwitch :
            return fallback()
        return mySwitch[lastIntent]()
        
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
            if nick in self._ctxDict:
                ctx = self._ctxDict[nick]
            # 2. 없으면 만들어라.
            else :
                ctx = DoumdoumContext(givenMetaInfo)
                self._ctxDict[nick] = ctx
        else : raise Exception('No nickname.')

        # 3. 응답을 시작하겠음을 그 Context에게 알려줘야 한다.
        ctx.startDialog(intent)

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

        self._lastGivenIntent = None
        self._currentGivenIntent = None
        self._lastExpectedSlot = None
        self._currentExpectedSlot = None

    def createdAt(self):
        return self._timestamp

    def isPastSecond(self, sec):
        '''만들어진 지 sec초가 지났는가?'''
        # tiemdelta
        # https://docs.python.org/3/library/datetime.html#timedelta-objects
        l_given = timedelta(seconds=sec)
        l_this = datetime.now() - self._timestamp
        return l_this >= l_given

    def setExpected(self, whatSlot):
        self._currentExpectedSlot = whatSlot

    def wasExpectedLast(self, whatSlot):
        return self._lastExpectedSlot == whatSlot

    def whatGivenIntentLast(self):
        return self._lastGivenIntent

    def startDialog(self, givenIntent):
        # _current** -> _last**
        # _current는 초기화
        self._lastGivenIntent = self._currentGivenIntent
        #self._currentGivenIntent = None
        self._currentGivenIntent = givenIntent
        self._lastExpectedSlot = self._currentExpectedSlot
        self._currentExpectedSlot = None


def newNluinfoOfSlots(slots):
    return NluInfo('임시텍스트', 'defaultIntent', slots)
