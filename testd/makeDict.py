class MakeDict:
    # 이 클래스는 회사이름이 앞에 오는 경우에만 사용할 수 있음
    def __init__(self, text, intent, lengthOfCorpNm):
        # e.g.: text = 컴투스 회사 대표가 누구니?
        # e.g.: intent = recruit.corpAddr
        self.nluDict = {
            'meta': {
                'domain' : 'test',
            },
            'text' : text,
            'nlu' : {
                'intent' : [
                    {
                        'tag' : intent,
                        'probability' : None
                    },
                ],
            'slot'   : {
                'probability' : None,
                'tags' : self.makeBIO(text, lengthOfCorpNm),
            },
            'elapsed_time': None,
            }
        }
        
    def makeBIO(self, text, lengthOfCorpNm):
        # text 앞에 오는 회사이름을 B,I로 만들고 나머지는 O로 만들어서 slot.tags에 리스트로 반환시킴
        if lengthOfCorpNm <= 0:
            raise NotGreaterThanZeroError('회사이름의 길이는 0보다 커야합니다.')
        else:
            list = []
            list.append('B-corpNm')
            for i in range(lengthOfCorpNm - 1):
                list.append('I-corpNm')
            for i in range(len(text) - lengthOfCorpNm):
                list.append('O')
            return list

    def getDict(self):
        return self.nluDict


class NotGreaterThanZeroError(Exception):
    pass