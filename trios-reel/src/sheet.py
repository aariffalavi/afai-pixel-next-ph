import sys
from PIL import Image
fs=sys.argv[2:];ims=[Image.open(f).resize((432,768)) for f in fs]
o=Image.new('RGB',(432*len(ims),768));[o.paste(im,(i*432,0)) for i,im in enumerate(ims)];o.save(sys.argv[1])
