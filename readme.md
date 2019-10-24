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