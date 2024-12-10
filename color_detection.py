import cv2
import pandas as pd

# Load the color dataset
csv_file = "colors.csv"
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(csv_file, names=index, header=None)

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to get the color name
def getColorName(R, G, B):
    minimum = 10000
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse callback function
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Main function
if __name__ == "__main__":
    # Image path
    image_path = "colorpic.jpg"  # Replace with your image file name
    
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found. Check the file path.")
        exit()

    # Create a window and set the mouse callback
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_function)

    while True:
        # Show the image
        cv2.imshow("Image", img)
        if clicked:
            # Draw rectangle and display color name
            text = getColorName(r, g, b) + " R=" + str(r) + " G=" + str(g) + " B=" + str(b)
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            if r + g + b >= 600:
                cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            clicked = False
        
        # Exit loop with 'Esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
