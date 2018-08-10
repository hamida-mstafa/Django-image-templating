from django import template
from smartad.settings import overlays,Images_Folder,Font_location
import json,os
import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

register = template.Library()
pen=ImageFont.truetype(Font_location, 40)

@register.simple_tag
def imagefy(**kwargs):
    info_json = json.load(open(overlays))
    imagename=kwargs['image']
    img=os.path.join(Images_Folder,imagename)
    if os.path.exists(img):
        infotags=info_json.get(img)
        if infotags:
            image=Image.open(img).convert('RGBA')
            additive=Image.new('RGBA', image.size, (255, 255, 255, 0))
            drawer=ImageDraw.Draw(additive)
            for var,area in infotags.items():
                if var in kwargs:
                    text=kwargs.get(var)
                    x,y,w,h=area
                    drawer.text((x,y),text,fill="black",font=pen)
            image.alpha_composite(additive)
            buffered=BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue())
            return 'data:image/png;base64, '+img_str.decode()
        else:
            return "!!Error! Image has not been registered!!"
    else:
        return "!!Image template does not exist!!"