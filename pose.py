import mediapipe as mp
import cv2

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()


def predict(img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    h, w, c = img.shape
    try:
        lm = [{"id": id, "lm": lm}
              for id, lm in enumerate(results.pose_landmarks.landmark)]

        if results.pose_landmarks and draw:
            mpDraw.draw_landmarks(img, results.pose_landmarks,
                                  mpPose.POSE_CONNECTIONS)
        return lm
    except:
        return []
