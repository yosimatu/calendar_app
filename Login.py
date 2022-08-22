import tkinter
import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors
from YicDiary import YicDiary

class Login():
    '''ログインを制御するクラス'''

    def __init__(self, root, main):
        '''コンストラクタ
            master:ログイン画面を配置するウィジェット
            body:アプリ本体のクラスのインスタンス
        '''
        root.title('ログイン画面')

        # メインウィンドウのサイズ設定
        root.geometry("520x280")

        self.master = root

        # アプリ本体のクラスのインスタンスをセット
        self.main = main

        # ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        # ログイン画面のウィジェット作成
        self.create_widgets()

    def create_widgets(self):
        '''ウィジェットを作成・配置する'''

        # ユーザー名入力用のウィジェット
        self.name_label = tkinter.Label(
            self.master,
            text="ユーザー名"
        )
        self.name_label.grid(
            row=0,
            column=0
        )
        self.widgets.append(self.name_label)

        self.name_entry = tkinter.Entry(self.master)
        self.name_entry.grid(
            row=0,
            column=1
        )
        self.widgets.append(self.name_entry)

        # パスワード入力用のウィジェット
        self.pass_label = tkinter.Label(
            self.master,
            text="パスワード(半角8文字)"
        )
        self.pass_label.grid(
            row=1,
            column=0
        )
        self.widgets.append(self.pass_label)

        self.pass_entry = tkinter.Entry(
            self.master,
            show="*"
        )
        self.pass_entry.grid(
            row=1,
            column=1
        )
        self.widgets.append(self.pass_entry)

        # ログインボタン
        self.login_button = tkinter.Button(
            self.master,
            text="ログイン",
            command=self.login
        )
        self.login_button.grid(
            row=2,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.login_button)

        # 登録ボタン
        self.register_button = tkinter.Button(
            self.master,
            text="登録",
            command=self.register
        )
        self.register_button.grid(
            row=3,
            column=0,
            columnspan=2,
        )
        self.widgets.append(self.register_button)

        # ウィジェット全てを中央寄せ
        self.master.grid_anchor(tkinter.CENTER)
    
    def login(self):
        username = self.name_entry.get()
        password = self.pass_entry.get()

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
                sql = 'select user_ID, user_name from User_table WHERE User_name = "{}" and User_password = "{}";'.format(username, password)
            
                cursor.execute(sql)

                results = cursor.fetchone()
                print(results)
                #print(results["exists"])
                if results == None:
                    #print('None')
                    self.fail()
                else:
                    #print('ログイン')
                    self.login_ID, self.login_name = results["user_ID"], results["user_name"]
                    self.success()

                # 登録されていなければ
                

            connection.commit()

        except:
            print('error')
        
        finally:
            connection.close()
    
    def register(self):
        '''ユーザー名とパスワードを登録する'''

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()
    
        print(username)
        print(password)

        connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apri02',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

        try:
            # トランザクション開始
            connection.begin()
            with connection.cursor() as cursor:
                cursor = connection.cursor()

                print('INSERT INTO User_table(User_name, User_password) VALUES(,);の実行')
                sql = 'INSERT INTO User_table(User_name, User_password) VALUES("{}","{}");'.format(username,password)
                cursor.execute(sql)

            connection.commit()

        except:
            print('error')
            
        finally:
            connection.close()

    def fail(self):
        '''ログイン失敗時の処理を行う'''

        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに失敗しました"メッセージを表示
        self.message = tkinter.Label(
            self.master,
            text="ログインに失敗しました",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tkinter.CENTER
        )

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.redisplay)

    def redisplay(self):
        '''ログイン画面を再表示する'''

        # "ログインできませんでした"メッセージを削除
        self.message.destroy()

        # ウィジェットを再度作成・配置
        self.create_widgets()

    def success(self):
        '''ログイン成功時の処理を実行する'''
        
        # 表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        # "ログインに成功しました"メッセージを表示
        self.message = tkinter.Label(
            self.master,
            text="ログインに成功しました",
            font=("",40)
        )
        self.message.place(
            x=self.master.winfo_width() // 2,
            y=self.master.winfo_height() // 2,
            anchor=tkinter.CENTER
        )
        
        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.main_start)

    def main_start(self):
        '''アプリ本体を起動する'''

        # "ログインに成功しました"メッセージを削除
        self.message.destroy()

        # アプリ本体を起動
        self.main.start(self.login_ID, self.login_name)
        #self.master.destroy()
        
class MainAppli():
    '''アプリ本体'''

    def __init__(self, master):
        '''
            コンストラクタ
            master:ログイン画面を配置するウィジェット
        '''

        self.master = master

        # ログイン完了していないのでウィジェットは作成しない

    def start(self, login_ID, login_name):
        '''アプリを起動する'''

        # ログインユーザー名を表示する
        self.message = tkinter.Label(
            self.master,
            font=("",40),
            text=login_name + "でログイン中"
        )
        self.message.pack()
        #self.master.destroy()
        self.master.destroy()

        root = tk.Tk()
        YicDiary(root, login_ID, login_name)
        root.mainloop()
        #self.Login.main_start()

        # 必要に応じてウィジェット作成やイベントの設定なども行う
    

app = tkinter.Tk()

#app.title('ログイン画面')

# メインウィンドウのサイズ設定
#app.geometry("600x400")

# アプリ本体のインスタンス生成
main = MainAppli(app)

# ログイン管理クラスのインスタンス生成
login = Login(app, main)

app.mainloop()