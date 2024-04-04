import cv2
import pickle

# Load video file
cap = cv2.VideoCapture('input/parking.mp4')

# Load parking positions from pickle file
with open('park_positions', 'rb') as f:
    park_positions = pickle.load(f)

# Define font for text overlay
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Parking space parameters
width, height = 40, 19
full = width * height
empty = 0.22


def parking_space_counter(img_processed):
    # Initialize parking space counter
    counter = 0

    for position in park_positions:
        x, y = position

        img_crop = img_processed[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)

        ratio = count / full

        if ratio < empty:
            color = (0, 255, 0)  # Green color for empty parking space
            counter += 1
        else:
            color = (0, 0, 255)  # Red color for occupied parking space

        cv2.rectangle(overlay, position, (position[0] + width, position[1] + height), color, -1)
        cv2.putText(overlay, "{:.2f}".format(ratio), (x + 4, y + height - 4), font, 0.7, (255, 255, 255), 1,
                    cv2.LINE_AA)

    return counter


while True:
    # Check if the video has reached its end, if yes, reset it
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Read a frame from the video
    _, frame = cap.read()
    overlay = frame.copy()

    # Preprocess the frame
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # Count parking spaces and update overlay
    counter = parking_space_counter(img_thresh)

    # Create a new frame with overlay
    alpha = 0.7
    frame_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # Draw text showing parking space count
    w, h = 220, 60
    cv2.rectangle(frame_new, (0, 0), (w, h), (255, 0, 255), -1)
    cv2.putText(frame_new, f"{counter}/{len(park_positions)}", (int(w / 10), int(h * 3 / 4)), font, 2, (255, 255, 255),
                2, cv2.LINE_AA)

    # Display the frame
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame_new)

    # Check for 'Esc' key press to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
