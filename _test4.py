# 모집정보(Wanted)를 추가하는 예시

from doumdoum_knowledge import *

km = DoumdoumKnowledgeManager()

km.addNewWanted(
    corpNm= '효성',
    collectPsncnt= None,
    receiptOpenDt= '2019-11-13',
    receiptCloseDt= '2019-11-24',
    edu= EDU_DAE_SEOKSA,
    emp_tp= EMP_TP_REGULAR,
    contactTelno= None,
    enter_tp= ENTER_TP_EXPERIENCED,
    jobsNm= '가스·에너지공학 기술자 및 연구원 | 가스·에너지 시험원',
    major= '화학, 화학공학, 전기화학, 재료공학, 물리 등 배터리 관련 전공',
    pfCond= '배터리 관련 중견업체 이상 근무한 사람',
    submitDoc= None,
    workRegion= '경기 안양시',
    fourInsNps= True,
    fourInsEi= True,
    fourInsWc= True,
    fourInsNhi= True,
    annualAvgSal= 55330,
)

km.getWantedByCorpnm('효성')
