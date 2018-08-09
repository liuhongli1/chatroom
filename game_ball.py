from tkinter import *
import random
import time #调用时间函数让游戏有真实感
paddle_pos1=None

def My_game():
#将对手排的w位置实时发过来和击球时的排的速度传入作为小球返回的速度的依据
    global ck
    tk = Tk()
    tk.title("Game") 
    #给窗口命名
    tk.resizable(0,0)
    #窗口的大小不可调整，第一个参数表示长，0，0的意思是“窗口的大小在水平方向上和垂直方向上都不能改变”
    tk.wm_attributes("-topmost",1)
    #将画布的窗口始终放到所有其他窗口之前
    canvas = Canvas(tk,width=500, height=400,bg='purple', bd=0, highlightthickness=0)#后两个参数作用：确保画布之外没有边框，使得屏幕更美观
    canvas.pack()
    tk.update()#为动画做好初始化
    ball_id = canvas.create_oval(10, 10, 20, 20, fill='red')#（10,10）表示左上角x,y坐标，（25,25）表示右下角x,y坐标，填充色
    canvas.move(ball_id, 245,195)#将球移动到画布中心
    # ball_paddle = paddle
    starts = [-3,-2,-1,1,2,3]
    random.shuffle(starts)
    # ball_x = starts[0]*paddle_x2
    ball_x = starts[0]
    ball_y = starts[0]
    paddle_id = canvas.create_rectangle(0, 0, 100, 10, fill='green') 
     # （10,10）
    paddle_id1 = canvas.create_rectangle(0, 0, 100, 10, fill='green')
    # 创建对手的排
    canvas.move(paddle_id, 200, 390)  # 自己的排放在最下面中间
    canvas.move(paddle_id1, 200, 0)#将对手的排放在最上方
    paddle_x = 0
    paddle_x1=0
    pos = canvas.coords(ball_id)
    paddle_pos=canvas.coords(paddle_id)
    paddle_pos1=canvas.coords(paddle_id1)
    def turn_left(evt):#改变向左向右的方向
        nonlocal paddle_x
        if paddle_pos[0]<=0 or paddle_pos[2]>=canvas.winfo_width():
            paddle_x=0      
        else:
            paddle_x = -1
    def turn_right(evt):
        nonlocal paddle_x
        if paddle_pos[0]<=0 or paddle_pos[2]>=canvas.winfo_width():
            paddle_x=0
            
        else:
            paddle_x = 1
    def turn_top(evt):
        nonlocal paddle_x
        if paddle_x==0:
            pass
        elif paddle_x<0:
            paddle_x-=1
        else:
            paddle_x+=1
    def turn_buttom(evt):
        nonlocal paddle_x
        if paddle_x == 0:
            pass
        elif paddle_x<0:
            paddle_x+=1
        else:
            paddle_x-=1
    def send_ready():
        def my_destroy():
            tk1.destroy()
        tk1=Tk()
        tk1.title("over")
        tk.resizable(0,0)
        label=Label(tk1,text='对方准备好了',fg='red',font='15')
        label.pack()
        buttom=Button(tk1,text='确定',bg='green',command=my_destroy)
        buttom.pack()
        tk1.mainloop()
    def send_go():
        nonlocal paddle_x
        nonlocal paddle_x1
        def my_destroy():
            nonlocal paddle_x1
            global ck
            tk1.destroy()
            time.sleep(3)
            while 1:
                if hit_bottom ==False:
                    ck.send(paddle_x.encode('utf-8'))
                    paddle_x1 =ck.recv(1024).decode('utf-8')
                    tub=draw(ball_id,paddle_id,paddle_id1)
                    
                else:
                    tk.update_idletasks()
                    tk.update()
                    time.sleep(0.01)
        tk1=Tk()
        tk1.title("over")
        tk.resizable(0,0)
        label=Label(tk1,text='确定后三秒游戏开始',fg='red',font='15')
        label.pack()
        buttom=Button(tk1,text='确定',bg='green',command=my_destroy)
        buttom.pack()
        tk1.mainloop()
    def play_agin():
        nonlocal hit_bottom
        nonlocal paddle_x
        nonlocal ball_x
        nonlocal ball_y
        nonlocal ball_id
        nonlocal pos
        nonlocal paddle_pos
        nonlocal paddle_pos1
        x=250-pos[0]
        hit_bottom ==False
        starts = [-3,-2,-1,1,2,3]
        random.shuffle(starts)
        ball_x = starts[0]
        ball_y = starts[0]
        paddle_x1=0
        paddle_x = 0
        canvas.move(ball_id, x,-200)
        send_go()
        # paddle_id = canvas.create_rectangle(0, 0, 100, 10, fill='green')
    def send_quit():
        tk.destroy()
    canvas.bind_all('<KeyPress-Left>', turn_left)
    canvas.bind_all('<KeyPress-Up>', turn_top)
    #按键时调用函数，< >内为 事件名字，让对象对操作有反应
    canvas.bind_all('<KeyPress-Down>', turn_buttom)
    canvas.bind_all('<KeyPress-Right>', turn_right)
    hit_bottom = False
    def draw(ball_id,paddle_id,paddle_id1):
        nonlocal hit_bottom
        nonlocal paddle_x
        nonlocal paddle_x1
        nonlocal ball_x
        nonlocal ball_y
        nonlocal pos
        nonlocal paddle_pos
        nonlocal paddle_pos1
        canvas.move(ball_id,ball_x,ball_y)
        canvas.move(paddle_id,paddle_x,0)
        canvas.move(paddle_id1,paddle_x1,0)
        pos = canvas.coords(ball_id)
        paddle_pos1=canvas.coords(paddle_pos1)
        paddle_pos=canvas.coords(paddle_pos)
        if paddle_pos[0]<0:
            paddle_x=0
            paddle_pos[0]=0
            paddle_pos[2]=100
            
        elif paddle_pos[2]>canvas.winfo_width():
            paddle_x=0
            paddle_pos[0]=canvas.winfo_width()-100
            paddle_pos[2]=canvas.winfo_width()
        else:
            paddle_pos=canvas.coords(paddle_id)
        def my_destroy():
            tk1.destroy()
        if pos[0] == paddle_pos1[2]or pos[1]<=paddle_pos[3] or pos[2]>=paddle_pos[0]:
            ball_y = -ball_y
        elif pos[1] <= 0:
            tk1=Tk()
            tk1.title("over")
            tk.resizable(0,0)
            label=Label(tk1,text='你赢了',fg='red',font='15')
            label.pack()
            buttom=Button(tk1,text='确定',bg='green',command=my_destroy)
            buttom.pack()
            tk1.mainloop()
        if pos[3] == paddle_pos[1]or pos[0]<=paddle_pos[2] or pos[2]>=paddle_pos[0]:
            ball_y = -ball_y
        elif pos[3] >= canvas.winfo_height():
            tk1=Tk()
            tk1.title("over")
            tk.resizable(0,0)
            label=Label(tk1,text='你输了',fg='red',font='15')
            label.pack()
            buttom=Button(tk1,text='确定',bg='green',command=my_destroy)
            buttom.pack()
            tk1.mainloop()
            return 'Fail'
        elif pos[0]==paddle_pos[2] and 390<=pos[3]>=400:
            ball_y = -ball_y
        elif pos[0] <= 0:
            ball_x = -ball_x
        elif pos[2]==paddle_pos[0]and 390<=pos[3]>=400:
            ball_y = -ball_y
        elif pos[2] >= canvas.winfo_width():
            ball_x = -ball_x
    frame = Frame(tk)
    frame.pack()
    button1=Button(frame,text='准备',command=send_ready).pack(side=LEFT)
    button2=Button(frame,text='开始',command=send_go).pack(side=LEFT)
    button3=Button(frame,text='再来一局',command=play_agin).pack(side=LEFT)
    buttom4=Button(frame,text='退出',command=send_quit).pack(side=LEFT)    

        
   

    tk.mainloop()
if __name__ == '__main__':
    My_game()