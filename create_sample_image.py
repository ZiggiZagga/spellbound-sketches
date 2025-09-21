from PIL import Image, ImageDraw

# Create a white background image
img = Image.new('RGBA', (256, 256), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

# Draw a simple smiling face
# Head
draw.ellipse((56, 56, 200, 200), outline=(0, 0, 0), width=4, fill=(255, 255, 200, 255))
# Eyes
draw.ellipse((96, 110, 116, 130), fill=(0, 0, 0))
draw.ellipse((146, 110, 166, 130), fill=(0, 0, 0))
# Smile
draw.arc((100, 130, 160, 180), start=20, end=160, fill=(0, 0, 0), width=4)

img.save('sample_data/sample_drawing.png')
print('sample_drawing.png created!')
