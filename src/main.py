import cv2
import tools

# PARAMETER
img_width = 480
img_height = 640
img_path = '../phieuthi.png'
ans = [0, 0, 1, 1, 3, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 3, 1, 1, 1, 2, 2, 2, 2, 1, 1, 0, 3, 1, 2, 2, 2, 1, 0,
       2, 1, 2, 1, 2, 3, 3, 1, 1, 3, 3, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 2, 3, 3, 1, 1, 3, 2, 1, 2, 2, 1, 2, 2, 1, 1,
       1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 0, 1, 3, 1, 1, 2, 1, 1, 1, 2, 3, 0, 1, 0, 0, 0, 0, 0, 3, 1, 1,
       1, 1, 1, 2, 1, 3, 3, 1, 1, 1, 1, 0]

# READ IMAGE
img = cv2.imread(img_path)

# PREPROCESSING IMAGE
img = cv2.resize(img, (img_width, img_height))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img_threshold = cv2.threshold(img_gray, 205, 255, cv2.THRESH_BINARY_INV)

# FIND CONTOURS
img_contour = img.copy()
contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img_contour, contours, -1, (0, 255, 0), 2)

# GET BOX CONTOURS
box_contour = tools.getContourBox(contours)
img_box_contour = img.copy()
cv2.drawContours(img_box_contour, box_contour, -1, (0, 255, 0), 2)
contour_ans = box_contour[: 4]
contour_ans = tools.reOrder(contour_ans)
contour_stu_code = box_contour[4]
contour_top_code = box_contour[5]

# LIST IMAGE ANSWER
list_img_ans = []
hi = []
for cnt in contour_ans:
    img_ans = tools.getImageRoi(img, cnt)
    hi.append(img_ans)
    img_ans = tools.convertThres(img_ans)
    list_img_ans.append(img_ans)

# PROCESS ANSWER
matrix_ans = tools.matrixAnswer(list_img_ans)
matrix_nonzero = tools.matrixNonZero(matrix_ans)
my_choice = tools.matrixChoice(matrix_nonzero)
grading, score = tools.grading(ans, my_choice)
img_result = tools.showAnswer(img, contour_ans, my_choice, grading)

# GET STUDENT CODE
img_stu_code = tools.getImageRoi(img, contour_stu_code)
# cv2.imwrite('img_stu_code.jpg', img_stu_code)
img_stu_code = tools.convertThres(img_stu_code)
# cv2.imwrite('img_stu_code_thres.jpg', img_stu_code)
stu_code = tools.getStudentCode(img_stu_code)

# GET TOPIC CODE
img_top_code = tools.getImageRoi(img, contour_top_code)
# cv2.imwrite('img_top_code.jpg', img_top_code)
img_top_code = tools.convertThres(img_top_code)
# cv2.imwrite('img_top_code_thres.jpg', img_top_code)
top_code = tools.getTopicCode(img_top_code)

# DISPLAY
# cv2.imwrite('img.jpg', img)
# cv2.imwrite('img_gray.jpg', img_gray)
# cv2.imwrite('img_threshold.jpg', img_threshold)
# cv2.imwrite('img_contour.jpg', img_contour)
# cv2.imwrite('img_box_contour.jpg', img_box_contour)
# cv2.imwrite('img_result.jpg', img_result)
# cv2.imwrite('img_ans[0].jpg', hi[0])
# cv2.imwrite('img_ans[1].jpg', hi[1])
# cv2.imwrite('img_ans[2].jpg', hi[2])
# cv2.imwrite('img_ans[3].jpg', hi[3])
# cv2.imwrite('list_img_ans[0].jpg', list_img_ans[0])
# cv2.imwrite('list_img_ans[1].jpg', list_img_ans[1])
# cv2.imwrite('list_img_ans[2].jpg', list_img_ans[2])
# cv2.imwrite('list_img_ans[3].jpg', list_img_ans[3])
list_img = [[img, img_gray, img_threshold, img_contour]]
display = tools.displayListImg(list_img, 0.5)
cv2.imshow('PROCESS IMAGE', display)
cv2.imshow('Image box contour', img_box_contour)
cv2.imshow('Image Result', img_result)
if cv2.waitKey() & 0xFF == ord('s'):
    tools.writeResult(my_choice, grading, score, stu_code, top_code)
    cv2.destroyAllWindows()
if cv2.waitKey():
    cv2.destroyAllWindows()

