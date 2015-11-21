# GensoukyoBurstedRouter

## 简介
GensoukyoBurstedRouter，中文名称 幻想乡炸裂路由器 ，是用于swzry.com的用户系统zlogin2的验证码生成器。

[项目页面&Demo](http://zlogin.swzry.com/captcha/GensoukyoBurstedRouter/)

该验证码生成器利用分词技术获得名词和动词两个词库，通过从词库内随机选择两个名词和一个动词，按照名词+动词+名词的主谓宾结构组合， 形成验证码所需的字符串。这种生成方式所生成的验证码字符串，不再枯燥，很容易随机地产生良多乐趣（←_←），让用户在输入验证码这一 让人烦躁的过程之中，偶尔也能找到一点崎岖的笑点。

关于这个项目崎岖的名称，由来就是，项目在开发过程中，测试字符串生成器的时候，出现的第一个让开发者印象深刻的随机字串。 不得不说，这个生成方式确实是很有趣啊2333333333333333 

## 使用之前
在使用之前，请先生成一个字典。
生成字典的工具在Tools/DictTool/目录内。
按如下步骤生成字典：
1. 您需要准备一篇包含大量中文词汇的文章，比如一篇小说之类的。
2. 将这篇文章放入Source.txt，保存为UTF-8编码。
3. 在custom.json内设置需要从结果中排除或额外增加的动词和名词，像这样：

    (其中nouns是名词，verbs是动词，将要手动添加的词汇放到对应的add里，要从结果中删除的词汇放入对应的del里)
```JSON
{
    "nouns":{
        "add":["博丽神社","博丽灵梦","幻想乡","琪露诺"],
        "del":["博丽神","博丽灵","琪露"]
    },
    "verbs":{
        "add":[],
        "del":["琪露"]
    }
}
```

4.执行DictGenerator.py，会生成两个文件：
    captcha-dict.json是生成的字典文件，请放到合适的目录，然后在底下的使用说明中将其路径赋予给配置文件。
    captcha-dict-human-read.json是上面那个字典文件的副本，它包含缩进，更利于人类阅读，但体积显然会更大。

## 使用说明
在部署之前，请先确保您安装了PIL（Python Imaging Library）。

该项目用于Django环境，但也可以轻易地移植用于其它的Web框架。

此处以Django中使用为例。先将captcha.py放入某个Django App，然后在Django的settings.py内加入像这样的配置：
```Python
CAPTCHA_CONF = {
    "colorList":[
                    (228,0,255),(255,0,0),(0,255,255),(255,255,0),
                    (75,189,88),(221,140,45),(45,165,221),(0,255,0),
                    (255,126,217),(126,255,196),(255,205,126),
                    (255,126,126),(181,126,255),(126,162,255),(232,255,126)
                ], #所有可用颜色列表
    "fontType":"/Path/To/Fonts/CaptchaFont.ttf", #验证码字体
    "tipFontType":"/Path/To/Fonts/TipFont.ttf", #验证码内提示性文字的字体
    "size":(300,120), #尺寸，(长,宽)
    "img_type":"PNG", 
        #图片格式（其它格式请参见PIL文档。您的PIL需已编译入相关格式的库，如果没有，请参照网上的教程，安装PIL的png支持）
    "mode":"RGB",
        #参见PIL文档
    "bg_color":(28, 44, 97), #背景颜色
    "font_size":24, #字体颜色
    "draw_lines":True, #是否绘制干扰线
    "line_range":(5,10), #干扰线数量范围
    "draw_points":True, #是否绘制干扰点
    "point_chance":5, #干扰点强度
}

with open(os.path.join(SWZRY_COMMON_DIR, 'captcha-dict.json')) as fjs:
    # captcha-dict.json为字典文件的文件名
    jsc=fjs.read()
    CAPTCHA_DICT = json.loads(jsc)

```

之后您就可以在Django中导入该模块并生成验证码了：
```Python
from django.http import HttpResponse
import StringIO
from zlogin.captcha import create_validate_with_conf
# 从您的APP中导入该模块

def MakeCaptchaImage_Test(request,randstr):
    ioStr = StringIO.StringIO()
    img,text = create_validate_with_conf()
    img.save(ioStr, "PNG")
    ot.seek(0)
    # 在这里放置用于存储验证码session的代码，验证码的内容在text变量内
    response = HttpResponse(ioStr.read(), mimetype='image/png')
    return response

```

## 关于字典生成器引用的jieba分词模块
该项目的字典生成器，其分词模块使用了基于MIT License的开源项目jieba分词
[该模块Github地址](https://github.com/fxsjy/jieba)
为了方便大家使用，所以直接把这个本来可以让大家自己pip install安一下的东西直接放进了项目里了。
由于是从Python的dist-packages目录里拷贝出来的，所以LICENSE, README.md, ChangeLog是我后来从GitHub上重新下载了放进去的。

## 关于字典生成器内的Source.txt
这个文件的内容是我写的连载小说《博丽结界之外 ~ Out of Hakurei Firewall》的部分内容。
提供这个文件只是方便测试演示，您如果需要使用该文件的内容，请遵照该小说的版权说明。
[小说项目地址](http://novel.z-touhou.org/OutOfHakureiFirewall/)
（您看见本条目时小说可能还尚未发布，却已经先放入该项目中作为Demo使用，在小说发布之前您无权转载。）
（这个文件会从半中间随机删掉部分小说内容，然后随机打乱顺序，请不要将其当小说阅读）