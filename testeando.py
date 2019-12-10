from PIL import Image

path = '/Users/andalval/Desktop/prueba datalicit/7. FONTIC FTIC-LP-03-2019/data/'
images_list = [path+'Financiero-31.png', path+'Organizacional-62.png',path+'UNSPSC-26.png',path+'UNSPSC-31.png']
imgs = [Image.open(i) for i in images_list]

# If you're using an older version of Pillow, you might have to use .size[0] instead of .width
# and later on, .size[1] instead of .height
min_img_width = min(i.width for i in imgs)

total_height = 0
for i, img in enumerate(imgs):
    # If the image is larger than the minimum width, resize it
    if img.width > min_img_width:
        imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
    total_height += imgs[i].height

# I have picked the mode of the first image to be generic. You may have other ideas
# Now that we know the total height of all of the resized images, we know the height of our final image
img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
y = 0
for img in imgs:
    img_merge.paste(img, (0, y))

    y += img.height
img_merge.save('terracegarden_v.jpg')