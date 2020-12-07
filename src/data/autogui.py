from ctypes import pythonapi
import os
import pyautogui
import shutil
import json
from PIL import Image, ImageGrab, ImageChops, ImageStat
import time
import random

resolution = None

def read_filename(subdir):
    path_dir = os.getcwd() + "/" + subdir
    file_list = [x for x in os.listdir(path_dir)]
    return file_list

# 문자열로 된 지수표기법 숫자를 정수형으로
def expstr2int(expstr):
    if len(expstr.split("e+")) >= 2:
        frac = float(expstr.split("e+")[0])
        exp = int(expstr.split("e+")[1])
        ret = frac * 10 ** exp
        return ret
    elif len(expstr.split("e+")) == 1:
        ret = float(expstr)
        return ret
 
# Digimat 의 fe2hp 파일을 읽어서 dictionary 형식으로 반환하는 함수
# 해당 구조의 물성치가 담겨있다.
# properties 에 json 형식으로 써야할까?
def read_fe2hp(file_num):
    success = False
    path_dir = "C:\MSC.Software\Digimat\working"
    file_list = [x for x in os.listdir(path_dir)]
    for filename in file_list:
        if filename[:9] == "fe2hpResu":
            with open(path_dir+"\\"+filename, "r") as f:
                data = f.readlines()

            # 유의미한 값이 들어 있는 것만 리턴
            if len(data) >= 10:
            
                data = list(map(str.strip, data[1:]))
                ret = {}
                for row in data:
                    var, value = map(str.strip, row.split("="))
                    # print(var, value)
                    value = expstr2int(value)
                    if var != "mismatch":
                        ret[var] = value
                
                dst = "raw/properties/"
                with open(dst+f"{file_num}.json", "w") as f:
                    json.dump(ret, f, indent=4)
                
                # 있으면 success 로 바꾼다
                success = True
                return True
            
    # 반복문 다 끝나도 success 가 False 면 에러 반환
    if success == False:
        print(f"num: {file_num}, no result file")
        return False


# Digimat 의 dat 파일(mesh 정보) 을 복사해서 반환하는 함수
# analysis 에 dat 형식으로 그대로 내용 복사
def meshdat_copy(file_num):
    try:
        src = "C:\MSC.Software\Digimat\working\Analysis1.dat"
        dst = "raw/analysis/"
        # print(src)
        # print(dst)
        shutil.copy2(src, dst)
        shutil.move(dst+"Analysis1.dat", dst+f"{file_num}.dat")
    except FileNotFoundError:
        print(f"No dat file on {file_num}")
        return False

# 해당 영역 +-2px 이미지 변화 감지
def PixelCheck(x, y):
    im1 = ImageGrab.grab((x-2, y-2, x+2, y+2))
    while True:
        time.sleep(0.03)
        im2 = ImageGrab.grab((x-2, y-2, x+2, y+2))
        im = ImageChops.difference(im1, im2)
        stat = ImageStat.Stat(im)
        if stat.sum != [0,0,0]:
            return True
    
def PixelCheck2(x, y):
    start = time.time()
    im1 = ImageGrab.grab((x-2, y-2, x+2, y+2))
    while True:
        time.sleep(0.03)
        im2 = ImageGrab.grab((x-2, y-2, x+2, y+2))
        im = ImageChops.difference(im1, im2)
        stat = ImageStat.Stat(im)
        if stat.sum != [0,0,0]:
            return True
        if time.time() - start >= 300:
            if resolution == "FHD":
                pyautogui.moveTo(750, 375, 0.5)
                pyautogui.click()
                
            if resolution == "QHD":
                pyautogui.moveTo(1000, 500, 0.5)
                pyautogui.click()
    

def ErrorCheck():
    print("Error Check: ", end="")
    # error
    x1 = 640
    y1 = 620
    im1 = ImageGrab.grab((x1-2, y1-2, x1+2, y1+2))
    # no error
    x2 = 862
    y2 = 486
    im2 = ImageGrab.grab((x2-2, y2-2, x2+2, y2+2))
    while True:
        time.sleep(0.5)
        im1_now = ImageGrab.grab((x1-2, y1-2, x1+2, y1+2))
        im2_now = ImageGrab.grab((x2-2, y2-2, x2+2, y2+2))
        im1_res = ImageChops.difference(im1, im1_now)
        im2_res = ImageChops.difference(im2, im2_now)
        stat_error = ImageStat.Stat(im1_res)
        stat_result = ImageStat.Stat(im2_res)
        # 정상 먼저, error 먼저 하면 문제 발생
        if stat_result.sum != [0,0,0]:
            print("good!")
            return False
        if stat_error.sum != [0,0,0]:
            print("error occured, try again")
            return True
        

# raw 에 analysis 와 properties 데이터
# 파일 리스트 확인하고, 뒷 숫자부터 붙여넣기
def DigimatControl(num, volFrac, numIncl, aspectR, resolution, num_of_core):
    # GUI 통제해서 
    # geometry 생성 -> mesh 생성 -> mesh 데이터 복사 후 저장 -> 
    # solution(create new job) 실행 -> 
    # 대화상자 종료 전에 read_fe2hp -> label 에 저장
    # 대화상자 종료 -> 다시 geometry 생성
    
    start = time.time()
    waittime = 0.2
    
    # phase2 사이드바
    pyautogui.moveTo(175, 366, waittime)
    pyautogui.click(clicks=2, interval=0.3)
    time.sleep(1)
    # PixelCheck(1000,1127)
    
    # 맨 위로
    if resolution == "QHD":
        pyautogui.moveTo(1228, 240, waittime)
    elif resolution == "FHD":
        pyautogui.moveTo(906, 240, waittime)
    pyautogui.click()
        
    # volume fraction
    pyautogui.moveTo(612, 246, waittime)
    pyautogui.doubleClick()
    pyautogui.write(volFrac)
    
    # num of inclusions
    pyautogui.moveTo(820, 382, waittime)
    pyautogui.doubleClick()
    pyautogui.write(numIncl)
    
    # aspect ratio
    pyautogui.moveTo(559, 636, waittime)
    pyautogui.doubleClick()
    pyautogui.write(aspectR)
    
    # Create
    if resolution == "FHD":
        pyautogui.moveTo(879, 923, waittime) # FHD
    elif resolution == "QHD":
        pyautogui.moveTo(1199, 1283, waittime) # QHD
    pyautogui.click()
    
    # Geometry 사이드바
    pyautogui.moveTo(160, 434, waittime)
    pyautogui.click()
    
    # Geometry setup
    pyautogui.moveTo(409, 145, waittime)
    pyautogui.click()
    
    # scroll #Only on FHD
    if resolution == "FHD":
        pyautogui.moveTo(843, 953, waittime)
        pyautogui.click()
    
    # generate geometry
    if resolution == "FHD":
        pyautogui.moveTo(844, 913, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(1158, 1290, waittime)
    pyautogui.click()
    
    # confirmation
    if resolution == "FHD":
        pyautogui.moveTo(316, 574, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(474, 755, waittime)
    pyautogui.click()
    
    # confirmation2
    if resolution == "FHD":
        pyautogui.moveTo(379, 574, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(541, 755, waittime)
    pyautogui.click()
    
    # 픽셀 변화 하얀색으로!
    PixelCheck(841, 838)
    
    # generation 끝 확인!
    if resolution == "FHD":
        pyautogui.moveTo(480,576, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(641,755, waittime)
    pyautogui.click()

    # Mesh 사이드바
    pyautogui.moveTo(148, 463, waittime)
    pyautogui.click()
    
    # Mesh
    pyautogui.moveTo(408, 677, waittime)
    pyautogui.click()
    
    # 메시 진행중 화면(나중에 픽셀 변화 감지)
    if resolution == "FHD":
        time.sleep(1)
        PixelCheck(815,515)
    elif resolution == "QHD":
        time.sleep(1)
        PixelCheck(1170,696)
    
    # 148 465 Mesh 사이드바(마우스 우클릭)
    pyautogui.moveTo(148, 463, 1)
    pyautogui.click(button='right')
   
    # 211 530 Mesh export
    pyautogui.moveTo(270, 530, waittime)
    pyautogui.click()
    
   
    # 737 664 Ok
    if resolution == "FHD":
        pyautogui.moveTo(737, 664, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(808, 842, 1)
    pyautogui.click()
   
    # 803 567 overwrite OK
    if resolution == "FHD":
        pyautogui.moveTo(321, 575, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(509, 751, waittime)
    pyautogui.click()

    # 159 556 Mechanical 사이드바
    pyautogui.moveTo(159, 556, waittime)
    pyautogui.click()
    
    # 1849 931 Validate
    if resolution == "FHD":
        pyautogui.moveTo(875, 929, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(1201, 1289, waittime)
    pyautogui.click(clicks=2, interval=0.5)

    # 129 585 Solution 사이드바
    pyautogui.moveTo(129, 585, waittime)
    pyautogui.click()
    
    # number of CPUs
    pyautogui.moveTo(620, 494, waittime)
    pyautogui.doubleClick()
    pyautogui.write(str(num_of_core))
    
    # Solver Type
    pyautogui.moveTo(620, 563, waittime)
    pyautogui.click()
    # direct
    # pyautogui.moveTo(620, 587, waittime)
    # pyautogui.click()
    # iterative
    pyautogui.moveTo(620, 613, waittime)
    pyautogui.click()
    # CASI iterative
    # pyautogui.moveTo(620, 637, waittime)
    # pyautogui.click()
    
    # 413 654 create new job
    pyautogui.moveTo(413, 660, waittime)
    pyautogui.click()
    
    # 286 569 Yes
    if resolution == "FHD":
        pyautogui.moveTo(286, 568, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(447, 754, waittime)
    pyautogui.click()
    
    # 703 381 하얀색으로 바뀌면 대화상자 뜬 것
    # if resolution == "FHD":
    #     check = PixelCheck(703,381)
    jobstart = time.time()
    count = 0
    # 3번 이상 연산이 실패하면 처음부터
    while True:
        time.sleep(1)
        count += 1
        
        PixelCheck2(515, 620)    
        check = read_fe2hp(num)

        if check == False:
            # 에러 창 끄기
            if resolution == "FHD":
                pyautogui.moveTo(480, 582, waittime)
            if resolution == "QHD":
                pyautogui.moveTo(640, 760, waittime)
            pyautogui.click()
            
            # 카운트가 3 이상이면 다시 처음부터
            if count >= 3:
                DigimatControl(num, volFrac, numIncl, aspectR, resolution, num_of_core)
                
            # 413 654 create new job
            pyautogui.moveTo(413, 660, waittime)
            pyautogui.click()
            
            # 286 569 Yes
            if resolution == "FHD":
                pyautogui.moveTo(286, 568, waittime)
            elif resolution == "QHD":
                pyautogui.moveTo(447, 754, waittime)
            pyautogui.click()
            
        elif check == True:
            break
     
    jobtime = time.time()-jobstart
        
    meshdat_copy(num)
    time.sleep(1)
    # 모든 정보 긁어오기 ok 누르기 전에!
    # 479 633 ok (대화상자 닫음)
    if resolution == "FHD":
        pyautogui.moveTo(480, 715, waittime)
    elif resolution == "QHD":
        pyautogui.moveTo(641, 896, waittime)
    pyautogui.click()

    print(f"data {num} Generated, time spent: {round(time.time()-start)}s,", time.strftime("%I:%M %p", time.localtime(time.time())))
    time.sleep(0.5)
    
    delete_fesu()
    delete_mesh()

    return jobtime

def delete_mesh():
    try:
        os.remove("C:\MSC.Software\Digimat\working\Analysis1.dat")
    except FileNotFoundError:
        print("No dat file to remove")
    
def delete_fesu():
    path_dir = "C:\MSC.Software\Digimat\working"
    file_list = [x for x in os.listdir(path_dir)]
    for filename in file_list:
        if filename[:9] == "fe2hpResu":
            # 프로세스가 모두 끝나면 삭제
            try:
                os.remove(path_dir+"\\"+filename)
            except FileNotFoundError:
                print("No result file to remove")
    
def saveEtc(num, volFrac, numIncl, aspectR, jobtime):
    temp = {
        "num": f"{num}",
        "volume of fraction": f"{volFrac}",
        "number of Inclusion": f"{numIncl}",
        "aspect ratio": f"{aspectR}",
        "Calculation time": f"{jobtime}",
    }
    with open(f"raw/etc/{num}_data.json", "w") as f:
        json.dump(temp, f, indent=4)


if __name__ == "__main__":
    delete_fesu()
    
    while True:
        resolution = input("resolution(fhd or qhd): ")
        if resolution == "fhd" or resolution == "f":
            resolution = "FHD"
            break
        elif resolution == "qhd" or resolution == "q":
            resolution = "QHD"
            break
        else:
            continue
        
    while True:
        index_from = int(input("index from:"))
        index_to = int(input("index to:"))
        if index_from < index_to:
            break
    
    while True:
        num_of_core = int(input("# of cores:"))
        if num_of_core >= 1 and num_of_core <= 8:
            break
        
    while True:
        mode = int(input("mode(all: 0, odd: 1, even: 2): "))
        if mode == 0 or mode == 1 or mode == 2:
            break
    
    if mode == 0:    
        range_of_index = range(index_from, index_to+1)
    elif mode == 1:
        range_of_index = range(index_from, index_to+1, 2)
    elif mode == 2:
        range_of_index = range(index_from+1, index_to+1, 2)
    
    meshsize = "30"
    
    filelist = read_filename("raw/properties/")
    nums = [int(x.split(".")[0]) for x in filelist]
    nums.sort()
    print("Existing datas:", nums)
    
    # Geometry 사이드바, Allow interpenetration
    # pyautogui.moveTo(160, 434, 0.2)
    # pyautogui.click()
    # pyautogui.moveTo(351, 248, 0.2)
    # pyautogui.click()
    
    # Mesh 사이드바, Mesh size
    pyautogui.moveTo(148, 463, 0.2)
    pyautogui.click()
    pyautogui.moveTo(510, 415, 0.2)
    pyautogui.doubleClick()
    pyautogui.write(meshsize)
    pyautogui.moveTo(510, 450, 0.2)
    pyautogui.doubleClick()
    pyautogui.write(meshsize)
    pyautogui.moveTo(510, 485, 0.2)
    pyautogui.doubleClick()
    pyautogui.write(meshsize)
        
    for i in range_of_index:
        if i in nums: continue
        
        print("i:", i, end="\t")
        volFrac = random.uniform(0.05, 0.20)
        numIncl = random.randint(30, 50)
        aspectR = random.uniform(1,4)
        # aspectR = 1
        try:
            jobtime = DigimatControl(i, str(volFrac), str(numIncl), str(aspectR), resolution, num_of_core)
            time.sleep(1)
            saveEtc(i, volFrac, numIncl, aspectR, jobtime)
            filelist = read_filename("raw/properties/")
            nums = [int(x.split(".")[0]) for x in filelist]
            nums.sort()
        except ValueError:
            continue