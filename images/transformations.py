from PIL import Image

def resize_image(image, width, height):
    return image.resize((width, height))

def crop_image(image, x, y, width, height):
    return image.crop((x, y, x + width, y + height))

def rotate_image(image, degrees):
    return image.rotate(degrees, expand=True)

def add_watermark(image, watermark_image, position):
    watermark = Image.open(watermark_image).convert("RGBA")
    image.paste(watermark, position, watermark)
    return image

def flip_image(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def mirror_image(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def compress_image(image, quality=85):
    from io import BytesIO
    output = BytesIO()
    image.save(output, format="JPEG", quality=quality)
    return output

def change_image_format(image, format):
    from io import BytesIO
    output = BytesIO()
    image.save(output, format=format)
    return output

def apply_grayscale(image):
    return image.convert("L")

def apply_sepia(image):
    width, height = image.size
    # Loads image pixel data
    pixels = image.load()  

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            # Ensure pixel values stay within 0-255
            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    return image


def apply_transformations(image, transformations):
    # Resize
    if 'resize' in transformations.keys():
        width = transformations['resize'].get('width')
        height = transformations['resize'].get('height')
        image = resize_image(image, width, height)
    
    # Crop
    if 'crop' in transformations.keys():
        x = transformations['crop'].get('x')
        y = transformations['crop'].get('y')
        width = transformations['crop'].get('width')
        height = transformations['crop'].get('height')
        image = crop_image(image, x, y, width, height)
    
    # Rotate
    if 'rotate' in transformations.keys():
        degrees = transformations['rotate']
        image = rotate_image(image, degrees)
    
    # Watermark
    if 'watermark' in transformations.keys():
        watermark_image = transformations['watermark'].get('image')
        position = transformations['watermark'].get('position', (0, 0))
        image = add_watermark(image, watermark_image, position)
    
    # Flip
    if 'flip' in transformations.keys() and transformations['flip']:
        image = flip_image(image)
    
    # Mirror
    if 'mirror' in transformations.keys() and transformations['mirror']:
        image = mirror_image(image)
    
    # Compress
    if 'compress' in transformations.keys():
        quality = transformations['compress'].get('quality', 85)
        image = compress_image(image, quality)
    
    # Change format
    if 'format' in transformations.keys():
        format = transformations['format']
        image = change_image_format(image, format)
    
    # Grayscale
    if 'filters' in transformations.keys() and transformations['filters'].get('grayscale'):
        image = apply_grayscale(image)
    
    # Sepia
    if 'filters' in transformations.keys() and transformations['filters'].get('sepia'):
        image = apply_sepia(image)

    return image
