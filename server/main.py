from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from random import randint
from time import sleep
from threading import Thread, Event
import cv2
import imutils
import boundary_detection as BD

#  Flask Server Initialization
app = Flask(__name__)

# Flask app confi
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

# Adding CORS to flask App
CORS(app, resources={r"/*": {"origins": "*"}})

# Connection Socket -- Flask // and adding cors origins
socketio = SocketIO(app, cors_allowed_origins='*')

thread = Thread()
thread_stop_event = Event()


def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    # infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = randint(-5, 5)
        print(number)
        socketio.emit('newNumber', {'number': number})
        socketio.sleep(2)


# Connections Event
@socketio.on('connect')
def connection():
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        # thread = socketio.start_background_task(randomNumberGenerator)
        thread = socketio.start_background_task(playVideo)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('update')
def handleUpdate(update):
    emit('')


def playVideo():
    # Window name in which image is displayed

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initializing the HOG person
    # detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # threshold for radius search
    threshold = 30
    lockout_counter = 0

    cap = cv2.VideoCapture('walking_lowres.mp4')
    count = 0
    notFirst = False
    previous = None
    while cap.isOpened():
        # Reading the video stream
        ret, image = cap.read()
        if ret:
            image = imutils.resize(image, width=min(600, image.shape[1]))

            image = BD.draw_boundaries(image)
            # Detecting all the regions
            # in the Image that has a
            # pedestrians inside it
            (regions, _) = hog.detectMultiScale(image,
                                                winStride=(4, 4),
                                                padding=(8, 8),
                                                scale=1.05)

            # print(regions)

            # Drawing the regions in the
            # Image

            # regions = np.array([[x, y, x + w, y + h] for (x, y, w, h) in regions])
            # filtered_regions = NMS.non_max_suppression(regions, overlapThresh=0.65)
            i = 0
            person = 0
            vectors = []
            centers = []
            for x, y, w, h in regions:
                center = (x + round(w / 2), y + round(h / 2))
                if notFirst:
                    for a, b, c, d in previous:
                        oldcenter = (a + round(c / 2), b + round(d / 2))
                        vector = (center[0] - oldcenter[0], center[1] - oldcenter[1])
                        mag = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
                        if mag <= threshold:
                            # we found a point to associate!!
                            cv2.arrowedLine(image, oldcenter, (center[0] + 3 * vector[0], center[1] + 3 * vector[1]),
                                            (255, 0, 255), 1)
                            vectors.append(vector)
                            centers.append(center)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(image, center, 2, (0, 0, 255), 2)
                cv2.putText(image, 'person', (x + 10, y + 20), font, 0.5, (0, 0, 255), 1)
                person += 1
            # apply non-maxima suppression to the bounding boxes using a
            # fairly large overlap threshold to try to maintain overlapping
            # boxes that are still people

            # draw the final bounding boxes
            # for (xA, yA, xB, yB) in pick:
            # cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 255), 2)

            cv2.putText(image, 'Current Count: ' + str(count), (20, 40), font, 0.6, (255, 255, 255), 2)
            # cv2.putText(image, f'Total Persons : {person - 1}', (20, 70), font, 0.6, (255, 255, 255), 2)
            previous = regions
            notFirst = True

            if lockout_counter <= 0:
                crossing = BD.detect_crossing(centers, vectors)
                if (crossing):
                    count += crossing
                    socketio.emit('newNumber', {'number': crossing})
                    socketio.sleep(2)
                    print("Emitted: {}".format(crossing))
                    lockout_counter = 30
            lockout_counter -= 1

            # Showing the output Image
            cv2.imshow("Image", image)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    socketio.run(app)
