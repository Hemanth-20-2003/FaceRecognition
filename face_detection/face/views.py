from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
import threading
from django.views.decorators import gzip
import face_recognition
import pickle
from django.http import HttpResponse
import base64
import time
def cam(request):
    return render(request,'face/cam.html')

def face(request):
    try:
        c=cideo()
        return StreamingHttpResponse(live(c),
					content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        pass

class cideo(object):
    def __init__(self) -> None:
        self.video=cv2.VideoCapture(0)
        print('hi')
        self.f1 = open ("/Users/subbahemanthraju/Desktop/known.txt", "rb")
        print('hi')
        self.known = pickle.load(self.f1)
        self.f2 = open ("/Users/subbahemanthraju/Desktop/known_names.txt", "rb")
        self.known_names = pickle.load(self.f2)
        print(self.known_names)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,f=self.video.read()
        f_small=cv2.resize(f,(0,0),fx=0.25,fy=0.25)
        all=face_recognition.face_locations(f_small,model='hog',number_of_times_to_upsample=1)
        all_enc=face_recognition.face_encodings(f_small,all)
        for cur_loc,cur_enc in zip(all,all_enc):
            t,r,b,l=cur_loc
            name='unknown'
            a_m = face_recognition.compare_faces(self.known, cur_enc)
            t*=4
            r*=4
            b*=4
            l*=4
            if True in a_m:
                first_match_index = a_m.index(True)
                name = self.known_names[first_match_index]
            cv2.rectangle(f,(l,t),(r,b),(0,0,255),2)
            font=cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(f,name,(l,b),font,0.5,(255,255,255),1)
        _,jpeg=cv2.imencode('.jpg',f)
        return jpeg.tobytes()


def hm(request):
    return render(request,'face/face.html')

def live(camera):
    while(True):
        f=camera.get_frame()
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')

# Create your views here.
def add1(request):
    try:
        c=cideo1()
        return StreamingHttpResponse(live(c),
					content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        pass

class cideo1(object):
    def __init__(self) -> None:
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        print("done")
        re,f_small=self.video.read()
        face=face_recognition.face_locations(f_small,model='cnn')
        im1_enc=face_recognition.face_encodings(f_small,face)[0]
        f1 = open ("/Users/subbahemanthraju/Desktop/known.txt", "rb")
        known = pickle.load(f1)
        known.append(im1_enc)
        f1 = open ("/Users/subbahemanthraju/Desktop/known.txt", "wb")
        pickle.dump(known, f1)
        f1.close()
        self.video.release()
    def get_frame(self):
        ret,f=self.video.read()
        f_small=cv2.resize(f,(0,0),fx=0.25,fy=0.25)
        all=face_recognition.face_locations(f_small,model='hog',number_of_times_to_upsample=1)
        for cur_loc in all:
            t,r,b,l=cur_loc
            name='unknown'
            t*=4
            r*=4
            b*=4
            l*=4
            cv2.rectangle(f,(l,t),(r,b),(0,0,255),2)
        _,jpeg=cv2.imencode('.jpg',f)
        return jpeg.tobytes()

def add(request):
    if(request.method=='POST'):
        f2 = open ("/Users/subbahemanthraju/Desktop/known_names.txt", "rb")
        known_names =pickle.load(f2)
        f2 = open ("/Users/subbahemanthraju/Desktop/known_names.txt", "wb")
        k=request.POST['name']
        known_names.append(k)
        pickle.dump(known_names,f2)
        f2.close()
        return render(request,'face/res.html')
    else:
        return render(request,'face/add.html')
    
def pic1(request):
    k=cv2.VideoCapture(0)
    f1 = open ("/Users/subbahemanthraju/Desktop/known.txt", "rb")
    known = pickle.load(f1)
    f2 = open ("/Users/subbahemanthraju/Desktop/known_names.txt", "rb")
    known_names = pickle.load(f2)
    time.sleep(3)
    re,f=k.read()
    k.release()
    f_small=f
    face=face_recognition.face_locations(f_small,model='cnn',number_of_times_to_upsample=1)
    im=face_recognition.face_encodings(f_small,face)
    print('hi',face)
    ls=[]
    for i,e in zip(face,im):
        t,r,b,l=i
        a_m = face_recognition.compare_faces(known, e)
        name="unknown"
        print(name)
        print(name)
        if True in a_m:
            first_match_index = a_m.index(True)
            name = known_names[first_match_index]
            if(name not in ls):
                ls.append(name)
            print(name)
        cv2.rectangle(f,(l,t),(r,b),(0,0,255),2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(f, name, (l,b), font, 2, (255,255,255),1)

    _, buffer = cv2.imencode(".jpg", f)
    image_base64 = base64.b64encode(buffer).decode()
    context = {'img': image_base64,'l':ls}
    return render(request, 'face/result.html', context)


def pic3(request):
    try:
        c=cideo3()
        return StreamingHttpResponse(live(c),
					content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        pass

class cideo3(object):
    def __init__(self) -> None:
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,f=self.video.read()
        f_small=cv2.resize(f,(0,0),fx=0.25,fy=0.25)
        all=face_recognition.face_locations(f_small,model='hog',number_of_times_to_upsample=1)
        for cur_loc in all:
            t,r,b,l=cur_loc
            name='unknown'
            t*=4
            r*=4
            b*=4
            l*=4
            cv2.rectangle(f,(l,t),(r,b),(0,0,255),2)
        _,jpeg=cv2.imencode('.jpg',f)
        return jpeg.tobytes()

def live3(camera):
    f=camera.get_frame()
    yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')
def pic(request):
    return render(request,'face/pic.html')