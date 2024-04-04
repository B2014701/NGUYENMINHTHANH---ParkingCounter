import cv2
import pickle

# Kích thước của mỗi chỗ đậu xe
width, height = 107, 48

try:
    # Đọc danh sách vị trí đã lưu từ trước (nếu có)
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    # Nếu không tìm thấy tệp, tạo danh sách mới
    posList = []


def mouseClick(event, x, y):
    global posList

    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Xóa vị trí của chỗ đậu xe nếu nhấp chuột phải vào một trong chúng
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Lưu danh sách vị trí vào tệp
    with open('CarParkPos', 'wb') as p:
        pickle.dump(posList, p)


while True:
    img = cv2.imread('carParkImg.png')

    # Vẽ hình chữ nhật cho mỗi chỗ đậu xe trong danh sách vị trí
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # Hiển thị hình ảnh và gọi hàm xử lý sự kiện chuột
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    # Chờ phím nhấn từ bàn phím
    key = cv2.waitKey(1)
    if key == 27:  # 'Esc' key
        break

# Đóng cửa sổ và kết thúc chương trình
cv2.destroyAllWindows()
