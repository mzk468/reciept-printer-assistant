import markdown
from PIL import Image, ImageDraw, ImageFont
import io

def markdown_to_image(markdown_text, image_width=576):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_text)

    # Use a simple font
    font = ImageFont.load_default()
    
    # Create a new image with white background
    image = Image.new('RGB', (image_width, 800), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw the text
    y_position = 0
    for line in html.splitlines():
        draw.text((0, y_position), line, font=font, fill="black")
        y_position += font.getsize(line)[1] + 5
    
    # Trim the image to remove extra whitespace
    image = image.crop((0, 0, image_width, y_position))
    
    return image

# Example Markdown content
markdown_text = """
# Heading 1
## Heading 2
### Heading 3
This is some regular text in the markdown.
"""

# Convert to image
image = markdown_to_image(markdown_text)

# Save or display the image (for testing)
image.save("output.png")
# image.show()  # Uncomment to display the image

from escpos.printer import Usb

def print_image(image, printer):
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image_data = output.getvalue()
    
    # Print the image
    printer.image(io.BytesIO(image_data))
    printer.cut()

if __name__ == "__main__":
    # Replace with your printer's USB vendor_id and product_id
    p = Usb(0x04b8, 0x0202)

    # Load the image created in the previous step
    image = Image.open("output.png")
    
    # Print the image
    print_image(image, p)

    # Close the printer connection
    p.close()
