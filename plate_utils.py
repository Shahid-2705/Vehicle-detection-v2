import cv2
import pytesseract
from datetime import datetime
import os

# Path to Tesseract executable (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_plate_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blur, 30, 200)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    plate_img = None
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.018 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            plate_img = image[y:y+h, x:x+w]
            break

    if plate_img is not None:
        plate_text = pytesseract.image_to_string(plate_img, config='--psm 8').strip()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        save_path = os.path.join("logs", f"plate_{timestamp}.jpg")

        # Draw timestamp and plate number
        cv2.putText(plate_img, timestamp, (10, plate_img.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(plate_img, f"Plate: {plate_text}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Save image
        cv2.imwrite(save_path, plate_img)

        # Save to CSV log
        with open("logs/plate_logs.csv", "a") as f:
            f.write(f"{plate_text},{timestamp},{save_path}\n")

        return plate_text, save_path

    return None, None
