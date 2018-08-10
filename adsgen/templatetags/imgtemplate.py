from django import template
from smartad.settings import overlays,Images_Folder
import json,os
import base64
from io import BytesIO
from PIL import Image

info_json = json.load(open(overlays))
register = template.Library()

@register.simple_tag
def imagefy(**kwargs):
    imagename=kwargs['image']
    img=os.path.join(Images_Folder,imagename)
    if os.path.exists(img):
        if info_json.get(img):
            image=Image.open(img)
            buffered=BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            return 'data:image/png;base64, '+img_str.decode()
        else:
            return "!!Error! Image has not been registered!!"
    else:
        return "!!Image template does not exist!!"