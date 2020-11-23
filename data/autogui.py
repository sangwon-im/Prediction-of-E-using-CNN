import os
import pyautogui

def expstr2int(expstr):
    if len(expstr.split("e+")) >= 2:
        frac = float(expstr.split("e+")[0])
        exp = int(expstr.split("e+")[1])
        ret = frac * 10 ** exp
        return ret
    elif len(expstr.split("e+")) == 1:
        ret = float(expstr)
        return ret
    
def read_fe2hp():
    path_dir = "C:\MSC.Software\Digimat\working"
    file_list = [x for x in os.listdir(path_dir)]
    for filename in file_list:
        if filename[:9] == "fe2hpResu":
            with open(path_dir+"\\"+filename, "r") as f:
                data = f.readlines()
            
            # 유의미한 값이 들어 있는 것만 리턴
            if len(data) > 2:
                data = list(map(str.strip, data[1:]))
                ret = {}
                for row in data:
                    var, value = map(str.strip, row.split("="))
                    # print(var, value)
                    value = expstr2int(value)
                    if var != "mismatch":
                        ret[var] = value
                
                return ret


# raw 에 analysis 와 label 데이터
properties = read_fe2hp()
print(properties)


# print(expstr2int("6.26963e+001"))


# position = pyautogui.position()
# print(pyautogui.size())
# print(position.x)
# print(position.y)

# GUI 통제해서 
# geometry 생성 -> mesh 생성 -> mesh 데이터 복사 후 저장 -> 
# solution(create new job) 실행 -> 
# 대화상자 종료 전에 read_fe2hp -> label 에 저장
# 대화상자 종료 -> 다시 geometry 생성

# 199 367 phase2 사이드바
# 612 236 volume fraction
# 820 372 num of inclusions
# 559 626 aspect ratio

# 160 421 Geometry 사이드바
# 423 131 Geometry setup
# 1814 929 generate geometry
# 822 571 confirmation
# 822 571 confirmation2
# 822 571 confirmation2
# 580 825 픽셀 변화 하얀색으로!
# 951 569 generation 끝 확인!

# 148 454 Mesh 사이드바
# 436 670 Mesh
# 834 496 메시 진행중 화면(나중에 픽셀 변화 감지)

# 159 544 Mechanical 사이드바
# 1849 931 Validate
# 1849 931 Validate 두번 누르기?

# 129 572 Solution 사이드바
# 399 651 create new job
# 766 569 Yes

# 956 376 하얀색으로 바뀌면 대화상자 뜬 것

# 961 636 ok (대화상자 닫음)



# with open(f"FE_result/label/{}", "w") as f:
#     f.write(data)