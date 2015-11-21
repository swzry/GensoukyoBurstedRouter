# -*- coding: UTF-8 -*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter

bgcolor = (28, 44, 97)
forecolor = [
                    (228,0,255),(255,0,0),(0,255,255),(255,255,0),(189,75,110),
                    (75,189,88),(221,140,45),(45,165,221),(0,255,0),
                    (255,126,217),(126,255,196),(255,205,126),
                    (255,126,126),(181,126,255),(126,162,255),(232,255,126)
]
text = u"测试Example"
size = (400,400)

def create_strs(draw, font_type, font_size, width, height, fg_color, strs, ofs):
	'''绘制验证码字符'''
	'''生成给定长度的字符串，返回列表格式'''
	#c_chars = random.sample(chars, length)
	# c_chars=random.sample(rjs, length)
	# strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开
	font = ImageFont.truetype(font_type, font_size)
	font_width, font_height = font.getsize(strs)
	draw.text((10,ofs*font_height), strs, font=font, fill=fg_color)

img = Image.new('RGB', size, bgcolor)
draw = ImageDraw.Draw(img)
for i,v in enumerate(forecolor):
	create_strs(draw,"FZCQJW.ttf",16,size[0],size[1],v,text,i)
f = open("test.png","wb")
img.save(f, "PNG")
f.close()