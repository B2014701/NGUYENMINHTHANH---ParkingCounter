import cv2
import pickle
from math import sqrt

# Kich thuoc cua moi cho dau xe
width, height = 40, 23

# Cac bien toan cuc de luu vi tri cua hai diem chon
pt1_x, pt1_y, pt2_x, pt2_y = None, None, None, None

try:
    # Load danh sach vi tri da duoc luu tru tu truoc (neu co)
    with open('park_positions', 'rb') as f:
        park_positions = pickle.load(f)
except FileNotFoundError:
    # Neu khong tim thay tep, tao danh sach moi
    park_positions = []


def parking_line_counter():
    # Tinh toan so luong cho dau xe dua tren khoang cach giua hai diem chon va kich thuoc cho dau xe
    global pt1_x, pt1_y, pt2_x, pt2_y
    distance = sqrt((pt2_x - pt1_x) ** 2 + (pt2_y - pt1_y) ** 2)
    line_count = int(distance / height)
    return line_count


def mouse_events(event, x, y):
    global pt1_x, pt1_y, pt2_x, pt2_y

    if event == cv2.EVENT_LBUTTONDOWN:
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        pt2_x, pt2_y = x, y
        parking_spaces = parking_line_counter()
        if parking_spaces == 0:
            park_positions.append((x, y))
        else:
            for i in range(parking_spaces):
                park_positions.append((pt1_x, pt1_y + i * height))

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Xoa vi tri cua cho dau xe neu nhan chuot phai vao mot trong chung
        for i, position in enumerate(park_positions):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                park_positions.pop(i)

    # Luu danh sach vi tri vao tep
    with open('park_positions', 'wb') as f:
        pickle.dump(park_positions, f)


while True:
    # Doc hinh anh cua bai dau xe
    img = cv2.imread('input/parking.png')

    # Ve hinh chu nhat cho moi cho dau xe trong danh sach vi tri
    for position in park_positions:
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 0, 255), 3)

    # Hien thi hinh anh va goi ham xu ly su kien chuot
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouse_events)

    # Cho phim nhan tu ban phim
    key = cv2.waitKey(30)
    if key == 27:  # 'Esc' key
        break

# Dong cua so va ket thuc chuong trinh
cv2.destroyAllWindows()
