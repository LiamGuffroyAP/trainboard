import tkinter as tk
from datetime import datetime, timedelta
import trainboard
from functools import partial
import tts
root = tk.Tk()

class liveboard:

    def __init__(self, parent):
        #window creation
        parent.title("liveboard")
        parent.geometry("1280x720")
        departureList = []
        self.createCanvas(parent)
        self.frames()
        #list to make it easier to edit the frames
        frameList = [

        self.train1, self.train2, self.train3 ,self.train4 ,self.train5 ,self.train6 ,self.train7 ,self.train8 ,
        self.train9 ,self.train10 ,self.train11 ,self.train12 ,self.train13 ,self.train14 ,self.train15

        ]
        self.framePlace(frameList)
        self.canvas.after(1000, partial(self.refresh, frameList, departureList))

    def createCanvas(self, parent):
        #create canvas to put frames on
        self.canvas = tk.Canvas(parent, height=720, width=1280, bg="#222c36")
        self.canvas.grid(columnspan=3,rowspan=5)

    def frames(self):
        #create frames also add them to list
        self.train1 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train2 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train3 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train4 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train5 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train6 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train7 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train8 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train9 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train10 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train11 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train12 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train13 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train14 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)
        self.train15 = tk.Frame(self.canvas, bg="#2472bf", width=420, height=136)

    def framePlace(self, frameList):
        #make variables
        c = 0
        r = 0
        #for loop to place the frames in a grid
        for f in frameList:
            f.grid(column=c, row=r,  padx=4, pady=4)
            f.pack_propagate(0)
            if r < 4:
                r +=1
            elif r == 4:
                r=0
                c+=1

    def refresh(self, frameList, departureList):
        if trainboard.getList() != departureList:
            departureList = trainboard.getList() #get teh list from the api
            i = 0
            for f in frameList: #create labels from the list data and place them on the frame, do this for every frame
                for l in f.winfo_children():
                    l.destroy()
                f.pack_propagate(0)
                dest = tk.Label(f, bg="#2472bf", font=("Microsoft Sans Serif", 17), text=departureList[i]["station"], anchor="w")
                dest.place(rely=0, relx=0, relheight=0.5, relwidth=0.5)
                time = tk.Label(f, bg="#2472bf", font=("Microsoft Sans Serif", 17), text= datetime.fromtimestamp(int(departureList[i]["time"])).strftime("%H:%M"))
                time.place(rely=0, relx=0.5, relheight=0.5, relwidth=0.5)
                delayD = datetime.fromtimestamp(int(departureList[i]["delay"])).strftime("%M")
                delay = tk.Label(f, bg="#2472bf", font=("Microsoft Sans Serif", 17), text="+"+delayD, fg="red")
                if delayD != "00":
                    delay.place(rely=0, relx=0.86, relheight=0.5, relwidth=0.09)
                platform = tk.Label(f,bg="#2472bf", font=("Microsoft Sans Serif", 17), text= "platform: "+departureList[i]["platform"], anchor="w")
                if departureList[i]["canceled"] == "1":
                    platform.configure(text="CANCELED", fg="red")
                platform.place(rely=0.5, relx=0, relheight=0.5, relwidth=0.5)
                name = tk.Label(f, bg="#2472bf", font=("Microsoft Sans Serif", 17), text= departureList[i]["vehicleinfo"]["shortname"])
                name.place(rely=0.5, relx=0.5, relheight=0.5, relwidth=0.5)
                i += 1
        for index in range(10): #if the frist train has a delay and teh second train will arrive first I still want it to do this so im making it check the first 10 trains
            if timedelta(seconds=0) <= ( datetime.now()- (datetime.fromtimestamp(int(departureList[index]["time"]))+timedelta(minutes=int(datetime.fromtimestamp(int(departureList[index]["delay"])).strftime("%M") ) ) ) ) <= timedelta(seconds=11):
                #print("trein komt aan") # for debugging
                ttsText = "the "+ departureList[index]["vehicleinfo"]["type"] + " train to " + departureList[index]["station"] + " will be leaving at platform " + departureList[index]["platform"]
                print(ttsText) #for debugging but leaving it here
                tts.TTS(ttsText)
            #else:
                #print(index, datetime.fromtimestamp(int(departureList[index]["time"])), datetime.now()) #was for debugging

        self.canvas.after(10000, partial(self.refresh, frameList, departureList))
        return(departureList)

l = liveboard(root)
root.mainloop()
