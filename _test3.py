# 챗봇이 맥락 운용을 할 수 있는지 테스트한다.

from chatbotpack.nlubringer import goNlu
from chatbotpack.dialog import DialogManager
from doumdoum_dialog import DoumdoumDialogStrategy

dm = DialogManager( DoumdoumDialogStrategy() )

qtext = '대표자 누구니'
na = goNlu(qtext)
myMeta = {'nickname':'doumdoum_gigagenie_@_128.159.0.0'}
dr = dm.goDialog(myMeta, na)
print("답변객체 : %s" % dr)
print("답변text() : %s" % dr.text())
print('----------------------------')

qtext = '컴투스 말이야'
na = goNlu(qtext)
myMeta = {'nickname':'doumdoum_gigagenie_@_128.159.0.0'}
dr = dm.goDialog(myMeta, na)
print("답변객체 : %s" % dr)
print("답변text() : %s" % dr.text())
print('----------------------------')
