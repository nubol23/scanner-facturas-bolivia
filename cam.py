import cv2
from pyzbar import pyzbar
import pandas as pd
import os


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    address = "http://192.168.0.2:4747/video"
    cap.open(address)

    temp_entry = None
    columns = ["NIT Comercio", "Nro Factura", "Autorización", "Fecha", "Total1", "Total2",
               "Cod Control", "NIT Cliente", "Uknown1", "Uknown2", "Uknown3", "Uknown4"]

    if os.path.isfile('datos.csv'):
        print('Cargando')
        df = pd.read_csv('datos.csv')
    else:
        df = pd.DataFrame(columns=columns)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        barcodes = pyzbar.decode(gray)

        flipped = cv2.flip(frame, 1)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            line = barcodeData.split('|')
            entry = {
                "NIT Comercio": line[0],
                "Nro Factura": line[1],
                "Autorización": line[2],
                "Fecha": line[3],
                "Total1": line[4],
                "Total2": line[5],
                "Cod Control": line[6],
                "NIT Cliente": line[7],
                "Uknown1": line[8],
                "Uknown2": line[9],
                "Uknown3": line[10],
                "Uknown4": line[11]
            }
            if temp_entry is None or temp_entry["NIT Comercio"] != entry["NIT Comercio"]:
                temp_entry = entry
                print(temp_entry)

        cv2.imshow('frame', flipped)

        # key = cv2.waitKey(33)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('x'):
            if temp_entry is None:
                print("Error")
            else:
                print('Guardando:', temp_entry["NIT Comercio"])
                df = df.append(temp_entry, ignore_index=True)
                df.to_csv('datos.csv', index=False)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
