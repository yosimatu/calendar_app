import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors
from tkinter import messagebox


WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
#actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class YicDiary:
  def __init__(self, root, login_ID, login_name):
    #root = tk.Tk()
    self.write_name = login_name
    self.write_idx = login_ID
    self.user_ID = login_ID
    self.login_name = login_name
    
    self.root = root
    self.root.title('予定管理アプリ' + self.login_name + 'でログイン中')
    self.root.geometry('520x280')
    self.root.resizable(0, 0)
    self.root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(self.root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(self.root)
    rightFrame.grid(row=0, column=1)

    #rightFrame2 = tk.Frame(root)
    #rightFrame2.grid(row=0, column= 2)
    #rightFrame2 = rightFrame.grid(row=1, column=2)
    self.rightBuild(rightFrame)

    # 予定を表示する部分
    #rightFrame = tk.Frame(root)
    #rightFrame.grid()

    self.actions = self.get_actions()

    write_users_ID, self.users = self.get_users()
    self.user_idx = self.users.index(self.login_name)
    print(write_users_ID)
    print(self.users)


  def get_actions(self):
    connection = pymysql.connect(host='127.0.0.1',
                            user='root',
                            password='',
                            db='apri03',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    try:
      # トランザクション開始
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        # 日付からその日のデータを持ってくる
        sql = "select Plan_type from Plan_type_table;"
        cursor.execute(sql)

        results = cursor.fetchall()
        actions = []
        for my_list in results:
          actions.append(my_list["Plan_type"])

      connection.commit()

    except:
      print('error')
    
    finally:
      connection.close()
    
    return actions

  #--------------------------------------------------------------
  # userを求めるメソッド
  def get_users(self):
    connection = pymysql.connect(host='127.0.0.1',
                            user='root',
                            password='',
                            db='apri03',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    try:
      # トランザクション開始
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        # 日付からその日のデータを持ってくる
        sql = "select user_ID, user_name from user_table group by user_ID;"
        cursor.execute(sql)

        results = cursor.fetchall()
        print(results)
        users = []
        write_users_ID = []
        for idx, my_list in enumerate(results):
          users.append(my_list['user_name'])
          write_users_ID.append(my_list['user_ID'])

      connection.commit()

    except:
      print('error')
    
    finally:
      connection.close()
    
    return write_users_ID, users

  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)

  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)
    
    self.login_nameLabel = tk.Label(self.root, font=('', 10), text=self.login_name)
    self.login_nameLabel.place(x = (210 + 440) / 2 - 30, y = 250)
    beforButton2 = tk.Button(self.root, text='＜', font=('', 10), command=lambda:self.change_user(-1))
    beforButton2.place(x = 220, y = 250)
    nextButton2 = tk.Button(self.root, text='＞', font=('', 10), command=lambda:self.change_user(1))
    nextButton2.place(x = 440, y = 260, anchor=tk.CENTER)
    
    self.schedule()

  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    self.text = tk.Text(self.r2_frame, width=35, height=15)
    self.text.grid(row=1, column=0)
    scroll_v = tk.Scrollbar(self.r2_frame, orient=tk.VERTICAL)
    scroll_v.grid(row=1, column=1, sticky=tk.N+tk.S)
    #scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
    self.text["yscrollcommand"] = scroll_v.set

    self.date = "{}-{}-{}".format(self.year, self.mon, self.today)

    # データベースに予定の問い合わせを行う
    # デバック：引数をここでそろえてみるー－－－－－－－－－－－－－－－－－

    # labelから表示するuserを得る
    self.label_name = self.login_nameLabel.cget("text")
    #write_user_ID = self.select_write_user_ID(write_user_name)
    print("ラベルは" + self.label_name)
    # そのuserのIDを得る
    print("select_label_user_IDの実行")
    self.label_ID = self.select_label_user_ID()

    results = self.select_plan()
    print(results)

    if len(results) == 0:
      temp = "予定なし"
      self.text.insert(1.0, temp)

    else:
      for idx, my_list in enumerate(results):
        temp = "{} : {}".format(my_list['plan_type'], my_list['memo'])
        self.text.insert(float(idx), temp)

  def select_label_user_ID(self):
    #print("実行されたんゴ")
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apri03',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
      # トランザクション開始
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()

        sql = 'select user_ID from user_table where user_name = "{}";'.format(self.label_name)
        
        cursor.execute(sql)

        result = cursor.fetchone()

      connection.commit()

    except:
      print('error')
    
    finally:
      connection.close()
    print(self.label_name + "のIDは" + str(result['user_ID']))
    return result['user_ID']


  def select_plan(self):
    print("self.user_IDは" + str(self.user_ID))
    print("self.label_IDは" + str(self.label_ID))
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apri03',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
      # トランザクション開始
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        
        sql = 'select plan_type, memo from plan_table inner join plan_type_table ON \
        plan_table.plan_type_ID = plan_type_table.plan_type_ID where user_ID = {} and \
        plan_date = "{}";'.format(self.label_ID, self.date)
        cursor.execute(sql)

        results = cursor.fetchall()

      connection.commit()

    except:
      print('error')
    
    finally:
      connection.close()

    return results

  def change_user(self, argv):
    
    #print(self.login_name, self.user_idx)
    ist_lengs = len(self.users)
    self.user_idx += argv
    #print(self.users[self.user_idx])
    #print(len(self.users))
    if self.user_idx < 0:
      self.user_idx = len(self.users) - 1
    elif self.user_idx > len(self.users) - 1:
      self.user_idx = 0
    
    #print(self.users[self.user_idx])    
    self.login_nameLabel['text'] = self.users[self.user_idx]
  
    self.schedule()
    

  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    #self.sub_win.withdraw()
    if self.label_name == self.login_name:
      if self.sub_win == None or not self.sub_win.winfo_exists():
        self.sub_win = tk.Toplevel()
        self.sub_win.geometry("300x300")
        self.sub_win.title("予定の追加")
        self.sub_win.resizable(0, 0)

        # ラベル
        sb1_frame = tk.Frame(self.sub_win)
        sb1_frame.grid(row=0, column=0)
        temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
        title = tk.Label(sb1_frame, text=temp, font=('', 12))
        title.grid(row=0, column=0)

        # 予定種別（コンボボックス）
        sb2_frame = tk.Frame(self.sub_win)
        sb2_frame.grid(row=1, column=0)
        label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
        label_1.grid(row=0, column=0, sticky=tk.W)
        self.combo = ttk.Combobox(sb2_frame, state='readonly', values=self.actions)
        self.combo.current(0)
        self.combo.grid(row=0, column=1)

        # テキストエリア（垂直スクロール付）
        sb3_frame = tk.Frame(self.sub_win)
        sb3_frame.grid(row=2, column=0)
        self.text = tk.Text(sb3_frame, width=40, height=15)
        self.text.grid(row=0, column=0)
        scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
        scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.text["yscrollcommand"] = scroll_v.set

        # 保存ボタン
        sb4_frame = tk.Frame(self.sub_win)
        sb4_frame.grid(row=3, column=0, sticky=tk.NE)
        button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
        button.pack(padx=10, pady=10)
      elif self.sub_win != None and self.sub_win.winfo_exists():
        self.sub_win.lift()
    else:
      if self.sub_win == None or not self.sub_win.winfo_exists():
        messagebox.showerror("", "他のユーザーの予定は追加できません")
        '''
        self.sub_win = tk.Toplevel()
        self.sub_win.geometry("280x40")
        self.sub_win.title("")
        self.sub_win.resizable(0, 0)

        sb1_frame = tk.Frame(self.sub_win)
        sb1_frame.grid(row=0, column=0)
        temp = '他のユーザーの予定は追加できません'
        title = tk.Label(sb1_frame, text=temp, font=('', 12))
        title.grid(row=0, column=0)
        '''
        

      elif self.sub_win != None and self.sub_win.winfo_exists():
        self.sub_win.lift()

  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    # データベースに新規予定を挿入する
    # 引数を集める

    # 年月日 23行目 書き換え
    self.date = "{}-{}-{}".format(self.year, self.mon, self.today)
    # 予定の種類
    self.kinds = self.combo.get()
    # 予定の種類のID
    self.kinds_ID = self.get_kinds_ID()
    # 予定の内容
    self.memo =  self.text.get('1.0', 'end')
    print(self.date, self.kinds_ID, self.memo)

    # データベースに入れる
    self.insert_date()

    self.sub_win.destroy()
  
  # kind_IDを求めるメソッド
  def get_kinds_ID(self):
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apri03',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
      # トランザクション開始
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()

        sql = 'select Plan_type_ID from plan_type_table where Plan_type = "{}"'.format(self.kinds)
        cursor.execute(sql)

        result = cursor.fetchone()
        #print(result)

      connection.commit()

    except:
      print('error')
    
    finally:
      connection.close()
    
    return result["Plan_type_ID"]

  def insert_date(self):
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apri03',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
      # トランザクション開始
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()

        sql = 'insert into plan_table(user_ID, plan_date, plan_type_ID, memo) values({}, "{}", {}, "{}");'\
        .format(self.user_ID, self.date, self.kinds_ID, self.memo)
        cursor.execute(sql)

      connection.commit()

    except:
      print('error')
    
    finally:
      connection.close()

  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day
    
    self.schedule()


def Main():
  root = tk.Tk()
  YicDiary(root, 5, "野比のび太")
  root.mainloop()

if __name__ == '__main__':
  Main()
