import pymysql

BUSI_SIZE_DAE = 1
BUSI_SIZE_JUNGGEYON = 2
BUSI_SIZE_JUNGSO = 3
BUSI_SIZE_GONG = 4
EDU_FREE = 1
EDU_GOJOL = 2
EDU_DAEJOL4 = 3
EDU_DAEJOL2 = 4
EDU_DAE_SEOKSA = 5
EDU_DAE_BAKSA = 6
EMP_TP_REGULAR = 1
EMP_TP_TEMPORARY = 2
ENTER_TP_EXPERIENCED = 1
ENTER_TP_NEWCOMER = 2

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


    def addNewCorp(self, name, yrSalesAmt=None, addr=None, homepg=None, busi_size=None, reprNm=None):
        '''
        새로운 회사를 넣는다.
        yrSalesAmt는 단위가 '천원'이라는 것에 주의하라.
        yrSalesAmt=100은 10만원을 의미한다.
        '''
        #https://stackoverflow.com/questions/28698722/pymysql-insert-null-or-a-string
        sql = '''
        INSERT INTO Corp
        (name, yrSalesAmt, addr, homepg, busi_size_id, reprNm)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        '''
        with self._conn.cursor() as crs:
            crs.execute(sql, (name, yrSalesAmt, addr, homepg, busi_size, reprNm))
        self._conn.commit()


    def delCorpByName(self, corpNm):
        '''
        corpNm에 해당하는 회사 정보를 없앤다.
        그러한 이름이 없어서 삭제가 이루어지지 않으면 0을 리턴한다.
        '''
        sql = "DELETE FROM Corp WHERE name=%s"
        affectedRows = 0
        with self._conn.cursor() as crs:
            affectedRows = crs.execute(sql, (corpNm))
        self._conn.commit()
        return affectedRows


    def getWantedByCorpnm(self, corpNm):
        '''
        회사명 corpNm에 해당하는 모집정보. dict 배열로 되어있다.
        가장 나중에 마감하는 것이 첫번째에 온다.
        찾지 못하면 None.
        '''
        sql = '''
        SELECT W.* FROM Wanted W
        JOIN Corp C ON W.corp_id = C.corp_id
        WHERE C.name = %s AND W.receiptCloseDt >= CURDATE()
        ORDER BY W.receiptCloseDt DESC
        '''
        with self._conn.cursor() as crs:
            crs.execute(sql, (corpNm))
            result = crs.fetchall()
            if result:
                return result
            else:
                return None


    def addNewWanted(self,
            corpNm, collectPsncnt=None, receiptOpenDt=None, receiptCloseDt=None,
            edu=None, emp_tp=None, contactTelno=None, enter_tp=None,
            jobsNm=None, major=None, pfCond=None, submitDoc=None, workRegion=None,
            fourInsNps=None, fourInsEi=None, fourInsWc=None, fourInsNhi=None,
            annualAvgSal=None):
        '''
        회사명 corpNm에 해당하는 모집정보를 새로이 추가한다.
        그러한 회사명이 없어 제대로 추가하지 못하면 LookupError가 발생.
        일자(receiptOpenDt, receiptCloseDt)는 '2019-10-12'와 같은 형식을 취해야 한다.
        '''
        
        # 먼저 주어진 회사명에 해당하는 corp_id를 찾자. 찾지 못하면 LookupError.
        corp = self.getCorpByName(corpNm)
        if not corp:
            raise LookupError('Invalid corporation name. Is it on the table Corp?')
        corp_id = corp['corp_id']

        # 이제 corp_id을 찾았으니 INSERT를 수행한다.
        sql = '''
        INSERT INTO Wanted
        (corp_id, collectPsncnt, receiptOpenDt, receiptCloseDt,
        edu_id, emp_tp_id, contactTelno, enter_tp_id,
        jobsNm, major, pfCond, submitDoc, workRegion,
        fourInsNps, fourInsEi, fourInsWc, fourInsNhi,
        annualAvgSal)
        VALUES
        (%s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s)
        '''
        with self._conn.cursor() as crs:
            crs.execute(sql, (
                corp_id, collectPsncnt, receiptOpenDt, receiptCloseDt,
                edu, emp_tp, contactTelno, enter_tp,
                jobsNm, major, pfCond, submitDoc, workRegion,
                fourInsNps, fourInsEi, fourInsWc, fourInsNhi,
                annualAvgSal
                ))
        self._conn.commit()


    def delWantedByCorpnm(self, corpNm):
        '''
        회사명 corpNm에 해당하는 모집정보를 없앤다.
        삭제된 정보 갯수가 리턴된다.
        '''
        sql = '''
        DELETE FROM Wanted W
        JOIN Corp C ON W.corp_id = C.corp_id
        WHERE C.name = %s
        '''
        affectedRows = 0
        with self._conn.cursor() as crs:
            affectedRows = crs.execute(sql, (corpNm))
        self._conn.commit()
        return affectedRows
    