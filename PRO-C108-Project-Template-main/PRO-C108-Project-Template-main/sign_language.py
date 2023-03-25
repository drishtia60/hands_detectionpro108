import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands()

finger_tips =[8, 12, 16, 20]
thumb_tip= 4

while True:

    ret,image = cap.read()

    image = cv2.flip(image, 1)

    h,w,c = image.shape

    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            #accessing the landmarks by their position
            lm_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

             #Code goes here   
            for tip in finger_tips:
                x,y = int(lm_list[tip].x*w),int(lm_list[tip].y*h)
                cv2.circle(image,(x,y),15,(255,0,0),cv2.FILLED)

                finger_fold_status = []

                if lm_list[tip].x < lm_list[tip - 3].x:
                    cv2.circle(image,(x,y),15,(0,255,0),cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

            if all(finger_fold_status):
                if lm_list[thumb_tip].y < lm_list[thumb_tip-1].y < lm_list[thumb_tip-2].y:
                    print("LIKE")
                    cv2.putText(image,"LIKE",(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
                if lm_list[thumb_tip].y > lm_list[thumb_tip-1].y > lm_list[thumb_tip-2].y : 
                    print("DISLIKE")
                    cv2.putText(image,"DISLIKE",(20,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)


            mp_draw.draw_landmarks(image, hand_landmark,
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),
            mp_draw.DrawingSpec((0,255,0),4,2))

    key = cv2.waitKey(1)
    if key == 32:
        break
    

    cv2.imshow("hand tracking", image)
    