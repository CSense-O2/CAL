# -*- Encoding:UTF-8 -*- #
### 코드를 무단으로 복제,개조 및 배포하지 말 것 ###
### Copyright ⓒ 2021 CSense-O2 / 산소 my______baby@naver.com ###
import os
import sys
import shutil
from tkinter import *
from tkinter import filedialog
import tkinter.ttk
import tkinter.messagebox as msgbox
import webbrowser
from string import ascii_uppercase
from bs4 import BeautifulSoup
from requests import get

현재버전 = '1.0.3'
real_path = os.getcwd()
exe_path = real_path.replace('\\', '/')
backup_path = os.path.expanduser('~')+'/Desktop/CAL_backup/filepath.txt'
for drive in list(ascii_uppercase):
    for (path, dir, files) in os.walk(drive+':/'):
        if 'LOSTARK' in dir:
            customizing_path = path.replace(
                '\\', '/')+'/LOSTARK/EFGame/Customizing'
            break

url = 'https://bit.do/customizing'

response = get(url)

download_list = []

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    version = soup.select_one('#version')
    try:
        최신버전 = version.get_text().replace("v", "")
        updatelog = soup.select_one('#'+version)
        patchnote = """
### ver."""+현재버전+""" 업데이트 안내 ###
"""+updatelog.get_text()
    except AttributeError:
        msgbox.showinfo('최신버전 확인 오류', '최신 버전 확인에 오류가 발생했습니다.\r홈페이지를 확인해주세요.')
        webbrowser.open('https://bit.do/customizing')
        sys.exit(0)
    if 최신버전 > 현재버전:
        q1 = msgbox.askquestion(
            '최신 버전 발견', '최신 버전 다운로드를 위해 링크가 열립니다.\n커마 경로 파일을 백업하시겠습니까?')
        if q1 == 'yes':
            shutil.copyfile(exe_path+'/MainFolder/filepath.txt', backup_path)
        msgbox.showinfo('최신 버전 발견', '최신 버전 다운로드를 위해 링크가 열립니다.')
        webbrowser.open('https://bit.do/customizing')
        sys.exit(0)
    elif 최신버전 <= 현재버전:
        pass
    else:
        msgbox.showerror('버전 확인 오류', '관리자에게 "버전 확인 오류"라고 전달해주세요.')
        webbrowser.open('http://pf.kakao.com/_laxars/chat')
        sys.exit(0)
elif response.status_code == 404:
    msgbox.showinfo('현재 점검중입니다.', '현재 점검중이니 관리자에게 문의해주세요.')
    webbrowser.open('http://pf.kakao.com/_laxars/chat')
    sys.exit(0)
else:
    msgbox.showerror("파싱 오류", 'response : ' +
                     response.status_code+"\n해당 오류 코드를 관리자에게 전달해 주세요.")
    webbrowser.open('http://pf.kakao.com/_laxars/chat')
    sys.exit(0)

if customizing_path == '':
    msgbox.showinfo('로스트아크 설치 탐색 오류', '관리자에게 "로스트아크 설치 탐색 오류" 라고 전달해주세요.')
    webbrowser.open('http://pf.kakao.com/_laxars/chat')

root = Tk()
root.title("커스터마이징 적용기")
w = 430
h = 500
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws-w)/2
y = (hs-h)/2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(False, TRUE)
root.iconbitmap(exe_path+'/MainFolder/icon.ico')

with open(exe_path+'/MainFolder/다시보지않기.txt', 'r', encoding='utf-8') as file:
    read = file.read()

if '다시보지않기' not in read:
    toplevel = Toplevel(root)
    toplevel.title('업데이트 내역')
    toplevel.geometry('+%d+%d' % (x, y))
    toplevel.iconbitmap(exe_path+'/MainFolder/icon.ico')
    toplevel.wm_attributes("-topmost", 1)
    Label(toplevel, text=patchnote).pack(padx=20)

    def 다시보지않기():
        with open(exe_path+'/MainFolder/다시보지않기.txt', 'w', encoding='UTF-8') as file:
            file.write('다시보지않기')
        toplevel.destroy()
    Button(toplevel, text='다시보지않기', command=다시보지않기).pack(pady=5)


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


def link_btn():
    webbrowser.open('http://pf.kakao.com/_laxars/chat')


def update_log():
    msgbox.showinfo("업데이트 내용 확인", patchnote)


def install_btn():
    msgbox.showinfo("커마 폴더 경로", customizing_path)


def version_btn():
    msgbox.showinfo("현재 버전", '[ v '+현재버전+' ]')


def load():
    work_choose = worklist.index(work_combobox.get())
    if work_choose < 0:
        msgbox.showwarning('직업 선택 오류', '직업을 선택한 후 불러오기 버튼을 눌러주세요.')
    elif work_choose >= 0:
        with open(exe_path+'/MainFolder/filepath.txt', 'r', encoding='utf-8') as file:
            file_read = file.read()
        work_list = list_chunk(file_read.split('\n'), 5)
        file_list = work_list[work_choose]
        slot1_filename.set(file_list[0].split(':')[1].split('|')[0])
        slot2_filename.set(file_list[1].split(':')[1].split('|')[0])
        slot3_filename.set(file_list[2].split(':')[1].split('|')[0])
        slot4_filename.set(file_list[3].split(':')[1].split('|')[0])
        slot5_filename.set(file_list[4].split(':')[1].split('|')[0])
        slot1_filepath.set(file_list[0].split('|')[1])
        slot2_filepath.set(file_list[1].split('|')[1])
        slot3_filepath.set(file_list[2].split('|')[1])
        slot4_filepath.set(file_list[3].split('|')[1])
        slot5_filepath.set(file_list[4].split('|')[1])


def apply():
    path_list = [slot1_path.cget("text"), slot2_path.cget("text"), slot3_path.cget(
        "text"), slot4_path.cget("text"), slot5_path.cget("text")]
    work_name = work_combobox.get()
    work_choose = worklist.index(work_name)
    work_list = ['Warrior', 'Fighter_Male', 'Fighter',
                 'Hunter', 'Hunter_Female', 'Magician', 'Delain']
    if work_choose < 0:
        msgbox.showwarning('직업 선택 오류', '직업을 선택한 후 불러오기 버튼을 눌러주세요.')
    elif work_choose >= 0:
        q2 = msgbox.askyesno(work_name+'의 커마 파일 적용',
                             work_name+'의 커마 파일을 적용하시겠습니까?')
        if q2 == 1:
            for path in path_list:
                if path == '비어있음':
                    pass
                elif path != '비어있음':
                    if os.path.isfile(customizing_path+'/Customizing_'+work_list[work_choose]+'_slot'+str(path_list.index(path))+'.cus'):
                        q3 = msgbox.askquestion(
                            '커마 파일 확인', '해당 슬롯에 커마 파일이 존재합니다.\n덮어쓰시겠습니까?')
                        if q3 == 'yes':
                            shutil.copyfile(str(path), customizing_path+'/Customizing_'+str(
                                work_list[work_choose])+'_slot'+str(path_list.index(path))+'.cus')
                            msgbox.showinfo(
                                '커마 파일 적용 완료', '커마 파일이 적용되었습니다.\n인게임에서 확인해주세요.')
                        elif q3 == 'no':
                            msgbox.showwarning(
                                '커마 파일 중복 확인', '해당 커마 파일을 백업하신 후 다시 시도해주세요.')
                            break
                    else:
                        shutil.copyfile(str(path), customizing_path+'/Customizing_'+str(
                            work_list[work_choose])+'_slot'+str(path_list.index(path))+'.cus')
                        msgbox.showinfo(
                            '커마 파일 적용 완료', '커마 파일이 적용되었습니다.\n인게임에서 확인해주세요.')


def save():
    work_name = work_combobox.get()
    work_choose = worklist.index(work_name)
    if work_choose < 0:
        msgbox.showwarning('직업 선택 오류', '직업을 선택한 후 불러오기 버튼을 눌러주세요.')
    elif work_choose >= 0:
        q4 = msgbox.askyesno(work_name+'커마 파일 저장',
                             work_name+'의 커마 파일을 저장하시겠습니까?')
        if q4 == 1:
            with open(exe_path+'/MainFolder/filepath.txt', 'r', encoding='utf-8') as file:
                read_file = file.read()
            current_list = [work_name+'1번:'+slot1_filename.get()+':'+slot1_filepath.get(), work_name+'2번:'+slot2_filename.get()+':'+slot2_filepath.get(), work_name+'3번:'+slot3_filename.get(
            )+':'+slot3_filepath.get(), work_name+'4번:'+slot4_filename.get()+':'+slot4_filepath.get(), work_name+'5번:'+slot5_filename.get()+':'+slot5_filepath.get()]
            read_file.split('\n')[work_choose*5:work_choose*5+5] = current_list
            if work_choose == 0:
                write_file_list = current_list+read_file.split('\n')[5:]
            elif work_choose == 1:
                write_file_list = read_file.split(
                    '\n')[5]+current_list+read_file.split('\n')[10:]
            elif work_choose == 2:
                write_file_list = read_file.split(
                    '\n')[:10]+current_list+read_file.split('\n')[15:]
            elif work_choose == 3:
                write_file_list = read_file.split(
                    '\n')[:15]+current_list+read_file.split('\n')[20:]
            elif work_choose == 4:
                write_file_list = read_file.split(
                    '\n')[:20]+current_list+read_file.split('\n')[25:]
            elif work_choose == 5:
                write_file_list = read_file.split(
                    '\n')[:25]+current_list+read_file.split('\n')[30:]
            elif work_choose == 6:
                write_file_list = read_file.split('\n')[:30]+current_list
            else:
                msgbox.showerror('직업 선택 오류', '관리자에게 "직업 선택 오류"라고 전달해주세요.')
                webbrowser.open('http://pf.kakao.com/_laxars/chat')
                sys.exit(0)
            with open(exe_path+'/MainFolder/filepath.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(write_file_list))
            msgbox.showinfo('파일 저장 완료', work_name+'의 커마 파일 저장이 완료되었습니다.')
    else:
        msgbox.showerror('저장 오류', work_choose)


def find_file(num):
    file_dir = filedialog.askopenfile(
        initialdir="/", title=num+"번 관문 BGM 파일 선택", filetypes=(("CUS files", "*.cus"), ("all files", "*.*")))
    if filedialog.Open():
        dir_name = file_dir.name
        file_name = file_dir.name.split('/')[-1]
        q5 = msgbox.askyesno(num+'번 슬롯 파일 선택 알림', num +
                             '번 슬롯 파일을 '+file_name+'으로 설정하시겠습니까?')
        if q5 == 1:
            if num == '1':
                slot1_filepath.set(dir_name)
            elif num == '2':
                slot2_filepath.set(dir_name)
            elif num == '3':
                slot3_filepath.set(dir_name)
            elif num == '4':
                slot4_filepath.set(dir_name)
            elif num == '5':
                slot5_filepath.set(dir_name)
            else:
                msgbox.showerror('슬롯 선택 오류', '관리자에게 "슬롯 선택 오류"라고 전달해주세요.')
                webbrowser.open('http://pf.kakao.com/_laxars/chat')


def restore_btn():
    if os.path.isfile(backup_path):
        q6 = msgbox.askquestion('파일 경로 복원', '커마 파일들의 경로를 복원하시겠습니까?')
        if q6 == 'yes':
            shutil.copyfile(backup_path, exe_path+'/MainFolder/filepath.txt')


def backup_btn():
    if os.path.isfile(backup_path):
        q7 = msgbox.askquestion(
            '파일 복원 확인', '해당 경로에 복원파일이 이미 존재합니다.\n파일을 덮어쓰시겠습니까?')
        if q7 == 'yes':
            shutil.copyfile(exe_path+'/MainFolder/filepath.txt', backup_path)


menu = Menu(root)
menu_update = Menu(menu, tearoff=0, relief='groove')
menu_update.add_command(label="커마 폴더 경로 확인", command=install_btn)
menu_update.add_command(label="현재 버전 확인", command=version_btn)
menu_update.add_command(label="업데이트 로그", command=update_log)
menu_chat = Menu(menu, tearoff=0, relief='groove')
menu_chat.add_command(label="오류 및 건의사항", command=link_btn)
menu_backup = Menu(menu, tearoff=0, relief='groove')
menu_backup.add_command(label="커마 파일 위치 복원하기", command=restore_btn)
menu_backup.add_command(label="커마 파일 위치 백업하기", command=backup_btn)

menu.add_cascade(label="정보", menu=menu_update)
menu.add_cascade(label="소통", menu=menu_chat)
menu.add_cascade(label="백업", menu=menu_backup)
root.config(menu=menu)

worklist = ['전사(남)', '무도가(남)', '무도가(여)', '헌터(남)', '헌터(여)', '마법사', '암살자']
work_combobox = tkinter.ttk.Combobox(root, height=15, values=worklist)
work_combobox.grid(row=0, column=0, padx=15, pady=15)
work_combobox.set("직업선택")
load_btn = Button(root, text='불러오기', command=load)
load_btn.grid(row=0, column=1)
slot1_filepath = StringVar()
slot2_filepath = StringVar()
slot3_filepath = StringVar()
slot4_filepath = StringVar()
slot5_filepath = StringVar()
slot1_filepath.set('비어있음')
slot2_filepath.set('비어있음')
slot3_filepath.set('비어있음')
slot4_filepath.set('비어있음')
slot5_filepath.set('비어있음')
slot1_filename = StringVar()
slot2_filename = StringVar()
slot3_filename = StringVar()
slot4_filename = StringVar()
slot5_filename = StringVar()
slot1_filename.set('비어있음')
slot2_filename.set('비어있음')
slot3_filename.set('비어있음')
slot4_filename.set('비어있음')
slot5_filename.set('비어있음')
slot1_name = Entry(root, textvariable=slot1_filename)
slot1_name.grid(row=1, column=0)
slot2_name = Entry(root, textvariable=slot2_filename)
slot2_name.grid(row=2, column=0)
slot3_name = Entry(root, textvariable=slot3_filename)
slot3_name.grid(row=3, column=0)
slot4_name = Entry(root, textvariable=slot4_filename)
slot4_name.grid(row=4, column=0)
slot5_name = Entry(root, textvariable=slot5_filename)
slot5_name.grid(row=5, column=0)
slot1_path = Label(root, textvariable=slot1_filepath, wraplength=100)
slot1_path.grid(row=1, column=1)
slot2_path = Label(root, textvariable=slot2_filepath, wraplength=100)
slot2_path.grid(row=2, column=1)
slot3_path = Label(root, textvariable=slot3_filepath, wraplength=100)
slot3_path.grid(row=3, column=1)
slot4_path = Label(root, textvariable=slot4_filepath, wraplength=100)
slot4_path.grid(row=4, column=1)
slot5_path = Label(root, textvariable=slot5_filepath, wraplength=100)
slot5_path.grid(row=5, column=1)
slot1_file = Button(root, text='1번슬롯 파일찾기', command=lambda: find_file('1'))
slot1_file.grid(row=1, column=2)
slot2_file = Button(root, text='2번슬롯 파일찾기', command=lambda: find_file('2'))
slot2_file.grid(row=2, column=2)
slot3_file = Button(root, text='3번슬롯 파일찾기', command=lambda: find_file('3'))
slot3_file.grid(row=3, column=2)
slot4_file = Button(root, text='4번슬롯 파일찾기', command=lambda: find_file('4'))
slot4_file.grid(row=4, column=2)
slot5_file = Button(root, text='5번슬롯 파일찾기', command=lambda: find_file('5'))
slot5_file.grid(row=5, column=2)
apply_btn = Button(root, text='적용하기', command=apply)
apply_btn.grid(row=6, column=0)
save_btn = Button(root, text='저장하기', command=save)
save_btn.grid(row=6, column=1)
root.mainloop()

# pyinstaller --uac-admin --clean --noconsole --icon=icon.ico --add-data='.\Lostark\CAL\CAL\MainFolder*;MainFolder' .\Lostark\CAL\CAL\CAL.py
