# e.g. 효성
# https://www.work.go.kr/empInfo/empInfoSrch/list/popup/popDhsOpenEmpInfoDetail.do?empSeqno=43661
# jobsNm 가스·에너지공학 기술자 및 연구원 | 가스·에너지 시험원
# major 화학, 화학공학, 전기화학, 재료공학, 물리 등 배터리 관련 전공
# pfCond 배터리 관련 중견업체 이상 근무한 사람
# submitDoc NULL (알 수 없음)
# workRegion 경기 안양시
# fourInsNps TRUE (국민연금 있음)
# fourInsEi TRUE (고용보험 있음)
# fourInsWc TRUE (산재보험 있음)
# fourInsNhi TRUE (건강보험 있음)
# retirepay NULL (퇴직금을 주는 지 알 수 없음)
# annualAvgSal 55330 (천 단위, 즉 5533만원; 같은 공채공지를 한 잡코리아에서 찾음.)

alter table Wanted drop column jobsNm;

ALTER TABLE Wanted
ADD jobsNm VARCHAR(255)
DEFAULT NULL;

ALTER TABLE Wanted
ADD major VARCHAR(255)
DEFAULT NULL;

ALTER TABLE Wanted
ADD pfCond VARCHAR(255)
DEFAULT NULL;

ALTER TABLE Wanted
ADD submitDoc VARCHAR(255)
DEFAULT NULL;

ALTER TABLE Wanted
ADD workRegion VARCHAR(255)
DEFAULT NULL;

ALTER TABLE Wanted
ADD fourInsNps BOOLEAN
DEFAULT NULL;

ALTER TABLE Wanted
ADD fourInsEi BOOLEAN
DEFAULT NULL;

ALTER TABLE Wanted
ADD fourInsWc BOOLEAN
DEFAULT NULL;

ALTER TABLE Wanted
ADD fourInsNhi BOOLEAN
DEFAULT NULL;

ALTER TABLE Wanted
ADD annualAvgSal DECIMAL(16,3)
DEFAULT NULL;
