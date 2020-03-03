# import tkinter as tk
# from tkinter import Message, Tk


# sec_timer = 2

# top = Tk()
# top.title('Device Status')
# Message(top, text='No camera!', padx=20, pady=20).pack()
# top.after(sec_timer*1000, top.destroy)

# top.mainloop()
# top.withdraw()

import cv2

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    cv2.putText(frame, 'Status: Fall', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.imshow('',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()