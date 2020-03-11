# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
from time import sleep
import cv2
import termios, tty, sys #for key capture
from gpiozero import CamJamKitRobot, LED #Change this to Robot if using another motor controller

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prototxt", required=True,
    help="path to Caffe 'deploy' prototxt file")
parser.add_argument("-m", "--model", required=True,
    help="path to Caffe pre-trained model")
parser.add_argument("-c", "--confidence", type=float, default=0.2,
    help="minimum probability to filter weak detections")
parser.add_argument("-u", "--movidius", type=bool, default=0,
    help="boolean indicating if the Movidius should be used")
args = vars(parser.parse_args())

#Setup the robot, button_delay and LED variables
#If using Robot instead of CamJamKitRobot do the following:
#Let us say you are using Pins 4, 14 for the left motor and 17 and 18 for the right motor
#Then you would replace the CamJamKitRobot as such:
#robot = Robot(left=(4, 14), right=(17, 18)
devastator_robot = CamJamKitRobot()
devastator_eye = LED(25)
button_delay = 0.2

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
#Add an ignore class if you only want to detect living creatures
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
# Then the model and prototxt file are read
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# specify the target device as the Myriad processor on the NCS2
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

#Let the LED blink 4 times to start the code
for x in range(1, 5):
    devastator_eye.off()
    sleep(0.5)
    devastator_eye.on()
    sleep(0.5)

#This function captures keystrokes for robotics movement
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        #The box will have coordinates startX, startY, endX, and endY
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            #The percentage label is added and confidence is multiplied by 100 to give you the percentage
            #The rectangle is drawn using the box coordinates and colors are chosen for each class
            #Here, if startY - 15 > 15, then y = startY - 15, otherwise y = startY + 15
            #The text is added using Hershey Simplex Font
            label = "{}: {:.2f}%".format(CLASSES[idx],
                confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            
           

    
    # show the output frame
    # if the `q` key was pressed, break from the loop
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    #define the getch() function and its keys
    #The robot will stop if no key is pressed
    #this uses the WASD control scheme similar to PC controls
    char = getch()
    
    if (char == "a"):
        devastator_robot.left()
        sleep(button_delay)
    elif (char == "s"):
        devastator_robot.backward()
        sleep(button_delay)
    elif (char == "w"):
        devastator_robot.forward()
        sleep(button_delay)
    elif (char == "d"):
        devastator_robot.right()
        sleep(button_delay)
    devastator_robot.stop()
    
    

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
#close windows, stop recording, stop the robot and turn off the LED
cv2.destroyAllWindows()
vs.stop()
devastator_robot.stop()
devastator_eye.off()
