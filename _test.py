from chatbotpack.nlubringer import goNlu
from chatbotpack.dialog import DialogManager
from doumdoum_dialog import DoumdoumDialogStrategy

qtext = '컴투스 대표 이름 말해'
#qtext = '농협은행의 우대조건은 뭐니'
na = goNlu(qtext)

dm = DialogManager( DoumdoumDialogStrategy() )
#myMeta = {'nickname':'doumdoum_gigagenie_@_128.159.0.0'}
myMeta = {}
dr = dm.goDialog(myMeta, na)

print('----------------------------')
print("답변객체 : %s" % dr)
print("답변text() : %s" % dr.text())
