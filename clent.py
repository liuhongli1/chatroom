from tkinter import *
import socket
import threading
from time import sleep,ctime
import random 
from game_ball import *
# from voice import *
ck = None#用于储存客户端的信息

data_list=None
# def getInfo():
#     while True:
#         data = ck.recv(1024)#用于接受服务其发送的信息
#         text.insert(INSERT, data.decode("utf-8"))#显示在信息框上


def connectServer():
    global ck
    ipStr = eip.get()
    portStr = eport.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6，和相关协议的
    client.connect((ipStr, int(portStr)))#连接ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    #2:bind()的参数是一个元组的形式
    ck = client


def sendMail():
    friend = efriend.get()
    sendStr = esend.get()
    sendStr = friend + ":" + sendStr
    ck.send(sendStr.encode("utf-8"))
class AppRegister(Toplevel):
    def __init__(self):
        # self.tk=Tk(className="欢迎注册")
        super().__init__()
        self.title('注册用户')
        self.name=' '
        self.password=' '
        self.loginfunc()
    def loginfunc(self):
        self.frame1 = Frame(self)  
        self.frame1.pack()
        self.label = Label(self.frame1,text="输入帐号")
        self.label.pack(side=LEFT)
        self.text = StringVar()
        self.text.set('')
        self.entry=Entry(self.frame1 )
        self.entry['textvariable']=self.text
        self.entry.pack(side=LEFT)
        

        self.frame2 = Frame(self)  
        self.frame2.pack()
        self.label = Label(self.frame2,text="输入密码")
        self.label.pack(side=LEFT)
        self.text1 = StringVar()
        self.text1.set('')
        self.entry=Entry(self.frame2,show='*',\
            textvariable=self.text1)
        self.entry.pack(side=LEFT)

        self.frame3 = Frame(self)  
        self.frame3.pack()
        self.label = Label(self.frame3,text='确认密码')
        self.label.pack(side=LEFT)
        self.text2 = StringVar()
        self.text2.set('')
        self.entry=Entry(self.frame3,show='*',\
            textvariable=self.text2)
        self.entry.pack(side=LEFT)

        #构造函数里传入一个父组件(master),创建一个Frame组件并显示  
        self.frame = Frame(self)  
        self.frame.pack()
        #创建两个button，并作为frame的一部分  
        self.button = Button(self.frame, text="QUIT",\
         fg="red", command=self.my_quit)  
        self.button.pack(side=LEFT) 
        #此处side为LEFT表示将其放置 到frame剩余空间的最左方  
        self.hi_there = Button(self.frame, text="ensure", \
            fg='green',command=self.say_hi)  
        self.hi_there.pack(side=LEFT)
    def do_prompt(self,num):
        self.tk1=Tk(className='prompt')
        if num == 1:
            self.label=Label(self.tk1,text='用户名或密码不能有空格',fg='red')
            self.label.pack()
        elif num ==2:
            self.label=Label(self.tk1,text='密码和帐号都不能空缺',fg='red')
            self.label.pack()
        elif num ==3:
            self.label=Label(self.tk1,text='两次输入密码必须一致',fg='red')
            self.label.pack()
        self.button=Button(self.tk1,text='确认',fg='yellow',\
            command=self.my_quit1)
        self.button.pack()
    def say_hi(self):
        self.name = self.text.get()
        self.password = self.text1.get()
        self.password1=self.text2.get()
        if self.password == self.password1:
            if (' ' in self.name)or(' ' in self.password):
                self.do_prompt(1)
            elif (not self.name) or (not self.password):
                self.do_prompt(2)
            else:
                self.name = self.name.replace("$",'$0')
                self.password = self.password.replace("$",'$0')
                self.name = self.name.replace("'",'$1')
                self.name = self.name.replace(">",'$2')
                self.name = self.name.replace("<",'$3')
                self.password = self.password.replace("'",'$1')
                self.password = self.password.replace(">",'$2')
                self.password = self.password.replace("<",'$3')    
                self.destroy()
        else:
            self.do_prompt(3)
        # print('确认登录')
        
    def my_quit1(self):
        self.tk1.destroy()
    def my_quit(self):
        self.destroy()
def my_register():
    global ck
    def my_destroy():
        tk1.destroy()
    appRegister = AppRegister()
    win.wait_window(appRegister)
    Arr =(appRegister.name,appRegister.password)
    cmd = 'R'+' '+Arr[0]+' '+Arr[1]
    ck.send(cmd.encode('utf-8'))
    data = ck.recv(1024).decode()
    tk1=Tk()
    tk1.title='提示'
    def my_destroy():
        tk1.destroy()
    if data == 'OK':
        print('注册成功')
        
        lam=Label(tk1,text='注册成功，可以登录',fg='red')
        lam.pack()
        
    else:
        lam=Label(tk1,text='注册失败'+'data'+'请重新注册',fg='red')
        lam.pack()
    button4=Button(tk1,text='确定',command=my_destroy)
    button4.pack()
    tk1.mainloop()
def chat_room(user_list,zai_list,name,ck):
 
  ###******回调函数定义******###

    #创建窗口 
    t = Tk()
    t.title('超级聊天窗口')     # 窗口名称
    t.resizable(0, 0)           # 禁止调整窗口大小
    user_list=user_list
    name=name
    zai_list.append('小刘')
    print(user_list)
    
    def My_recv(ck):
      global data_list
      while True:
        data = ck.recv(4096).decode('utf-8')
        data_list = data.split(' ')
        if data_list[0] =='OK':
          txtRecv=ctime().split(' ')[3]+data_list[1]+':进入聊天室\n'
          txtMsgFbList.insert(END, txtRecv, 'greencolor') 
        elif data_list[0]=='E':
          txtMsgFbList.insert(END, data_list[1]+'\n', 'greencolor') 
        elif data_list[0] =='C':
          txtMsgFbList.insert(END, data_list[1]+'\n', 'greencolor')
        elif data_list[0] =='R': 
          txtText.delete(END)
          cmd_List=data_list[1].split('\n')
          for x in cmd_List:
            txtText.insert(END,x)
        elif data_list[0]=='S':
          timeText.delete(0.0,END)
          cmd = ' '.join(data_list)
          cmd=cmd[1::]
          timeText2.insert(END,cmd,'greencolor')
        elif data_list[0]=='GR':
          print('hellogr')
          cmd = ctime().split(' ')[3]+data_list[1]+'向你发起打球挑战'
          txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
          request_game_button['text']='接受挑战'
          request_game_button['command']=accept_game_repuest
        elif data_list[0]=='GI':
          print('hellogi')
          cmd = ctime().split(' ')[3]+data_list[1]+'已经进入游戏'
          txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
          request_game_button['text']='追杀上去'
          request_game_button['command']=into_game
          break
        elif data_list[0]=='GA':
          print('helloga')
          cmd = ctime().split(' ')[3]+data_list[1]+'已经接受挑战'
          txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
          request_game_button['text']='进入游戏'
          request_game_button['command']=into_game
          quit_game_button=Button(frameA4,text='放弃',command=quit_game_msg)
          quit_game_button.pack(side.LEFT)
        elif data_list[0]=='GQ':
          print('hellogq')
          cmd = ctime().split(' ')[3]+data_list[1]+'怂包了，放弃'
          txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
          request_game_button['text']='发起游戏挑战'
          request_game_button['command']=send_game_msg

    th1=threading.Thread(target=My_recv,args=(ck,))
    th1.daemon =True
    th1.start()
    def sendMsg(): 
      global ck
      # global name
      textmsg=txtMsg.get('0.0', END)
      Link_man=entrySerch.get('0.0', END)
      Link_man=Link_man.replace('\n','')
      print('#'+Link_man+'#')
      if Link_man:
        print('*****')
        if Link_man=='小刘':
          cmd='S'+' '+Link_man+" "+name+' '+textmsg
        else:
          cmd='#'+' '+Link_man+" "+name+' '+textmsg
        
      else:
        cmd ='#'+' '+'anyone'+' '+name+' '+textmsg
        print('anyone') 
      ck.send(cmd.encode('utf-8'))
      txtMsg.delete('0.0',END)
      entrySerch.delete('0.0',END)
       
    def cancelMsg():                #取消消息
      txtMsg.delete('0.0', END)

    def sendMsgEvent(event):        #发送消息事件
      if event.keysym == "Return":  #按回车键可发送
        sendMsg()
    def message():
      # global user_list

      if entrySerch.get('0.0', END).replace('\n','') in zai_list:
        cmd=ctime().split(' ')[3]+'你查询的人在线'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
      else:
        cmd=ctime().split(' ')[3]+'你查询的人不在线'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
        entrySerch.delete('0.0', END)
    def sendSchEvent(event):
      if event.keysym =='Return':
        message()
    def voiceMsg():
      cmd=my_voice()
      cmd_list=cmd.split(' ')
      if cmd_list[0]=='OK':
        txtMsg.insert(END, cmd_list[1]+'\n', 'greencolor')
      else:
        timeText.delete('0.0',END)
        timeText.insert(END, cmd_list[1]+'\n', 'greencolor')
    def quitMsg():
      global ck 
      cmd = 'E'+' '+name
      ck.send(cmd.encode('utf-8'))
      ck.close()
      t.destroy()
    def Oval():               
      imgCanvas.create_oval(110, 20, 170, 120)
    def Polygon():
      imgCanvas.create_polygon(20, 20, 110, 50,100,110,40,120)

    def fontSize(ev=None):          #字体缩放
      timeText2.config(font='Helvetica -%d bold' % sizeScale.get())
      sizeLabel.config(text='字号：%d'% sizeScale.get())

    def txtlist():                  #字典实现--书名与内容的对应
      book={'NO.1 《平凡的世界》  路遥':'1.一个平平常常的日子，细蒙蒙的雨丝夹着一星半点的雪花，正纷纷淋淋的向大地飘洒着，时令已快到惊蛰，雪当然再不会存留，往往还没等落地，就消失的无踪无影了，黄土高原严寒而漫长的冬天看来就要过去，但那真正温暖的春天还远远没有到来。\n2、这时候，他也体验到了类似孙少平的那种感觉：只有繁重的体力劳动才使精神上的痛苦变为某种麻木，以致思维局限在机械性活动中。\n3、哭，笑，都是因为欢乐，哭的人知道而笑的人不知道，这欢乐是多少痛苦所换来的。',
            'NO.2 《看见》  柴静':'1.写本身也是一种发现自己的过程，你不写永远都知道自己身上发生了什么。\n2.保持对不同论述的警惕，才能保持自己的独立性。\n3.灵魂变得沉重，是因为爱，因为所爱的东西，眼睁睁在失去，却无能为力。\n4.我可能做不到更好了，但还是要像朱光潜说的那样，此时，此地，此身，此时我能做的事情绝不推诿到下一时刻，此地我能做的事情绝不换另一种境地再去做，此身我能做的事绝不妄想与他人来替代。\n5.如果带着强烈的预设和反感，你就没有办法真的认识这个人。',
            'NO.3 《亲爱的安德烈》龙应台':'1.我也要求你读书用功，不是因为我要你跟别人比较成就，而是因为，我希望你将来会拥有会选择的权利，选择有意义、有时间的工作，而不是被迫谋生。 当你的工作在你的心中有意义，你就有成就感。当你的工作给你时间，不剥夺你的生活，你就有尊严。成就感和尊严，给你快乐。\n2.农村中长大的孩子，会接触更真实的社会，接触更丰富的生活，会感受到人间的各种悲欢离合。所以更能形成那种原始的，正面的价值观—那“愚昧无知”的渔村，确实没有给我知识，但是给了我一种能力，悲悯同情的能力，使得我在日后面对权利的傲慢、欲望的嚣张和种种时代的虚假时，仍旧得以穿透，看见文明的核心关怀所在。'}
      txtText.delete(0.0,END)
      txtText.insert(END,book[txtSpinbox.get()])
   
    ###******回调函数定义******###
      
    def sendFindMsg():
      global ck
      numMsg1=numMsg.get()
      findManMsg1=findManMsg.get()
      cmd='Q'+' '+name+' '+findManMsg1+' '+numMsg1
      if numMsg1:
        if findManMsg1:
          if findManMsg1 in user_list:
            ck.send(cmd.encode('utf-8'))
          else:
            txtText.insert(END,'您输入的搜索人有错误','greencolor')
        else:
          cmd='Q'+' '+name+' '+'#'+' '+numMsg1
          ck.send(cmd.encode('utf-8'))
      else:
        if findManMsg1:
          if findManMsg1 in user_list:
            cmd='Q'+' '+name+' '+findManMsg1+' '+'0'
            ck.send(cmd.encode('utf-8'))
          else:
            txtText.insert(END,'您输入的搜索人有错误','greencolor')
        else:
          cmd='Q'+' '+name+' '+'#'+' '+'0'
          ck.send(cmd.encode('utf-8'))
      print(numMsg.get())
      print(findManMsg.get())
    
         

    ###******创建frame容器******###

    #第一列
    frmA1 = Frame(width=180, height=30)
    frmA2 = Frame(width=180, height=290)
    frmA3 = Frame(width=180, height=140,bg="green") 
    frmA4 = Frame(width=180, height=30)
    ###******窗口布局******### 
    frmA1.grid(row=0, column=0, padx=10, pady=3)
    frmA2.grid(row=1, column=0, padx=10)
    frmA3.grid(row=2, column=0, rowspan=1)
    frmA4.grid(row=3, column=0, rowspan=1)

    #第二列
    frmB1 = Frame(width=350, height=320)
    frmB2 = Frame(width=350, height=150)
    frmB3 = Frame(width=350, height=30)
      ###******窗口布局******###
    frmB1.grid(row=0, column=1, columnspan=1, rowspan=2, padx=1, pady=3)
    frmB2.grid(row=2, column=1, columnspan=1, padx=1, pady=1)
    frmB3.grid(row=3, column=1, columnspan=1, padx=1)

    #第三列
    frmC1 = Frame(width=300, height=30)
    frmC11= Frame(width=300, height=290)
    frmC2 = Frame(width=300, height=150)
    frmC3 = Frame(width=300, height=30)
    ###******窗口布局******##
    frmC1.grid(row=0, column=2, rowspan=1, padx=1, pady=1)
    frmC11.grid(row=1, column=2, rowspan=1, padx=1, pady=1)  
    frmC2.grid(row=2, column=2, rowspan=1, padx=1, pady=1)
    frmC3.grid(row=3, column=2, padx=1)
    
    #固定大小
    frmA1.grid_propagate(0)
    frmA2.grid_propagate(0)
    frmA3.grid_propagate(0)
    frmA4.grid_propagate(0)

    frmB1.grid_propagate(0)
    frmB2.grid_propagate(0)
    frmB3.grid_propagate(0)

    frmC1.grid_propagate(0)
    frmC11.grid_propagate(0)  
    frmC2.grid_propagate(0)
    frmC3.grid_propagate(0)
    ###******创建frame容器******###


    ###******创建控件******###

    #1.Text控件
    txtMsgFbList = Text(frmB1)                          #frmB1表示父窗口
    #创建并配置标签tag属性
    txtMsgFbList.tag_config('greencolor',               #标签tag名称
                          foreground='#008C00')       #标签tag前景色，背景色为默认白色
    txtMsg = Text(frmB2);
    txtMsg.bind("<KeyPress-Return>", sendMsgEvent)    #事件绑定，定义快捷键

    timeText=Text(frmC2,font=("Times", "28", "bold italic"),height=1,bg="PowderBlue")
    timeText2=Text(frmC2,fg="blue",width=40,font=("Times", "12","bold italic"))

                                                   # insert(插入位置，插入内容)
    #2.Button控件
    btnSend = Button(frmB3, text='发 送', width = 8,cursor='heart', command=sendMsg)
    btnCancel = Button(frmB3, text='取消', width = 8,cursor='shuttle', command=cancelMsg)
    btnSerch=Button(frmA1, text='搜索',         #button的显示内容
                    width = 9,height=1,               #宽和高
                    cursor='man',                     #光标样式     
                    command =message)                 #回调函数
    btnQuit = Button(frmB3, text='退出', width = 8,cursor='shuttle', fg='red',command=quitMsg)
    btnVoice = Button(frmB3, text='语音输入', width = 8,cursor='shuttle', fg='red',command=voiceMsg)
    #3.Entry控件
    txtMsg = Text(frmB2);
    txtMsg.bind("<KeyPress-Return>", sendMsgEvent)
    entrySerch=Text(frmA1, height=1,bd =3,width=18,font=("Times", "8", "bold italic"))                        #输入值以掩码显示    
    entrySerch.bind('<KeyPress-Return>',sendSchEvent)
    #4.Scrollbar控件
    scroLianxi = Scrollbar(frmA2,width=22,cursor='pirate',troughcolor="blue") 

    #5.Listbox控件
    listLianxi = Listbox(frmA2, width=22,height=16,
                         yscrollcommand = scroLianxi.set )  #连接listbox 到 vertical scrollbar
    listLianxi.insert(END,'智能人  ------小刘')
    for List in user_list:
      if List == 'OK':
        pass
      else:
        listLianxi.insert(END, "  联系人   ------" + str(List))
    scroLianxi.config( command = listLianxi.yview )   #scrollbar滚动时listbox同时滚动

    #6.Canvas控件
    # imgCanvas=Canvas(frmA3,bg='ivory')
    def game_one_Send():
      # global user_list

      if game_one_Text.get('0.0', END).replace('\n','') in zai_list:
        cmd=ctime().split(' ')[3]+'你挑战的人在线'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
      else:
        cmd=ctime().split(' ')[3]+'你挑战的人不在线，请选择别人'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
        game_one_Text.delete('0.0', END)
    def game_Event(event):
      if event.keysym =='Return':
        game_one_Send()
    def send_game_msg():
      if game_one_Text.get('0.0', END).replace('\n','') in zai_list:
        cmd=game_one_Text.get('0.0', END).replace('\n','')
        print(cmd+'*')
        cmd ='GR'+' '+name+' '+cmd
        ck.send(cmd.encode('utf-8'))
        cmd=ctime().split(' ')[3]+'你挑战的人在线'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
      else:
        cmd=ctime().split(' ')[3]+'你挑战的人不在线,请选择别人'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
        game_one_Text.delete('0.0', END)
    def into_game_msg():
      if game_one_Text.get('0.0', END).replace('\n','') in zai_list:
        cmd=game_one_Text.get('0.0', END).replace('\n','')
        print(cmd+'*')
        cmd ='GI'+' '+name+' '+cmd
        ck.send(cmd.encode('utf-8'))
        cmd=ctime().split(' ')[3]+'你挑战的人在线'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
      else:
        cmd=ctime().split(' ')[3]+'你挑战的人不在线,请选择别人'
        txtMsgFbList.insert(END, cmd+'\n', 'greencolor')
        game_one_Text.delete('0.0', END)
    def accept_game_repuest():
      cmd = 'GA'+' '+name+game_one_Text.get('0.0', END)
      ck.send(cmd.encode('utf-8'))
    def into_game():
      cmd = 'EG'+' '+name
      ck.send(cmd.encode('utf-8'))
      t.destroy()
      My_game(data_list[1])
    def quit_game_msg():
      cmd='GQ'+' '+name
      ck.send(cmd.encode('utf-8'))
    frmA31=Frame(frmA3,bg="PowderBlue",width=180, height=20)
    frmA32=Frame(frmA3,bg="PowderBlue",width=180, height=30)
    frmA33=Frame(frmA3,bg="PowderBlue",width=180, height=30)
    frmA34=Frame(frmA3,bg="PowderBlue",width=180, height=30)
    frmA35=Frame(frmA3,bg="PowderBlue",width=180, height=30)
    frmA31.grid(row=0,column=0)
    frmA32.grid(row=1,column=0)
    frmA33.grid(row=2,column=0)
    frmA34.grid(row=3,column=0)
    frmA35.grid(row=4,column=0)

    game_label=Label(frmA31,text='展示你的球技',bg="PowderBlue",fg='green')
    game_label.pack()
    game_one_Text=Text(frmA32,height=1,width=25,bg="PowderBlue")
    game_one_Text.bind("<KeyPress-Return>", game_Event)    #事件绑定，定义快捷键
    game_one_Text.grid(row=0,column=0)
    game_one_button=Button(frmA33,text='确定对手',command=game_one_Send)
    game_one_button.grid(row=0,column=1)
    game_msg_Text=Text(frmA35,height=1,width=25,bg="PowderBlue")    #事件绑定，定义快捷键
    game_msg_Text.grid(row=0,column=0)
    game_msg_label=Label(frmA34,text='告诉对手')
    game_msg_label.grid(row=0,column=0)
    request_game_button=Button(frmA4,text='发出游戏挑战',command=send_game_msg)
    
    request_game_button.pack(side=LEFT)
    # #7.Radiobutton控件
    # var = IntVar()                                    #设置variable和value可以保证只有一个按钮被按下
    # R1 = Radiobutton(frmA4, text="多边形", variable=var, value=1,command=Polygon)
    # R2 = Radiobutton(frmA4, text="椭圆", variable=var, value=2,command=Oval)

    # #8.Menubutton控件
    # colorMenubt =  Menubutton (frmA4, text="画板颜色", relief=RAISED )

    # #9.Menu控件
    # colorMenubt.menu  =  Menu ( colorMenubt, tearoff = 0 )
    # colorMenubt["menu"]  =  colorMenubt.menu

    # colorMenubt.menu.add_checkbutton ( label="红色",command=red)
    # colorMenubt.menu.add_checkbutton ( label="绿色",command=green)
    # colorMenubt.menu.add_checkbutton ( label="蓝色",command=blue)
    # colorMenubt.menu.add_separator()       #添加菜单分隔符
    # colorMenubt.menu.add_checkbutton ( label="连续色",command=color1)

    #10.Scale控件
    sizeScale = Scale(frmC3,length=135,width=18,from_=10, to=35,orient=HORIZONTAL,command=fontSize,cursor='star',
                      showvalue=0,         #不显示数值
                      sliderlength=30,     #滑块的长度             
                      troughcolor='ivory') #滑动条底色
    sizeScale.set(20)                      #设置滑块的初始值

    #11.Label控件
    sizeLabel = Label(frmC3,width=8,height=1,bd=1, relief=RIDGE)
    nameLabel = Label(frmC1, text='      附加功能  ',font="Times 16 bold italic")

    #12.Spinbox控件
    frmc111=Frame(frmC11,width=40)
    frmc111.grid(row=0,column=0)
    numMsg=StringVar()
    # numMsg.set('#')
    numMsgEntry = Entry(frmc111,width=5,textvariable=numMsg)
    numMsgEntry.pack(side=LEFT)
    numLabel=Label(frmc111,text = '记录数',)
    numLabel.pack(side = LEFT)
    findManMsg=StringVar()
    # findManMsg.set('#')
    findManMsgEntry = Entry(frmc111,width=5,textvariable=findManMsg)
    findManMsgEntry.pack(side=LEFT)
    numLabel1=Label(frmc111,text = '搜索人')
    numLabel1.pack(side = LEFT)
    findrecondBtn=Button(frmc111,text='查询',command=sendFindMsg)
    findrecondBtn.pack(side=LEFT)
    ###******创建控件******###


#-----------------------------------------------------------------------------
    
    frmC112=Frame(frmC11,width=40,height=13)
    frmC112.grid(row=1,column=0)
    scrolly = Scrollbar(frmC112)
    scrolly.pack(side=RIGHT, fill=Y)
    txtText = Listbox(frmC112,width=40, height=13, yscrollcommand=scrolly.set)
    # for x in range(1,5):
    #     txtText.insert(END,x)
    #     sleep(1)
    #     txtText.delete(END)
    txtText.pack()
    scrolly.config(command=txtText.yview)

#------------------------------------------------------------------

    ###******控件布局******### 

    btnSend.grid(row=0, column=0)
    btnCancel.grid(row=0, column=1)
    btnQuit.grid(row=0,column=2)
    btnVoice.grid(row=0,column=3)
    btnSerch.grid(row=0,column=1)

    nameLabel.grid()
    sizeLabel.grid(row=0,column=0)

    txtMsgFbList.grid()
    txtMsg.grid()

    entrySerch.grid(row=0,column=0)

    scroLianxi.grid(row=0,column=1,ipady=120)

    listLianxi.grid(row=0,column=0)

    timeText.grid(row=0,column=0)
    timeText2.grid(row=1,column=0,sticky=E+W)
    # txtText.grid(row=1,column=0,pady=5)

    sizeScale.grid(row=0,column=1)

    t.mainloop()
def my_login():
    global ck
    def my_destroy():
        tk1.destroy()
        if user_list[0] =='OK':
            sleep(0.2)
            win.destroy()
            chat_room(user_list,zai_list,name,ck)
    name = euser.get()      
    cmd='L'+' '+name+' '+epwd.get()
    ck.send(cmd.encode('utf-8'))
    data = ck.recv(1024).decode('utf-8')
    
    user_list1=data.split(' ')
    print(user_list1[-1])
    Sunnum = int(user_list1[-1])
    user_list=user_list1[0:Sunnum+1]
    zai_list=user_list1[Sunnum+1:]
    tk1=Tk()
    tk1.title='提示'
    if user_list[0] == 'OK':
        lam=Label(tk1,text='登录成功',fg='red')
        lam.pack()
        
    else:
        lam=Label(tk1,text='登录失败请重新输入',fg='red')
        lam.pack()
    button4=Button(tk1,text='确定',command=my_destroy)
    button4.pack()
    tk1.mainloop()
def my_quit():
    print('退出客户端')
    win.destroy()


#下面是界面

win =Tk()
win.title("客户端2")
win.geometry("300x200")
labelIp = Label(win, text="ip").grid(row=1, column=0)
eip = Variable()
entryIp = Entry(win, textvariable=eip).grid(row=1, column=1)

labelPort = Label(win, text="port").grid(row=2, column=0)
eport = Variable()

entryPort = Entry(win, textvariable=eport).grid(row=2, column=1)

button = Button(win, text="启动", command=connectServer).grid(row=3, column=0)


labelUse = Label(win, text="userName").grid(row=4, column=0)
euser = Variable()
entryUser = Entry(win, textvariable=euser).grid(row=4, column=1)
labelUse = Label(win, text="userPassword").grid(row=5, column=0)
epwd = Variable()
entryUser = Entry(win, show='*',textvariable=epwd).grid(row=5, column=1)
frame=Frame(win).grid(row=6)
button1=Button(frame, text='注册', \
             fg ='red' ,command=my_register)
button1.grid(row=6, column=0)
button2=Button(frame, text='登录', \
            fg ='red', command=my_login)
button2.grid(row=6, column=1)
button3=Button(frame, text='退出', \
            fg ='red' ,command=my_quit)
button3.grid(row=6, column=2)
win.mainloop()
