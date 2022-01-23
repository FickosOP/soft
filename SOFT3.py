import numpy as np
import cv2
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

import os


def get_left_and_right_edge(frame, show):
    edges = cv2.Canny(frame, 100, 200)
    plt.imshow(edges, 'gray')

    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=10, lines=np.array([]),
                            minLineLength=385, maxLineGap=20)

    left_edge = [960, 0, 960, 0]
    right_edge = [0, 0, 0, 0]

    if lines is not None:
        for i in range(0, len(lines)):
            line = lines[i][0]
            (x1, y1), (x2, y2) = (line[0], line[1]), (line[2], line[3])

            if x1 == x2:
                if x1 < left_edge[0]:
                    left_edge = [x1, y1, x2, y2]
                if x1 > right_edge[0]:
                    right_edge = [x1, y1, x2, y2]

    if show:
        cv2.line(frame, (left_edge[0], left_edge[1]), (left_edge[2], left_edge[3]), (0, 0, 255), 3, cv2.LINE_AA)
        cv2.line(frame, (right_edge[0], right_edge[1]), (right_edge[2], right_edge[3]), (0, 0, 255), 3, cv2.LINE_AA)

        plt.imshow(frame)
        plt.show()
    return left_edge, right_edge


def get_balls(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    ret, image_bin = cv2.threshold(frame_gray, 150, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(image_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    contours_balls = []
    for contour in contours:
        (x, y), r = cv2.minEnclosingCircle(contour)
        if 4 > r > 3.5:
            contours_balls.append((x, y))

    return contours_balls


def check_for_contact(left_edge, right_edge, balls):
    left_edge_x = left_edge[0]
    right_edge_x = right_edge[0]
    for ball in balls:
        x = ball[0]
        if x - left_edge_x <= 20:
            return True
        if right_edge_x - x <= 20:
            return True


def process_video(video_path):

    frame_num = 0
    cap = cv2.VideoCapture(video_path)

    left_edge, right_edge = [], []
    hit_counter = 0
    previous_hit = -1

    show_edges = input("Do you want to see plot of edges? [y/N]")
    show_hits = input("Do you want to see plot of hit frames? [y/N]")

    while True:
        frame_num += 1
        ret_val, frame = cap.read()

        if not ret_val:
            break

        if frame_num == 1:
            left_edge, right_edge = get_left_and_right_edge(frame, show_edges.lower() == 'y')

        balls = get_balls(frame)

        hit = check_for_contact(left_edge, right_edge, balls)

        if hit and frame_num > previous_hit + 2:
            if show_hits.lower() == 'y':
                plt.imshow(frame)
                plt.title(f"{video_path} - Frame {frame_num}")
                plt.show()
            hit_counter += 1
            previous_hit = frame_num

    return hit_counter


def get_real_count_for_video(file_name, video_name):
    file_lbl = open(file_name, "r")
    for line in file_lbl.readlines():
        tokens = line.strip().split(",")
        if tokens[0] == video_name:
            return int(tokens[1])


if __name__ == '__main__':
    print("PROJECT SOFT COMPUTING")
    print("Loading data...")
    root_path = "data"
    data_set = []

    for file in os.listdir(root_path):
        filename = os.fsdecode(file)
        if filename.endswith(".mp4"):
            data_set.append(file)

    print("Data loaded.")

    y_true = []
    y_predicted = []

    for video in data_set:
        bounces = process_video(root_path + "/" + video)
        real = get_real_count_for_video(root_path + "/res.txt", video)

        y_true.append(real)
        y_predicted.append(bounces)
        print(f"IN VIDEO: {video} there is {real} hits.")
        print(f"\n HITS DETECTED: {bounces}")
        print(f"\n ERROR: {bounces - real}")
        # wait = input()
    mae = mean_absolute_error(y_true, y_predicted)
    print(f"MAE: {mae}")
