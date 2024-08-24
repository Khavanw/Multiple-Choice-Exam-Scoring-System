import cv2
import numpy as np


# DISPLAY LIST IMAGES
def displayListImg(img_array, scale, lables=[]):
    rows = len(img_array)
    cols = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank] * rows
        hor_con = [image_blank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
            hor_con[x] = np.concatenate(img_array[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        hor_con = np.concatenate(img_array)
        ver = hor
    if len(lables) != 0:
        each_img_width = int(ver.shape[1] / cols)
        each_img_height = int(ver.shape[0] / rows)
        # print(eachImgHeight)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(ver, (c * each_img_width, each_img_height * d),
                              (c * each_img_width + len(lables[d][c]) * 13 + 27, 30 + each_img_height * d),
                              (255, 255, 255),
                              cv2.FILLED)
                cv2.putText(ver, lables[d][c], (each_img_width * c + 10, each_img_height * d + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver


def getContourBox(contours):
    boxs = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        ratio = h / w
        if area > 3000 and ratio > 2:
            boxs.append(contour)
    boxs = sorted(boxs, key=lambda x: cv2.contourArea(x), reverse=True)
    return boxs


def getX(contours):
    x, y, w, h = cv2.boundingRect(contours)
    return x


def reOrder(list_box_ans):
    list_box_ans = sorted(list_box_ans, key=lambda x: getX(x))
    return list_box_ans


def getImageRoi(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    roi = img[y: y + h, x: x + w]
    return roi


def convertThres(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_thresh = cv2.threshold(img_gray, 170, 255, cv2.THRESH_BINARY_INV)
    return img_thresh


def matrixAnswer(list_img_ans):
    matrix_ans = []
    count = 1
    for img_ans in list_img_ans:
        h, w = img_ans.shape
        sec_h1 = h // 6

        for x in range(6):
            box = img_ans[x * sec_h1:(x + 1) * sec_h1, :]
            cv2.imwrite(f'../img_box/box{count}.jpg', box)
            h, w = box.shape
            offset_top = 6
            offset_bottom = 5
            offset_left = 15
            offset_right = 1
            img_box = box[offset_top:h - offset_bottom, offset_left:w - offset_right]
            cv2.imwrite(f'../img_boxcrop/boxcrop{count}.jpg', img_box)
            h, w = img_box.shape
            sec_h2 = h // 5
            count += 1
            for y in range(5):
                ques = img_box[y * sec_h2:(y + 1) * sec_h2, :]
                sec_w = w // 4

                list_ques = []
                for z in range(4):
                    ans = ques[:, z * sec_w:(z + 1) * sec_w]
                    list_ques.append(ans)
                matrix_ans.append(list_ques)
    return matrix_ans


def matrixNonZero(matrix_answers):
    my_pixel_val = np.ones((120, 4))
    for row, ques in enumerate(matrix_answers):
        for col, ans in enumerate(ques):
            total_pixels = cv2.countNonZero(ans)
            my_pixel_val[row][col] = total_pixels

    return my_pixel_val


def matrixChoice(matrix_nonzero):
    my_choice = []
    for x in matrix_nonzero:
        ans_choice = np.argmax(x)
        my_choice.append(ans_choice)
    return my_choice


def grading(ans, my_choice):
    grad = []
    for x in range(120):
        if ans[x] == my_choice[x]:
            grad.append(1)
        else:
            grad.append(0)
    score = (sum(grad) / 120) * 10
    return grad, score


def showAnswer(img, list_contour_ans, my_choice, grading):
    img_result = img.copy()
    count = 0
    for contour_ans in list_contour_ans:
        x_ans, y_ans, w_ans, h_ans = cv2.boundingRect(contour_ans)
        img_ans = img[y_ans: y_ans + h_ans, x_ans: x_ans + w_ans]
        offset_top = 6
        offset_bottom = 5
        offset_left = 15
        offset_right = 1
        offset_h = h_ans - offset_top * 6 - offset_bottom * 6
        offset_w = w_ans - offset_left - offset_right
        sec_w = offset_w // 4
        sec_h = offset_h // 30
        bux = 0
        for i in range(30):
            if (i + 1) % 5 == 1:
                bux += 6
            my_ans = my_choice[count]
            cx = (offset_left + (my_ans * sec_w) + sec_w // 2) + x_ans
            cy = (bux + (i * sec_h) + sec_h // 2) + y_ans
            if (i + 1) % 5 == 0:
                bux += 5
            if grading[count] == 1:
                my_color = (0, 255, 0)
                cv2.circle(img_result, (cx, cy), 4, my_color, cv2.FILLED)
            else:
                my_color = (0, 0, 255)
                cv2.circle(img_result, (cx, cy), 4, my_color, cv2.FILLED)
            count += 1
    return img_result


def getStudentCode(img_student_code):
    h, w = img_student_code.shape
    matrix_stu_code = np.ones((10, 6))
    sec_h = h // 10
    sec_w = w // 6
    for x in range(10):
        row = img_student_code[x * sec_h:(x + 1) * sec_h, :]
        for y in range(6):
            col = row[:, y * sec_w:(y + 1) * sec_w]
            my_pixel = cv2.countNonZero(col)
            matrix_stu_code[x][y] = my_pixel
    stu_code = np.argmax(matrix_stu_code, axis=0)

    return stu_code


def getTopicCode(img_topic_code):
    h, w = img_topic_code.shape
    matrix_stu_code = np.ones((10, 3))
    sec_h = h // 10
    sec_w = w // 3
    for x in range(10):
        row = img_topic_code[x * sec_h:(x + 1) * sec_h, :]
        for y in range(3):
            col = row[:, y * sec_w:(y + 1) * sec_w]
            my_pixel = cv2.countNonZero(col)
            matrix_stu_code[x][y] = my_pixel
    topic_code = np.argmax(matrix_stu_code, axis=0)

    return topic_code


def writeResult(my_choice, grading, score, stu_code, top_code):
    stu = ''.join(map(str, stu_code))
    top = ''.join(map(str, top_code))
    with open('../result.txt', 'wt') as file:
        file.write(f'Ma so sinh vien: {stu}\n')
        file.write(f'Ma de: {top}\n')
        file.write(f'Diem = {score}\n')
