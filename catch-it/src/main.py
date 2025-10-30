import cv2 as cv
from ultralytics import YOLO

def main():
    model = YOLO("./models/yolov8n.pt")
    cam = cv.VideoCapture(0)
    
    if not cam.isOpened():
        print("Cannot open camera")
        return

    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    score = 0
    while True:
        ret, frame = cam.read()
        target_box = (frame_width//3, frame_height//3, frame_width//3, frame_height//3)
        x, y, w, h = target_box
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break
    
        results = model(frame)[0]
        
        
        for box in results.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2)//2, (y1 + y2)//2
        
            if x <= cx <= x + w and y <= cy <= y + h:
                score += 1
        
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.putText(frame, f"Score: {score}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv.imshow("Catch It! Game", frame)

                
        if cv.waitKey(1) == ord("q"):
            break
    
    cam.release()
    cv.destroyAllWindows()    


if __name__ == "__main__":
    main()
    