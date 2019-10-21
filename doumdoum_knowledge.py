import pymysql

class DoumdoumKnowledgeManager:
    def __init__(self):
        '''
        지식기반을 쓸 수 있게 한다.
        데이터베이스 접근을 해야 하므로, 먼저 MySQL 접속이 가능한 환경인지 확인하라.
        데이터베이스 연결은 끊어져야 하므로 미사용시 반드시 close()해달라.
        '''
        self._conn = pymysql.connect(
            host='localhost',  #IP
            user='doummaria',  #MySQL로 들어가는 계정
            password='doum4321',  #그 비밀번호
            db='doumdoum',  #무슨 DB를 쓰는가
            cursorclass=pymysql.cursors.DictCursor  #SELECT 결과를 dict로 받게 한다.
        )

    def close(self):
        self._conn.close()

    def getReprNm(self, corpNm):
        '''
        회사명 corpNm에 해당하는 대표자 이름.
        찾지 못하면 None.
        '''
        sql = "SELECT reprNm FROM Corp WHERE name=%s"
        with self._conn.cursor() as crs:
            crs.execute(sql, (corpNm,))
            result = crs.fetchone()
            if result:
                return result['reprNm']
            else:
                return None

    def getCorpByName(self, corpNm):
        '''
        회사명 corpNm에 해당하는 회사 정보. dict로 되어있다.
        찾지 못하면 None.
        '''
        sql = "SELECT * FROM Corp WHERE name=%s"
        with self._conn.cursor() as crs:
            crs.execute(sql, (corpNm,))
            result = crs.fetchone()
            if result:
                return result
            else:
                return None