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
            'recruit.homePg'            : self.drHomePg,
            'recruit.busiSize'          : self.drBusiSize,
            'recruit.jobsNm'            : self.drJobsNm,
            'recruit.collectPsncnt'     : self.drCollectPsncnt,
            'recruit.enterTpNm'         : self.drEnterTpNm,
            'recruit.eduNm'             : self.drEduNm,
            'recruit.major'             : self.drMajor,
            'recruit.pfCond'            : self.drPfCond,
            'recruit.submitDoc'         : self.drSubmitDoc,
            'recruit.workRegion'        : self.drWorkRegion,
            'recruit.fourIns'           : self.drFourIns,
            'recruit.contactTelno'      : self.drContactTelNo,
            'recruit.receiptCloseDt'    : self.drReceiptCloseDt,
            'recruit.salTpNm'           : self.drSalTpNm,
            'recruit.empTpNm'           : self.drEmpTpNm,
            'recruit.slotExtra.corpNm'  : self.drSlotExtra_corpNm
        }

    def __del__(self):
        # DoumdoumKnowledgeManager는 사용 후 반드시 close해 주어야 한다고 했다.
        print("DoumdoumDialogStrategy.__del__")
        self._km.close()


    # --- Helper Functions ---

    def humanReadableMoney_cheon(self, amt):
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

    # ------

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
            return DialogResponse().setText('무슨 회사의 대표자를 말하십니까?').setMeta('cnt')
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
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인 
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['yrSalesAmt'] :
            amt = corp['yrSalesAmt']  # 단위: 천원
            amt_hr = self.humanReadableMoney_cheon(amt)
            return DialogResponse().setText('%s의 연 매출액은 %s입니다.' % (corpNm, amt_hr))
        else :
            return DialogResponse().setText('죄송합니다. %s의 연 매출액을 알고 있지 않습니다.' % corpNm)


    # (회사명)의 위치는 어디니?
    def drCorpAddr(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['addr'] :
            corpAddr = corp['addr']
            return DialogResponse().setText('%s의 주소는 %s입니다.' % (corpNm, corpAddr))
        else :
            return DialogResponse().setText('%s의 주소를 아직 알고 있지 않습니다. 죄송합니다.' % corpNm)


    # (회사명)의 위치는 어디니?
    def drHomePg(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사의 홈페이지를 물으십니까?').setMeta('cnt')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['homepg'] :
            homePg = corp['homepg']
            return DialogResponse().setText('%s의 홈페이지는 %s입니다.' % (corpNm, homePg))
        else :
            return DialogResponse().setText('%s의 홈페이지 주소를 아직 알고 있지 않습니다. 죄송합니다.' % corpNm)


    # (회사명)의 회사 규모?
    def drBusiSize(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사의 기업 규모를 물으십니까?').setMeta('cnt')
        # 2. 지식 확인
        corp = self._km.getCorpByName(corpNm)
        if corp and corp['busi_size_id'] :
            busiSizeId = corp['busi_size_id']
            busiSize = ['대기업','중견기업','중소기업','공기업'][busiSizeId-1]
            return DialogResponse().setText('%s의 회사 규모는 %s입니다.' % (corpNm, busiSize))
        else :
            return DialogResponse().setText('%s의 회사 규모를 아직 알고 있지 않습니다. 죄송합니다.' % corpNm)


    # 6. (회사명)의 모집직종이 어떻게 되?
    def drJobsNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['jobsNm']:
            jobsNm = wanted['jobsNm']
            return DialogResponse().setText('%s의 모집직종은 %s입니다.' % (corpNm, jobsNm))
        else :
            return DialogResponse().setText('%s의 모집직종은 알려져 있지 않습니다. 죄송합니다.' % corpNm)

    
    # 8. (회사명)의 모집인원은 몇 명이니?
    def drCollectPsncnt(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['collectPsncnt']:
            collectPsncnt = wanted['collectPsncnt']
            return DialogResponse().setText('%s의 모집 인원은 %s명입니다.' % (corpNm, collectPsncnt))
        else :
            return DialogResponse().setText('%s의 모집 인원은 정해져 있지 않습니다.' % corpNm)

    
    # 9. (회사명)의 경력조건?
    def drEnterTpNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['enter_tp_id']:
            enterTpId = wanted['enter_tp_id']
            enterTp = ['경력직', '신입'][enterTpId-1]
            return DialogResponse().setText('%s의 경력 조건은 %s입니다.' % (corpNm, enterTp))
        else :
            return DialogResponse().setText('%s의 경력 조건은 정해져 있지 않습니다.' % corpNm)

    
    def drEduNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['edu_id']:
            edu_id = wanted['edu_id']
            edu = ['학력 무관', '고졸 이상', '대졸 4년제 이상', '대졸 2년제 이상', '대학원 석사 이상', '대학원 박사 이상'][edu_id]
            return DialogResponse().setText('%s의 요구 학력은 %s입니다.' % (corpNm, edu))
        else :
            return DialogResponse().setText('%s의 요구 학력은 정해져 있지 않습니다.' % corpNm)

    
    def drMajor(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['major']:
            major = wanted['major']
            return DialogResponse().setText('%s에서 요구하는 전공으로 %s가 있습니다.' % (corpNm, major))
        else :
            return DialogResponse().setText('%s의 요구 전공은 정해져 있지 않습니다.' % corpNm)

    
    def drPfCond(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['pfCond']:
            pfCond = wanted['pfCond']
            return DialogResponse().setText('%s의 우대조건은 %s입니다.' % (corpNm, pfCond))
        else :
            return DialogResponse().setText('%s의 우대조건은 정해져 있지 않습니다.' % corpNm)

    
    def drSubmitDoc(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['submitDoc']:
            submitDoc = wanted['submitDoc']
            return DialogResponse().setText('%s의 제출 서류 준비물은 %s입니다.' % (corpNm, submitDoc))
        else :
            return DialogResponse().setText('%s의 제출 서류 준비물은 정해져 있지 않습니다.' % corpNm)

    
    def drWorkRegion(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['workRegion']:
            workRegion = wanted['workRegion']
            return DialogResponse().setText('%s의 근무예정지는 %s입니다.' % (corpNm, workRegion))
        else :
            return DialogResponse().setText('%s의 근무예정지는 정해져 있지 않습니다.' % corpNm)

    
    def drFourIns(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['fourInsNps'] and wanted['fourInsEi'] and wanted['fourInsWc'] and wanted['fourInsNhi']:
            insArr = []
            if wanted['fourInsNps']: insArr.append('국민연금')
            if wanted['fourInsEi']: insArr.append('고용보험')
            if wanted['fourInsWc']: insArr.append('산재보험')
            if wanted['fourInsNhi']: insArr.append('건강보험')
            if len(insArr) > 0:
                return DialogResponse().setText('%s에서 가입하는 4대보험으로 %s가 있습니다.' % (corpNm, ", ".join(insArr)))
            else:
                return DialogResponse().setText('%s에서는 4대보험에 들지 않습니다.' % (corpNm))
        else :
            return DialogResponse().setText('%s의 4대보험 가입 여부는 아직 아는 바가 없습니다. 죄송합니다.' % corpNm)

    
    def drContactTelNo(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['contactTelno']:
            contactTelNo = wanted['contactTelno']
            return DialogResponse().setText('%s의 채용담당자 전화번호는 %s입니다.' % (corpNm, contactTelNo))
        else :
            return DialogResponse().setText('%s의 채용담당자 전화번호는 정해져 있지 않습니다.' % corpNm)

    # 19. (회사명) #접수마감일
    def drReceiptCloseDt(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm']
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['receiptCloseDt'] :
            receiptCloseDt = wanted['receiptCloseDt']
            receiptCloseDt_hr = receiptCloseDt.strftime('%Y년 %m월 %d일')
            return DialogResponse().setText('%s의 접수마감일은 %s입니다.' % (corpNm, receiptCloseDt_hr))
        else :
            return DialogResponse().setText('%s의 접수마감일을 아직 알고 있지 않습니다.' % corpNm)

    
    # 20. (회사명) #임금조건
    def drSalTpNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt')
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['annualAvgSal']:
            avs = wanted['annualAvgSal']
            annualAvgSal_hr = self.humanReadableMoney_cheon(avs)
            return DialogResponse().setText('%s의 연봉은 %s입니다.' % (corpNm, annualAvgSal_hr))
        else :
            return DialogResponse().setText('%s의 연봉을 아직 알고 있지 않습니다.' % corpNm)

    
    # 21. (회사명)의 고용 형태는 어떻게 되니?
    def drEmpTpNm(self, ctx, nlu):
        # 1. 슬롯 확인
        if nlu.slots() != None and 'corpNm' in nlu.slots() :
            corpNm = nlu.slots()['corpNm'] #회사명
        else :
            # 회사명 슬롯이 없을 때의 분기
            ctx.setExpected('corpNm')
            return DialogResponse().setText('어느 회사에 대해서 말하십니까?').setMeta('cnt') # setMeta는 프론트의 동작과 관련됨.
        # 2. 지식 확인
        wanted = self._km.getLastWantedByCorpnm(corpNm)
        if wanted and wanted['emp_tp_id']:
            emp_tp_id = wanted['emp_tp_id']
            return DialogResponse().setText('%s의 고용 형태는 %s입니다.' % (corpNm, emp_tp_id))
        else :
            return DialogResponse().setText('%s의 고용형태를 알고 있지 않습니다.' % corpNm)
    
    
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
        def yrSalesAmt():
            return self.drYrSalesAmt( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def corpAddr():
            return self.drCorpAddr( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def homePg():
            return self.drHomePg( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def busiSize():
            return self.drBusiSize( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )

        def jobsNm():
            return self.drJobsNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def collectPsncnt():
            return self.drCollectPsncnt( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def enterTpNm():
            return self.drEnterTpNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def eduNm():
            return self.drEduNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def major():
            return self.drMajor( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def pfCond():
            return self.drPfCond( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def submitDoc():
            return self.drSubmitDoc( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def workRegion():
            return self.drWorkRegion( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def fourIns():
            return self.drFourIns( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def contactTelno():
            return self.drContactTelNo( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def receiptCloseDt():
            return self.drReceiptCloseDt( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def salTpNm():
            return self.drSalTpNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )
        def empTpNm():
            return self.drEmpTpNm( ctx, newNluinfoOfSlots({'corpNm':corpNm}) )

        def fallback():
            return DialogResponse().setText('죄송합니다. 전에 하셨던 질문에 대해 아직 어떻게 답해야 할 지 모르겠습니다.')
        mySwitch = { #반드시 DialogResponse를 리턴해야 한다.
            'recruit.reperNm': reperNm,
            'recruit.yrSalesAmt': yrSalesAmt,
            'recruit.corpAddr': corpAddr,
            'recruit.homePg': homePg,
            'recruit.busiSize': busiSize,

            'recruit.jobsNm': jobsNm,
            'recruit.collectPsncnt': collectPsncnt,
            'recruit.enterTpNm':enterTpNm,
            'recruit.eduNm':eduNm,
            'recruit.major':major,
            'recruit.pfCond':pfCond,
            'recruit.submitDoc':submitDoc,
            'recruit.workRegion':workRegion,
            'recruit.fourIns':fourIns,
            'recruit.contactTelno':contactTelno,
            'recruit.receiptCloseDt':receiptCloseDt,
            'recruit.salTpNm':salTpNm,
            'recruit.empTpNm':empTpNm
 
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
