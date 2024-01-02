from PIL import ImageGrab
import pytesseract

def process_selection(image, coords):
    try:
        x0, y0 = coords['start']
        x1, y1 = coords['end']
        x0, x1 = sorted([x0, x1])
        y0, y1 = sorted([y0, y1])
        cropped_image = image.crop((x0, y0, x1, y1))
        text = pytesseract.image_to_string(cropped_image)
        return text
    except Exception as e:
        print(f"Error during text extraction: {e}")
        return ""