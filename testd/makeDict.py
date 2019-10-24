class MakeDict:
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
        if lengthOfCorpNm <= 0:
            raise NotGreaterThanOneError('회사이름의 길이는 0보다 커야합니다.')
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


class NotGreaterThanOneError(Exception):
    pass