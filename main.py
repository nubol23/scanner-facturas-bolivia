import cv2
from pyzbar import pyzbar

if __name__ == '__main__':
    img = cv2.imread('/home/nubol23/Pictures/qr3.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # mask = cv2.inRange(img, (0, 0, 0), (200, 200, 200))
    # thresholded = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # img = 255 - thresholded  # black-in-white

    barcodes = pyzbar.decode(img)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # text = "{} ({})".format(barcodeData, barcodeType)
        # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
        #             0.5, (0, 0, 255), 2)

        # print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        print(barcodeData)

    cv2.imshow("Barcode Scanner", img)
    key = cv2.waitKey(0) & 0xFF

    cv2.destroyAllWindows()
