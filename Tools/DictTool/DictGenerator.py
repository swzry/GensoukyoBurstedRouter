# -*- coding: UTF-8 -*-
import jieba.posseg as pseg
import json

print u"欢迎使用GensoukyoBurstedRouter验证码系统~"
print u"本工具用于词库生成，请将用于词库生成的文本放入Source.txt（例如找一篇小说之类的）"
print u"然后在custom.json内设置需要从结果中排除或额外增加的动词和名词"
print u"（友情提示：所有文件请均使用UTF-8编码！）"
print u"完成这些之后，请回车，否则请Ctrl+C终止执行。"
print u"按回车继续..."
raw_input()
print u"======================================"
print u"载入词库来源文本..."
ff=open('Source.txt','rb')
ftxt=ff.read().decode('utf-8')
ff.close()

print u"载入用户自定义配置..."
ff=open('custom.json','rb')
f=ff.read()
cstm = json.loads(f,encoding='utf-8')
ff.close()

print u"开始分词..."
nt,vt,=[],[]
jb=pseg.cut(ftxt)
for i in jb:
	if i.flag in ['n','nr','ns','nd','nh','ni','nl','ns','nz']:
		nt.append(i.word.encode('utf-8'))
	if i.flag == "v":
		vt.append(i.word.encode('utf-8'))
print u"分词完毕！"

print u"转换用户配置数据..."
ntcadd = set(cstm['nouns']['add'])
ntcdel = set(cstm['nouns']['del'])
vtcadd = set(cstm['verbs']['add'])
vtcdel = set(cstm['verbs']['del'])

print u"按照用户配置增删词条、去除重复..."
nts = set(nt)
ntu = nts | ntcadd
nto = ntu - ntcdel
ntl = list(nto)

vts = set(vt)
vtu = vts | vtcadd
vto = vtu - vtcdel
vtl = list(vto)
print u"处理完毕！正在写出文件..."

od = {u"nouns":ntl,u"verbs":vtl}
# for i in jb:
#     ot.append(i.encode('utf-8'))
oj=json.dumps(od,ensure_ascii=False,encoding='utf8')
ojhr = json.dumps(od,ensure_ascii=False,indent=4,encoding='utf8')

ff=open('captcha-dict.json','wb')
ff.write(oj.encode('utf-8'))
ff.close()
ff=open('captcha-dict-human-read.json','wb')
ff.write(ojhr.encode('utf-8'))
ff.close()
print u"恭喜！词库已生成成功~"