from flask import Flask, Response, render_template
import cv2
import faceTracker as ft
import handTracker as ht
import meshTracker as mt
import fingerCounter as fc


app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template('index.html')

#Face detection front end
@app.route("/face_detection")
def face_tracking():
    return render_template('facetracking.html')

#face detetcion module
def face_detection():
    face_tracker = ft.faceDetector()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            _ , frame = face_tracker.findFaces(frame, drawP=False)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#face detection streaming
@app.route("/faceTracking")
def faceTracking_streaming():
    return Response(face_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')

#Hand detection front end
@app.route("/hand_detection")
def hand_tracking():
    return render_template("handtracking.html")

#face detection module
def hand_detection():
    hand_tracker = ht.handTracker()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            hands = hand_tracker.findHands(frame)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#hand detection streaming
@app.route("/handtracking")
def handTracking_streaming():
    return Response(hand_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')

#Mesh Detection front end
@app.route("/mesh_detection")
def mesh_tracking():
    return render_template("meshtracking.html")

#mesh detection module
def mesh_detection():
    mesh_tracker = mt.MeshDetection()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if ret:
            _, img = mesh_tracker.findFaceMesh(frame)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#mesh detection streaming
@app.route("/meshtracking")
def meshtracking_streaming():
    return Response(mesh_detection(),mimetype='multipart/x-mixed-replace; boundary=frame')    

#finger Counter front end
@app.route("/finger_counter")
def counted_finger_tracking():
    return render_template("fingercounter.html")

#finger counting module
def finger_counting():
    hand_tracker = ht.handTracker()
    finger_counter = fc.FingerCounter()
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        cv2.rectangle(frame, (10,10), (250,30), (255,255,255), cv2.FILLED)
        cv2.putText(frame, 'Project Finger Counting', (15,25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
        if ret:
            hands = hand_tracker.findHands(frame)
            
            if hands:
                oneHand = hands[0]
                first_five = finger_counter.fingerOrientation(oneHand)

                if (len(hands) == 2):
                    secondHand = hands[1]
                    second_five = finger_counter.fingerOrientation(secondHand)
                    cv2.rectangle(frame, (10,50), (245,200), (55,245,10), cv2.FILLED)
                    cv2.putText(frame, str(first_five + second_five), (65,175), cv2.FONT_HERSHEY_COMPLEX, 4, (0,0,0), 20)
                else:
                    cv2.rectangle(frame, (40,50), (200,200), (55,245,10), cv2.FILLED)
                    cv2.putText(frame, str(first_five), (75,175), cv2.FONT_HERSHEY_COMPLEX, 4, (0,0,0), 20)
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

#counted finger streaming
@app.route("/countedfingerStreaming")
def fingerCounting_streaming():
    return Response(finger_counting(),mimetype='multipart/x-mixed-replace; boundary=frame')   
    
if __name__ == "__main__":
    app.run(debug = True)
    