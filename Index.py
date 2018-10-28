from tkinter import *
import Tkinter
import tkMessageBox
from tkinter import Text
from index import index_calc
import Twitter_Live
import urllib


global twitter_label


def clear(threadname, delay):
    sentiment['text'] = ""
    threadname.destroy()
    delay.delete('END')
    B2.destroy()
    return


def output1(rbutton,):
    #thread.start_new_thread(clear,(thread, 200000000))
    sentiment['text'] = ""

    rbut = rbutton
    rev = t.get("1.0", 'end-1c')
    #clear(sentiment, t, B2)
    if rev != "":

        msg1, score = index_calc(rbut, rev)
        sentiment['text'] = "Review is " + msg1 + " And Score is " + str(score)
        sentiment.pack()
        #B2 = Button(master1, text="Clear", font=('helvetica', 15, 'bold'), fg='steelblue', highlightcolor='orange',
                   # command=lambda: clear(sentiment, t, B2))
        #B2.config(height=1, width=20)
        #B2.pack(side=Tkinter.RIGHT)
    else:
        error_label = Label(master1, text="", font=('arial', 10, 'bold'), fg='RED')
        error_label['text'] = "Please Enter Anything on the Text Box"
        error_label.pack()
        global B2
        B2 = Button(master1, text="Clear", font=('helvetica', 15, 'bold'), fg='steelblue', highlightcolor='orange',
                    command=lambda: clear(error_label, t))
        B2.config(height=1, width=20)
        B2.pack(side=Tkinter.RIGHT)

    return


def movie_reviews(rb):

    global rbutton
    rbutton = rb
    global master1
    master1 = Tk()
    master1.geometry('1920x1080')
    frame1 = Tkinter.Frame(master1)
    frame1.pack()
    master1.title('Sentiment Calculator')
    master1.grid()
    v = IntVar()

    heading = Label(master1, text="SENTIMENT ANALYZER !!", font=('arial', 40, 'bold'), fg='steelblue').pack()
    sub_head = Label(master1, text="\"Sentiment Analysis from Movie Reviews\"", font=('helvetica', 15, 'bold'),
                     fg='#F60').pack()

    Label(master1, text="Enter Review", fg="#F09", font=('arial', 20, 'bold'), pady=40).pack(side=Tkinter.TOP)
    global t
    t = Text(master1, height=4, width=100)
    t.pack()
    global sentiment
    sentiment = Label(master1, text="", font=('arial', 30, 'bold'), fg='steelblue')

    B1 = Button(master1, text="Proceed", font=('helvetica', 15, 'bold'), fg='steelblue', highlightcolor='orange', command=lambda: output1(rbutton))
    B1.grid(row=2, column=10)
    B1.config(height=1, width=20)
    B1.pack(side=Tkinter.LEFT)
    mainloop()
    return


def output2():
    master3 = Tk()
    master3.geometry('1920x1080')
    frame3 = Tkinter.Frame(master)
    frame3.pack()
    master3.title('Sentiment Calculator-#Twttter')
    master3.grid()
    topic = t1.get("1.0", 'end-1c')

    global twitter_label1
    twitter_label1 = Label(master3, text="", font=('arial', 15, 'bold'), fg='#009900')
    global tweet_label1
    tweet_label1 = Label(master3, text="", font=('arial', 10, 'bold'), fg='steelblue')

    global twitter_label2
    twitter_label2 = Label(master3, text="", font=('arial', 15, 'bold'), fg='#FF0033')
    global tweet_label2
    tweet_label2 = Label(master3, text="", font=('arial', 10, 'bold'), fg='steelblue')

    print ("topic in tkinter " + topic)
    posper, negper, ptweets, ntweets = Twitter_Live.main(topic)
    twitter_label1['text'] = "Positive tweets percentage:  " + posper + "%\n"
    twitter_label1.pack()
    tweet_label1['text'] = "Some of Positive Tweets\n"
    for tweet in ptweets[:10]:
        tweet_label1['text'] += tweet['text'] + "\n"
    tweet_label1.pack()
    twitter_label2['text'] = "Negative tweets percentage:  " + negper + "%\n"
    twitter_label2.pack()
    tweet_label2['text'] = "Some of Negative Tweets\n"
    for tweet in ntweets[:10]:
        tweet_label2['text'] += tweet['text'] + "\n"
    tweet_label2.pack()
    return

def twitter():
    master2 = Tk()
    master2.geometry('1920x900')
    frame2 = Tkinter.Frame(master)
    frame2.pack()
    master2.title('Sentiment Calculator')
    master2.grid()
    v = IntVar()
    try:
        urllib.urlopen('http://google.com')
    except:tkMessageBox.showinfo("READ THIS", "No Internet Connection.")
    heading = Label(master2, text="SENTIMENT ANALYZER !!", font=('arial', 40, 'bold'), fg='steelblue').pack()
    sub_head = Label(master2, text="\"Sentiment Analysis from Tweets! #Twitter\"", font=('helvetica', 15, 'bold'),
                     fg='#F60').pack()

    Label(master2, text="Enter the Topic", fg="#F09", font=('arial', 20, 'bold'), pady=40).pack(side=Tkinter.TOP)
    global t1
    t1 = Text(master2, height=4, width=100)
    t1.pack()

    Bt = Button(master2, text="Proceed", font=('helvetica', 15, 'bold'), fg='steelblue', highlightcolor='orange',
                command=lambda: output2())
    Bt.grid(row=2, column=10)
    Bt.config(height=1, width=20)
    Bt.pack(side=Tkinter.LEFT)
    a = "Enter any kind of topic like \"Donald Trump\"  \"Bajaj Platina\" ,and proceed,\n The output will be positive and negative tweets regarding the topic."
    l = Label(master2, text = a, fg="#F09", font=('courier', 10, 'bold'))
    l.pack(side = Tkinter.TOP)
    mainloop()
    return


def create_window():
    radio = sel()
    if radio is '1':
        movie_reviews(radio)
    elif radio is '2':
        twitter()
    else:
        tkMessageBox.showinfo("READ THIS", "Please Select the type of Analysis from the above list")
    return


def sel():
    return str(v.get())


master = Tk()
master.geometry('1920x1080')
frame = Tkinter.Frame(master)
frame.pack()
master.title('Sentiment Calculator')
master.grid()
v = IntVar()

heading = Label(master, text="SENTIMENT ANALYZER !!", font=('arial', 40, 'bold'), fg = 'steelblue').pack()
sub_head = Label(master, text="\"SOCIAL MEDIA MONITORING\"", font=('helvetica', 15, 'bold'), fg = '#F60').pack()

rb1 = Radiobutton(master, text="Sentiment Analysis from Movie Reviews", variable=v, value=1, font=('helvetica', 15, 'bold'), fg='#90C', pady=15).pack(anchor=W)
rb2 = Radiobutton(master, text="Sentiment analysis from tweets! #Twitter", variable=v, value=2, font=('helvetica', 15, 'bold'), fg='#90C').pack(anchor=W)


B = Tkinter.Button(master, text="Proceed", font=('helvetica', 15, 'bold'), fg='steelblue', highlightcolor='orange', command=create_window)
B.config(height=1, width=20)

B.pack(side=Tkinter.LEFT, )



b2 = Button(master, text='Quit', command=master.quit, font=('helvetica', 15, 'bold'), fg= 'steelblue', highlightcolor='orange')
b2.config(height=1, width=20)
b2.pack(side=Tkinter.RIGHT)



mainloop()
