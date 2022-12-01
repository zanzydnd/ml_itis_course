import cv2

face_cascade_db = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + 'haarcascade_frontalface_default.xml'
)  # подгружает файл в память

capture_vid = cv2.VideoCapture(0)

# img = cv2.imread("img.png")

while True:
    success, img = capture_vid.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)

    for (x, y, w, h) in faces:
        cv2.rectangle(
            img,
            (x, y),  # верхняя левая координата
            (x + w, y + h),  # нижняя правая координата
            (0, 0, 255),  # цвет прямоугольника
            2  # толщина линии
        )

    cv2.imshow("rez", img)
    cv2.waitKey()

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

capture_vid.release()
cv2.destroyAllWindows()
