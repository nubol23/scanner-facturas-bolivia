import cv2
from pyzbar import pyzbar
import numpy as np


def scale(arr):
    arr = arr - arr.min()
    arr = arr * (255/arr.max())
    return arr


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    address = "http://192.168.0.2:4747/video"
    cap.open(address)

    frame_list = []
    while True:
        ret, frame = cap.read()
        # frame = cv2.fastNlMeansDenoisingColored(frame, None, 3, 3, 7, 21)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # if len(frame_list) == 35:
        #     frame_list.pop(0)
        #
        # frame_list.append(gray)
        #
        # for f in frame_list[:-1]:
        #     gray = scale(gray + f)
        # gray = gray.astype(np.uint8)

        xc, yc = frame.shape[1]//2, frame.shape[0]//2
        pad = 80
        x1, y1, x2, y2 = xc-pad, yc-pad, xc+pad, yc+pad

        # gray = cv2.fastNlMeansDenoising(gray, None, 5+1, 7, 21)
        # gray = cv2.fastNlMeansDenoisingMulti(frame_list, 4, 5, None, 4, 7, 35)
        gray = gray[y1:y2, x1:x2]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # gray = cv2.fastNlMeansDenoising(gray, None, 5, 5, 7)[20:gray.shape[0]-20, 20:gray.shape[1]-20]
        gray = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

        # clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
        # gray = clahe.apply(gray)

        # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                              cv2.THRESH_BINARY, 23, 2)

        # gray = cv2.morphologyEx(gray, cv2.MORPH_DILATE, np.ones((3, 3)), iterations=1)

        barcodes = pyzbar.decode(gray)
        # barcodes = pyzbar.decode(frame)

        flipped = cv2.flip(frame, 1)
        for barcode in barcodes:
            # (x, y, w, h) = barcode.rect
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # cv2.putText(frame, barcodeData, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.5, (0, 0, 255), 2)
            cv2.putText(flipped, barcodeData, (0, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            print(barcodeData)
        cv2.imshow('frame', flipped)
        cv2.imshow('gray', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

