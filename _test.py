import unittest
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

class DialogResponseTest(unittest.TestCase):
    dm = DialogManager( DoumdoumDialogStrategy() )
    #myMeta = {}
    myMeta = {'nickname':'doumdoum_gigagenie_@_128.159.0.0'}

    def testGoDialog(self):
    # func이름은 test로 무조건 실행되어야 한다.
        nluDict = MakeDict('효성 업무직종이 어떻게 돼?', 'recruit.jobsNm', 2).getDict()
        na = NluInfo()
        na.setup(nluDict)
        
        dr = self.dm.goDialog(self.myMeta, na)
        print('----------------------------')
        print("답변객체 : %s" % dr)
        print("답변text() : %s" % dr.text())

if __name__ == "__main__":
    unittest.main()




