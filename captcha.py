# -*- coding: UTF-8 -*-
import random,time
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from django.conf import settings

def create_validate_with_conf():
	size = settings.CAPTCHA_CONF['size']
	img_type = settings.CAPTCHA_CONF['img_type']
	mode = settings.CAPTCHA_CONF['mode']
	bg_color = settings.CAPTCHA_CONF['bg_color']
	font_size = settings.CAPTCHA_CONF['font_size']
	font_type = settings.CAPTCHA_CONF['fontType']
	TipFontType = settings.CAPTCHA_CONF['tipFontType']
	draw_lines = settings.CAPTCHA_CONF['draw_lines']
	n_line = settings.CAPTCHA_CONF['line_range']
	draw_points = settings.CAPTCHA_CONF['draw_points']
	point_chance = settings.CAPTCHA_CONF['point_chance']

# def create_validate_code(size=(300, 100),
						 # img_type="PNG",
						 # mode="RGB",
						 # bg_color=(255, 255, 255),
						 # font_size=24,
						 # font_type=fontType,
						 # TipFontType=tipFontType,
						 # length=3,
						 # draw_lines=True,
						 # n_line=(1, 3),
						 # draw_points=True,
						 # point_chance = 2):
#	 '''
#	 @todo: 生成验证码图片
#	 @param size: 图片的大小，格式（宽，高），默认为(120, 30)
#	 @param chars: 允许的字符集合，格式字符串
#	 @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
#	 @param mode: 图片模式，默认为RGB
#	 @param bg_color: 背景颜色，默认为白色
#	 @param font_size: 验证码字体大小
#	 @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
#	 @param length: 验证码字符个数
#	 @param draw_lines: 是否划干扰线
#	 @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
#	 @param draw_points: 是否画干扰点
#	 @param point_chance: 干扰点出现的概率，大小范围[0, 100]
#	 @return: [0]: PIL Image实例
#	 @return: [1]: 验证码图片中的字符串
#	 '''
	random.seed(hash(time.time()))
	width, height = size	# 宽， 高
	img = Image.new(mode, size, bg_color)	# 创建图形
	draw = ImageDraw.Draw(img)	# 创建画笔
	if draw_lines:
		create_lines(draw, n_line, width, height)
	if draw_points:
		create_points(draw, point_chance, width, height)
	ft_color = random.sample(settings.CAPTCHA_CONF['colorList'], 2)
	#text = u"请输入和这句话一样颜色的字"
	text = u"请输入和图中弧线一样颜色的字"
	realline = random.choice([True, False])
	subj = random.choice(settings.CAPTCHA_DICT['nouns'])
	obj = random.choice(settings.CAPTCHA_DICT['nouns'])
	pred = random.choice(settings.CAPTCHA_DICT['verbs'])
	rst = subj + pred + obj
	subj = random.choice(settings.CAPTCHA_DICT['nouns'])
	obj = random.choice(settings.CAPTCHA_DICT['nouns'])
	pred = random.choice(settings.CAPTCHA_DICT['verbs'])
	fst = subj + pred + obj
	if realline:
		create_strs(draw, font_type, font_size, width,height, ft_color[0], rst, 8)
		create_strs(draw, font_type, font_size, width,height, ft_color[1], fst, 2)
	else:
		create_strs(draw, font_type, font_size, width,height, ft_color[0], fst, 8)
		create_strs(draw, font_type, font_size, width,height, ft_color[1], rst, 2)
	# 图形扭曲参数
	# params = [1 - float(random.randint(1, 2)) / 100,
	# 0,
	# 0,
	# 0,
	##						1 - float(random.randint(1, 10)) / 100,
	##						float(random.randint(1, 2)) / 500,
	# 0.001,
	##						float(random.randint(1, 2)) / 500
	# ]
	params = [1 - float(random.randint(1, 2)) / 10000,
			  0,
			  0,
			  0,
			  1 - float(random.randint(1, 2)) / 10000,
			  float(random.randint(1, 2)) / 50000,
			  0.001,
			  float(random.randint(1, 2)) / 50000
			 ]
#	img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
#	img = img.filter(ImageFilter.RankFilter(size = 3, rank = 3))
#	draw = ImageDraw.Draw(img)
	# if realline:
	# 	create_tip_strs(draw, TipFontType, 14, width,height, ft_color[0], text, 1.1)
	# else:
	# 	create_tip_strs(draw, TipFontType, 14, width,height, ft_color[1], text, 1.1)
	if realline:
		create_color_arc(draw, ft_color[0], width, height)
	else:
		create_color_arc(draw, ft_color[1], width, height)
	create_tip_strs(draw, TipFontType, 14, width,height, (0,0,0), text, 1.1)
	return img, rst


def create_lines(draw, n_line, width, height):
	'''绘制干扰线'''
	line_num = random.randint(n_line[0], n_line[1])	# 干扰线条数
	for i in range(line_num):
		# 起始点
		fclr = random.choice(settings.CAPTCHA_CONF['colorList'])
		begin = (random.randint(0, width), random.randint(0, height))
		# 结束点
		end = (random.randint(0, width), random.randint(0, height))
		draw.line([begin, end], fill=fclr)

def create_color_arc(draw, color, width, height):
	'''显色弧'''
	# 起始点
	beginx,beginy = random.randint(0, width/2), random.randint(0, height/2)
	# 结束点
	#endx,endy = (beginx+random.randint(0, width-beginx)), beginy+random.randint(0, height-beginy)
	endx,endy = random.randint(width/2, width),random.randint(height/2, height-20)
	draw.arc([beginx,beginy,endx,endy],0,120,fill=color)
	draw.arc([beginx+1,beginy,endx+1,endy],0,120,fill=color)
	draw.arc([beginx-1,beginy,endx-1,endy],0,120,fill=color)
	draw.arc([beginx,beginy+1,endx,endy+1],0,120,fill=color)
	draw.arc([beginx,beginy-1,endx,endy-1],0,120,fill=color)


def create_points(draw, point_chance, width, height):
	'''绘制干扰点'''
	chance = min(100, max(0, int(point_chance)))	# 大小限制在[0, 100]

	for w in xrange(width):
		for h in xrange(height):
			tmp = random.randint(0, 100)
			fclr = random.choice(settings.CAPTCHA_CONF['colorList'])
			if tmp > 100 - chance:
				draw.point((w, h), fill=fclr)


def create_strs(draw, font_type, font_size, width, height, fg_color, strs, ofs):
	'''绘制验证码字符'''
	'''生成给定长度的字符串，返回列表格式'''
	#c_chars = random.sample(chars, length)
	# c_chars=random.sample(rjs, length)
	# strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开
	font = ImageFont.truetype(font_type, font_size)
	font_width, font_height = font.getsize(strs)
	draw.text(((width - font_width) / 3, (height - font_height) / ofs), strs, font=font, fill=fg_color)


def create_tip_strs(draw, font_type, font_size, width, height, fg_color, strs, ofs):
	'''绘制验证码字符'''
	'''生成给定长度的字符串，返回列表格式'''
	font = ImageFont.truetype(font_type, font_size)
	font_width, font_height = font.getsize(strs)
	beginx , beginy = (width - font_width) / 8, (height - font_height) / ofs
	draw.rectangle((beginx,beginy,beginx+font_width,beginy+font_height),fill=(255,255,255))
	draw.text((beginx,beginy), strs, font=font, fill=fg_color)
