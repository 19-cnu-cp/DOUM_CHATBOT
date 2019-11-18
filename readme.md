이 프로젝트에서 쓰인 3rd-party Libraries
=========================================
* requests
* pymysql

Database tables
===============
```
mysql -u doummaria -p
```

* BusiSize 회사규모
``` mysql
CREATE TABLE BusiSize (
  busi_size_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL #회사규모의 이름 (중소기업, 대기업, ...)
);
```
* insert문
``` mysql
insert into BusiSize values(1, '대기업');
insert into BusiSize values(2, '중견기업');
insert into BusiSize values(3, '중소기업');
insert into BusiSize values(4, '공기업');
```
* Corp 회사
``` mysql
CREATE TABLE Corp (
  corp_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL, #회사명
  yrSalesAmt DECIMAL(16,3), #연매출액 (단위:천원)
  addr VARCHAR(255), #회사주소
  homepg VARCHAR(255), #회사홈페이지 주소
  busi_size_id INT, #회사규모
  reprNm VARCHAR(16), #대표자 이름
  FOREIGN KEY (busi_size_id)
      REFERENCES BusiSize (busi_size_id)
);
```
* Wanted 채용
``` mysql
CREATE TABLE Wanted (
  wanted_id INT AUTO_INCREMENT PRIMARY KEY,
  corp_id INT NOT NULL, #회사
  collectPsncnt INT, #채용인원
  receiptOpenDt Date, #채용시작일
  receiptCloseDt Date, #채용마감일
  edu_id INT, #학력조건 (고졸이상...)
  emp_tp_id INT, #계약조건 (정규직 or 비정규직)
  contactTelno VARCHAR(255), #담당자 연락번호
  enter_tp_id INT, #경력조건 (경력직 or 신입)

  jobsNm VARCHAR(255) #모집직종
  major VARCHAR(255) #요구전공
  pfCond VARCHAR(255) #우대조건
  submitDoc VARCHAR(255) #제출서류준비물
  workRegion VARCHAR(255) #근무예정지
  fourInsNps BOOLEAN #4대보험 중 국민연금 National Person Service
  fourInsEi BOOLEAN #4대보험 중 고용보험 Employment Insurance
  fourInsWc BOOLEAN #4대보험 중 산재보험 Worker's Compensation
  fourInsNhi BOOLEAN #4대보험 중 건강보험 National Health Insurance
  annualAvgSal DECIMAL(16,3) #평균연봉 (단위:천원, 즉 **만원이라면 **0천원으로.)

  FOREIGN KEY (corp_id) REFERENCES Corp (corp_id),
  FOREIGN KEY (edu_id) REFERENCES Edu (edu_id),
  FOREIGN KEY (emp_tp_id) REFERENCES EmpTp (emp_tp_id),
  FOREIGN KEY (enter_tp_id) REFERENCES EnterTp (enter_tp_id)
);
```
* Edu 학력조건
```
+--------+-------------------------+
| edu_id | name                    |
+--------+-------------------------+
|      1 | 학력 무관               |
|      2 | 고졸 이상               |
|      3 | 대졸 4년제 이상         |
|      4 | 대졸 2년제 이상         |
|      5 | 대학원 석사 이상        |
|      6 | 대학원 박사 이상        |
+--------+-------------------------+
```
* EmpTp 계약조건
```
+-----------+--------------+
| emp_tp_id | name         |
+-----------+--------------+
|         1 | 정규직       |
|         2 | 비정규직     |
+-----------+--------------+
```
* EnterTp 경력조건
```
+-------------+-----------+
| enter_tp_id | name      |
+-------------+-----------+
|           1 | 경력직    |
|           2 | 신입      |
+-------------+-----------+
```
* insert문
```
insert into Corp values(1, '농협은행', 12225242000, '서울 중구 통일로 120', 1, '이대훈');
insert into Corp values(2, '컴투스', 479405296, '서울 금천구 가산디지털 1로 131, A', 2, '송병준');
insert into Corp values(3, '신세계푸드', 1263684652, '서울 성등구 성수일로 56, 4-7층', 1, '김운아/성열기');
```



클래스
=========

## dialog.py

- DialogManager \<Class>
  - Variable
    - _strategy

  - Function
    - goDialog(metaInfo, nluInfo)

- DialogResponse \<Class>
  - Variable
    - _text
g
  - Function
    - text()
    - setText(t)

- DialogStreategy \<Interface>
  - Function
    - makeDialogResponse(giventMetaInfo, givenNluInfo)

## nlubringer.py

- NluInfo \<class>
  - Variable
    - _text
    - _intent
    - _slots

  - Function
    - text()
    - intent()
    - slots()

- Variable
  - NLU_INPUT_URL

- Function
  - goNlu(text)
  - getNluFromServer(text)
  - slotsFromBio(text, bioTags)

## doumdoum_dialog.py

- DoumdoumDialogStrategy(DialogStrategy) \<Class>
  - Variable
    - _ctxDict
    - _intentDict
    - _km

  - Function
    - setupIntentDict()
    - drReperNm(ctx, nlu)
    - drYrSalesAmt(ctx, nlu)
    - makeDialogResponse(givenMetaInfo, givenNluInfo)
    - drFallback(ctx, nlu)

- DoumdoumContext \<Class>
  - Variable
    - _timestamp
    
  - Function
    - createdAt()
    - isPastSecond(sec)