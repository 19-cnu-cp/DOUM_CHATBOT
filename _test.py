# 챗봇의 대강스러운 작동 원리를 테스트한다.

from chatbotpack.nlubringer import goNlu
from chatbotpack.dialog import DialogManager
from doumdoum_dialog import DoumdoumDialogStrategy

qtext = '컴투스 연매출 얼마야'
#qtext = '컴투스 대표자 누구니'
na = goNlu(qtext)

dm = DialogManager( DoumdoumDialogStrategy() )
#myMeta = {'nickname':'doumdoum_gigagenie_@_128.159.0.0'}
myMeta = {}
dr = dm.goDialog(myMeta, na)

print('----------------------------')
print("답변객체 : %s" % dr)
print("답변text() : %s" % dr.text())
