# 챗봇의 대강스러운 작동 원리를 테스트한다.

from chatbotpack.nlubringer import goNlu, NluInfo
from chatbotpack.dialog import DialogManager
from doumdoum_dialog import DoumdoumDialogStrategy
from testd.makeDict import MakeDict
'''
qtext = '컴투스 연매출 얼마야'
#qtext = '컴투스 대표자 누구니'
na = goNlu(qtext)
'''
dm = DialogManager( DoumdoumDialogStrategy() )
#myMeta = {'nickname':'doumdoum_gigagenie_@_128.159.0.0'}
myMeta = {}
nluDict = MakeDict('컴투스 회사위치가 어디야', 'recruit.corpAddr', 3).getDict()
na = NluInfo(nluDict)
dr = dm.goDialog(myMeta, na)

print('----------------------------')
print("답변객체 : %s" % dr)
print("답변text() : %s" % dr.text())
