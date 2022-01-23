import numpy as np
import cv2
from sklearn import datasets
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os


def get_left_and_right_edge(frame):
    print("prvi frejm")
    edges = cv2.Canny(frame, 100, 200)
    plt.imshow(edges, 'gray')
    # plt.show()

    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=10, lines=np.array([]),
                            minLineLength=385, maxLineGap=20)

    print(f"Linija izdvojeno: {len(lines)}")

    left_edge = [960, 0, 960, 0]
    right_edge = [0, 0, 0, 0]
    if lines is not None:
        for i in range(0, len(lines)):
            line = lines[i][0]
            (x1, y1), (x2, y2) = (line[0], line[1]), (line[2], line[3])
            # cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv2.LINE_AA)
            if x1 == x2:
                # print(f"x1:{x1} y1:{y2} x2:{x2} y2:{y2}")
                if x1 < left_edge[0]:
                    left_edge = [x1, y1, x2, y2]
                    # cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv2.LINE_AA)
                if x1 > right_edge[0]:
                    right_edge = [x1, y1, x2, y2]
                    # cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv2.LINE_AA)
    cv2.line(frame, (left_edge[0], left_edge[1]), (left_edge[2], left_edge[3]), (0, 0, 255), 3, cv2.LINE_AA)
    cv2.line(frame, (right_edge[0], right_edge[1]), (right_edge[2], right_edge[3]), (0, 0, 255), 3, cv2.LINE_AA)

    # print(f"DESNA: {right_edge}")
    # print(f"LEVA: {left_edge}")
    # video 4, 7 pravi problem
    plt.imshow(frame)
    # plt.show()
    return left_edge, right_edge


def get_balls(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    ret, image_bin = cv2.threshold(frame_gray, 150, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(image_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    img = frame.copy()

    countours_balls = []
    for contour in contours:
        (x, y), r = cv2.minEnclosingCircle(contour)
        # print(f"Center: {(x, y)}\t Rad: {r}")
        # if 2.5 < r < 2.51: radi za video 1
        if 4 > r > 3.5:
            # print(f"Center: {(x, y)}\t Rad: {r}")
            countours_balls.append((x, y))
    # cv2.drawContours(img, countours_balls, -1, (255, 0, 0), 1)
    # plt.imshow(img)
    # plt.show()
    # plt.imshow(image_bin, 'gray')
    # plt.show()
    return countours_balls


def check_for_contact(left_edge, right_edge, balls):
    left_edge_x = left_edge[0]
    right_edge_x = right_edge[0]
    for ball in balls:
        x = ball[0]
        if x - left_edge_x <= 20:
            # print(f"UDALJENOST OD LEVE = {x - left_edge_x}")
            return True
        if right_edge_x - x <= 20:
            # print(f"UDALJENOST OD DESNE = {right_edge_x - x}")
            return True


def process_video(video_path):

    frame_num = 0
    cap = cv2.VideoCapture(video_path)
    cap.set(1, frame_num)  # indeksiranje frejmova

    left_edge, right_edge = [], []
    hit_counter = 0
    # analiza videa frejm po frejm
    previous_hit = -1
    while True:
        frame_num += 1
        ret_val, frame = cap.read()

        # ako frejm nije zahvacen

        if not ret_val:
            break
        if frame_num == 1:  # ako je prvi frejm, detektuj levu i desnu ivicu
            left_edge, right_edge = get_left_and_right_edge(frame)
            print(f"DESNA: {right_edge}")
            print(f"LEVA: {left_edge}")
        # KUGLICE ------------
        balls = get_balls(frame)
        # print(f"\n------\nKUGLICA:{len(balls)}\n\n")

        hit = check_for_contact(left_edge, right_edge, balls)
        if hit and frame_num != previous_hit + 1 and frame_num != previous_hit + 2:
            plt.imshow(frame)
            plt.title(f"{video_path} - Frame {frame_num}")
            # plt.show()
            hit_counter += 1
            previous_hit = frame_num
    # print(f"UKUPNO DODIRA:{hit_counter}")
    return hit_counter


def reshape_data(input_data):
    # transformisemo u oblik pogodan za scikit-learn
    nsamples, nx, ny = input_data.shape
    return input_data.reshape((nsamples, nx*ny))


def get_real_count_for_video(file_name, video_name):
    file_lbl = open(file_name, "r")
    for line in file_lbl.readlines():
        tokens = line.strip().split(",")
        if tokens[0] == video_name:
            return int(tokens[1])


if __name__ == '__main__':
    print("PROJEKAT SOFT")
    print("Ucitavanje skupa")
    root_path = "data"
    dataset = []
    labels = []
    for file in os.listdir(root_path):
        filename = os.fsdecode(file)
        if filename.endswith(".mp4"):
            dataset.append(file)

    # bounces = process_video(root_path + "/video4.mp4")

    y_true = []
    y_pred = []

    for video in dataset:
        bounces = process_video(root_path + "/" + video)
        real = get_real_count_for_video(root_path + "/res.txt", video)
        # if video != "video4.mp4":
        y_true.append(real)
        y_pred.append(bounces)
        print(f"U VIDEU {video} postoji   {real}  kontakata")
        print(f"\n UDARACA: {bounces}")
        print(f"\n GRESKA: {bounces - real}")
        # wait = input()
    mae = mean_absolute_error(y_true, y_pred)
    print(f"MAE: {mae}")
