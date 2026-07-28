import math
import cv2
import numpy as np

class FaceFilter:
    def __init__(self) -> None:
        #Loading Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        #Creating filters
        self.current_filter = "dog"

    def create_dog_ears(self, width):
        height = int(width * 0.5)
        dog_ears = np.zeros((height, width, 4), dtype=np.uint8)

        #Drawing Left Ear
        ear_width = width//4
        pts_left = np.array([[ear_width//2, height], [ear_width, 0], [ear_width*1.5, height]], dtype=np.int32)
        cv2.fillPoly(dog_ears, [pts_left], (139, 90, 43, 255)) #Brown
        cv2.polylines(dog_ears, [pts_left], True, (100, 60, 30, 255), 3)

        #Drawing Right Ear
        pts_right = np.array([[width - ear_width//2, height], [width - ear_width, 0], [width - ear_width*1.5, height]], dtype=np.int32)
        cv2.fillPoly(dog_ears, [pts_right], (139, 90, 43, 255)) #Brown
        cv2.polylines(dog_ears, [pts_right], True, (100, 60, 30, 255), 3)

        return dog_ears
    
    def create_dog_nose(self, size):
        nose = np.zeros((size, size, 4), dtype=np.uint8)
        center = size//2

        #Drawing Nose
        cv2.ellipse(nose, (center, center), (int(size*0.4), int(size*0.3)), 0, 0, 360, (0, 0, 0, 255), -1) #Black Nose
        cv2.ellipse(nose, (int(center*0.85), int(center*0.85)), (int(size*0.1), int(size*0.1)), 0, 0, 360, (50, 50, 50, 255), -1) #White Highlight
        cv2.ellipse(nose, (int(center*0.75), center), (int(size*0.08), int(size*0.1)), 0, 0, 360, (0, 0, 0, 255), -1) #Nostrils
        cv2.ellipse(nose, (int(center*1.25), center), (int(size*0.08), int(size*0.1)), 0, 0, 360, (0, 0, 0, 255), -1)

        return nose
    
    def create_sunglasses(self, width):
        height = int(width * 0.4)
        glasses = np.zeros((height, width, 4), dtype=np.uint8)

        center_y = height // 2
        lens_width = width//3

        #Drawing Left Lens
        cv2.ellipse(glasses, (width//3, center_y), (lens_width//2, height//3), 0, 0, 360, (50, 50, 50, 220), -1)
        cv2.ellipse(glasses, (width//3, center_y), (lens_width//2, height//3), 0, 0, 360, (0, 0, 0, 255), 3)

        #Drawing Right Lens
        cv2.ellipse(glasses, (2*width//3, center_y), (lens_width//2, height//3), 0, 0, 360, (50, 50, 50, 220), -1)
        cv2.ellipse(glasses, (2*width//3, center_y), (lens_width//2, height//3), 0, 0, 360, (0, 0, 0, 255), 3)

        #Drawing Bridge
        cv2.rectangle(glasses, (width//2 - 20, center_y), (width//2 + 20, center_y), (0, 0, 0, 255), 3)

        #Adding Reflective Effect
        cv2.ellipse(glasses, (width//3 - 20, center_y - 15), (lens_width//8, height//10), 0, 0, 360, (255, 255, 255, 150), -1)
        cv2.ellipse(glasses, (2*width//3 - 20, center_y - 15), (lens_width//8, height//10), 0, 0, 360, (255, 255, 255, 150), -1)

        return glasses
    
    def create_crown(self, width):
        height = int(width * 0.6)
        crown = np.zeros((height, width, 4), dtype=np.uint8)

        #Drawing Crown Shape
        points = []
        num_points = 9
        for i in range(0, num_points):
            x = int(width * i/(num_points - 1))
            if i%2 == 0:
                y = 0
            else:
                y = height//3
            points.append((x, y))

        points.append((width, height))
        points.append((0, height))

        pts = np.array(points, dtype=np.int32)
        cv2.fillPoly(crown, [pts], (0, 215, 255, 255)) #Gold Color
        cv2.polylines(crown, [pts], True, (0, 180, 200, 255), 2)

        #Adding Jewels
        jewel_y = height//6
        for i in range(1, num_points, 2):
            x = int(width * i/(num_points - 1))
            cv2.circle(crown, (x, jewel_y), 8, (0, 0, 255, 255), -1)  # Red Jewels
            cv2.circle(crown, (x, jewel_y), 8, (0, 0, 200, 255), 2)

        return crown
    
    def create_party_hat(self, width):
        height = int(width * 0.8)
        hat = np.zeros((height, width, 4), dtype=np.uint8)

        #Triangle hat
        pts = np.array([[width//2, 0],[width//4, height],[3*width//4, height]], dtype=np.int32)
        
        cv2.fillPoly(hat, [pts], (147, 20, 255, 255))  # Green Color
        cv2.polylines(hat, [pts], True, (100, 0, 200, 255), 3)

        #Adding Dots
        for i in range(0, 5):
            y = int(height * (i + 1) / 6)
            for j in range(0, 5):
                x = width//2 + (j-i//2) * 30
                cv2.circle(hat, (x, y), 8, (255, 255, 0, 255), -1)  # Yellow Dots

        cv2.circle(hat, (width//2, 10), 15, (255, 200, 0, 255), -1) #Pom-pom

        return hat
    
    def create_cat_ears(self, width):
        height = int(width * 0.6)
        ears = np.zeros((height, width, 4), dtype=np.uint8)

        ear_size = width//4

        #Drawing Left Ear
        pts_left = np.array([[ear_size//2, height], [ear_size, 0], [ear_size*1.5, height]], dtype=np.int32)

        cv2.fillPoly(ears, [pts_left], (200, 200, 200, 255)) #Black
        cv2.polylines(ears, [pts_left], True, (150, 150, 150, 255), 2)

        #Inner Left Ear
        pts_inner_left = np.array([[ear_size*0.7, height - 20], [ear_size, 30], [ear_size*1.2, height - 20]], dtype=np.int32)
        cv2.fillPoly(ears, [pts_inner_left], (255, 192, 203, 255)) #Pink

        #Drawing Right Ear
        pts_right = np.array([[width - ear_size//2, height], [width - ear_size, 0], [width - ear_size*1.5, height]], dtype=np.int32)
        cv2.fillPoly(ears, [pts_right], (200, 200, 200, 255)) #Black
        cv2.polylines(ears, [pts_right], True, (150, 150, 150, 255), 2)

        #Inner Right Ear
        pts_inner_right = np.array([[width - ear_size*0.7, height - 20], [width - ear_size, 30], [width - ear_size*1.2, height - 20]], dtype=np.int32)
        cv2.fillPoly(ears, [pts_inner_right], (255, 192, 203, 255)) #Pink

        return ears
    
    def overlay_transparent(self, background, overlay, x, y):
        h, w = overlay.shape[:2]

        #Ensuring overlay fits within bounds
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(background.shape[1], x + w), min(background.shape[0], y + h)

        if x1 >= x2 or y1 >= y2:
            return background
        
        #Calculating overlay region
        overlay_x1 = x1 - x
        overlay_y1 = y1 - y
        overlay_x2 = overlay_x1 + (x2 - x1)
        overlay_y2 = overlay_y1 + (y2 - y1)

        #Extracting alpha channel
        alpha = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3] / 255.0
        overlay_rgb = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, :3]

        #Blending
        for c in range(3):
            background[y1:y2, x1:x2, c] = (alpha * overlay_rgb[:, :, c] + (1 - alpha) * background[y1:y2, x1:x2, c])

        return background
    
    def apply_dog_filter(self, image, face_rect):
        x, y, w, h = face_rect

        #Creating Ears
        ears = self.create_dog_ears(int(w*1.5))
        ears_h, ears_w = ears.shape[:2]
        ears_x = x - int(w*0.25)
        ears_y = y - ears_h + 20
        frame = self.overlay_transparent(image, ears, ears_x, ears_y)

        #Creating and Applying Nose
        nose_size = int(w * 0.4)
        nose = self.create_dog_nose(nose_size)
        nose_x = x + w//2 - nose_size//2
        nose_y = y + int(h*0.6)
        frame = self.overlay_transparent(frame, nose, nose_x, nose_y)

        return frame
    
    def apply_glasses_filter(self, image, face_rect):
        x, y, w, h = face_rect

        #Creating Sunglasses
        glasses = self.create_sunglasses(int(w*1.2))
        glasses_h, glasses_w = glasses.shape[:2]
        glasses_x = x - int(w*0.1)
        glasses_y = y + int(h*0.2)
        frame = self.overlay_transparent(image, glasses, glasses_x, glasses_y)

        return frame

    def apply_crown_filter(self, image, face_rect):
        x, y, w, h = face_rect

        #Creating Crown
        crown = self.create_crown(int(w*1.2))
        crown_h, crown_w = crown.shape[:2]
        crown_x = x - int(w*0.15)
        crown_y = y - crown_h + 20
        frame = self.overlay_transparent(image, crown, crown_x, crown_y)
        return frame
    
    def apply_party_hat_filter(self, image, face_rect):
        x, y, w, h = face_rect

        #Creating Party Hat
        hat = self.create_party_hat(int(w*1.2))
        hat_h, hat_w = hat.shape[:2]
        hat_x = x + w//2 - hat_w//2
        hat_y = y - hat_h + 30

        frame = self.overlay_transparent(image, hat, hat_x, hat_y)
        return frame
    
    def apply_cat_ears_filter(self, image, face_rect):
        x, y, w, h = face_rect

        #Creating Cat Ears
        ears = self.create_cat_ears(int(w*1.4))
        ears_h, ears_w = ears.shape[:2]
        ears_x = x - int(w*0.2)
        ears_y = y - ears_h + 50
        frame = self.overlay_transparent(image, ears, ears_x, ears_y)

        return frame

    def apply_filter(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            match self.current_filter:
                case "dog":
                    frame = self.apply_dog_filter(frame, (x, y, w, h))
                case "glasses":
                    frame = self.apply_glasses_filter(frame, (x, y, w, h))
                case "crown":
                    frame = self.apply_crown_filter(frame, (x, y, w, h))
                case "party_hat":
                    frame = self.apply_party_hat_filter(frame, (x, y, w, h))
                case "cat_ears":
                    frame = self.apply_cat_ears_filter(frame, (x, y, w, h))
                case _:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        return frame
    
    def run(self):
        """Run the face filter application."""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("="*50)
        print("Face Filter Application")
        print("="*50)
        print("""Available Filters:
        1 - Dog
        2 - Glasses
        3 - Crown
        4 - Party Hat
        5 - Cat Ears
        0 - No Filter (Face Detection Only)
        S - Save Screenshot
        Q - Quit Application
        """)
        print("="*50)

        filter_map = {
            ord('1'): "dog",
            ord('2'): "glasses",
            ord('3'): "crown",
            ord('4'): "party_hat",
            ord('5'): "cat_ears",
            ord('0'): None
        }
        
        screenshot_counter = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame")
                break

            # Flipping horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            #Applying filter
            filtered_frame = self.apply_filter(frame)

            #Displaying information
            info_text = f"Filter: {self.current_filter.upper().replace("_", " ")}"
            cv2.putText(filtered_frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(filtered_frame, "Press 1-5 to change filter, Q to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("Simple Face Filter", filtered_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("n/Exiting...")
                break
            elif key in filter_map:
                self.current_filter = filter_map[key]
                print(f"-> Switched to: {self.current_filter.upper().replace('_', ' ')}")
            elif key == ord("s"):
                filename = f"screenshots/screenshot_{screenshot_counter}.jpg"
                cv2.imwrite(filename, frame)
                print(f"-> Screenshot saved as {filename}")
                screenshot_counter += 1

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_filter = FaceFilter()
    face_filter.run()