from enum import Enum


class DialogManager:
    def __init__(self, dialogStrategy):
        self._strategy = dialogStrategy
        if not isinstance(dialogStrategy, DialogStrategy) :
            raise TypeError('The argument dialogStrategy must be an instance of DialogStrategy.')
    

    def goDialog(self, metaInfo, nluInfo):
        '''
        메타정보(metaInfo; e.g.누가 어느 채널을 통해 발화했나)와
        NLU정보(nluInfo; 어떻게 발화했나)를 받아
        적당한 DialogResponse를 돌려준다. 챗봇은 이것으로 답변을 한다.
        '''
        return self._strategy.makeDialogResponse(metaInfo, nluInfo)
        

class DialogResponse:
    def __init__(self):
        self._text = '디폴트'

    def text(self):
        # e.g. '컴투스는 연 매출 OOO억원입니다.'
        return self._text

    def setText(self, t):
        self._text = t
        return self


class DialogStrategy:
    def makeDialogResponse(self, givenMetaInfo, givenNluInfo):
        raise NotImplementedError('This method should be implemented on child classes.')
