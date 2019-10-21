# 지식접근 기능을 테스트한다.
from doumdoum_knowledge import DoumdoumKnowledgeManager

km = DoumdoumKnowledgeManager()
print( km.getCorpByName('컴투스') )
km.close()
