객체 검출
문제 발생 : 전처리 3.부터 선이 인식 안됨
-> normalization의 standard를 13으로 해줌/ 12까지 선이 먹힘
-> functions의 10(standard)를 10이하에서 13으로 바꿈

객체 인식
문제 발생 : 인식과정 6. recognition_modules 함수에서 pass 오류 발생
-> key만 return해주면 된다고 생각 pass 지움
문제 발생 : 인식과정 6. 전부 완성해서 실행했을 때 list 에러 발생
-> 인식 과정 6. 조표 드럼악보에는 조표가 없으므로 무시하고 넘어감
문제 발생 : 인식과정 7.을 하며 이전에 했던 recognize_key 함수를 사용해야하나 에러가 발생함
-> recognition_modules의 recognize_key 함수에서 조표 관련 삭제
-> modules에서 recognition함수 수정(주석으로 표기되어있음)/return에서 key(조표)삭제-> main에서도 삭제
문제 발생 : key 이후에도 사용함, key에 대해 다시 정의할 필요를 느낌
-> key값을 1로 정함

해결 못한 문제

한 열에 음표가 2개 존재하면 위의 음표하나만 인식함
(recognized_image를 inshow하면 확인 가능함)

문제 발생 : 쉼표 인식 못함