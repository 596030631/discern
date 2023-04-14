import re
import pathlib

# 二元组  Bintuple（type，value）
class Bintuple(object):
    def __init__(self, type, value):
        # Bintuple type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # Bintuple value: non-negative integer value, '+', '-', or None
        self.value = value

    def __str__(self):
        
        return 'Bintuple({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
    

# 错误处理类

# 引入头文件错误类
class HeaderfileError(Exception):
    
    def __init__(self, header_f_name):
        self.header_f_name = header_f_name

    def __str__(self):
        return "{} 头文件不存在".format(repr(self.header_f_name))

# 宏定义错误类
class DefError(Exception):
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} 字符串不是C语言标识符".format(repr(self.name))

# 引号错误类
class MarkError(Exception):
    
    def __str__(self):
        return "双引号无法匹配"
    
# 判断标识符
def is_Identifier(string_input):
    
    return True if re.fullmatch('[_a-zA-Z][_a-zA-Z0-9]*', string_input) else False

with open("./test.txt", "r", encoding='utf8') as f:
    sourse = f.read()

# C语言标准库名
stdlib = ['assert.h', 'ctype.h', 'errno.h', 'float.h', 'limits.h',
               'locale.h', 'math.h', 'setjmp.h', 'signal.h', 'stdarg.h',
               'stddef.h', 'stdio.h', 'stdlib.h', 'string.h', 'time.h']


#头文件匹配，使用正则表达式，处理“include<......>”部分
'''include_stdlib = re.compile('#include *< *(\S*)? *>|#include *"(.*?)"')
stdlib_name = include_stdlib.search(sourse)
while stdlib_name:
    stdlib_name = stdlib_name.group(1)
    region_include = include_stdlib.search(sourse).span()
    startpos_include, endpos_include = region_include
    if stdlib_name.lower() in stdlib:
        # 标准库，暂时先直接删去，不做处理
        sourse = sourse[:startpos_include] + sourse[endpos_include:]
    else:
        headerfile_path = pathlib.Path(stdlib_name)
        if headerfile_path.is_file():
            with open(headerfile_path, 'r') as f:
                sourse = sourse[:startpos_include] + f.read() + sourse[endpos_include:]
        else:
            raise HeaderfileError(stdlib_name)
    stdlib_name = include_stdlib.search(sourse)'''

# 将代码中的字符串先进行隔离,防止下面的预处理污染显式字符串
regexp = r'(?<!\\)(?:\\\\)*"'
sourse_list = re.split(regexp, sourse)
string_list = sourse_list[1::2]
code_sourse_list = sourse_list[::2]

q_mark_list = re.findall(regexp, sourse)
if len(q_mark_list) % 2:
    raise MarkError
file_sourse_no_string = ""
for i in range(len(code_sourse_list) - 1):
    file_sourse_no_string += code_sourse_list[i] + q_mark_list[2 * i] + q_mark_list[2 * i + 1]
file_sourse_no_string += code_sourse_list[-1]
print(file_sourse_no_string)


#宏定义匹配，使用正则表达式，处理“define”部分
def_re = re.compile('#define +(\S+?) +(\S+?)(?=\n)')
def_row = def_re.search(file_sourse_no_string)
while def_row:
    file_sourse_no_string = file_sourse_no_string[:def_row.span()[0]] + file_sourse_no_string[
                                                                                  def_row.span()[1]:]
    name, stuff = def_row.groups()
    if is_Identifier(name):
        file_sourse_no_string = re.sub('(?<![_a-zA-Z])' + name + '(?![_a-zA-Z0-9])', stuff, file_sourse_no_string)
    else:
        raise DefError(name)
    def_row = def_re.search(file_sourse_no_string)

# 删除注释
file_sourse_no_string = re.sub(r'/\*(?:[^*]|\*+[^/*])*\*+/|//.*?(?=\n|$)', ' ', file_sourse_no_string)

# 删除多余空白字符，并将所有空白字符换成空格
file_sourse_no_string = re.sub(r'\s+', ' ', file_sourse_no_string).strip()
print(file_sourse_no_string)

# 还原隔离的字符串
regexp = r'(?<!\\)(?:\\\\)*"'
file_sourse_no_string_list = re.split(regexp, file_sourse_no_string)
code_sourse_list = file_sourse_no_string_list[::2]
q_mark_list = re.findall(regexp, file_sourse_no_string)
sourse = ""

for i in range(len(code_sourse_list) - 1):
    sourse += code_sourse_list[i] + q_mark_list[2 * i] + string_list[i] + q_mark_list[2 * i + 1]
sourse += code_sourse_list[-1]
#print('sourse',sourse)


# 词法分析程序

reverseWord = ['auto', 'double', 'int', 'struct', 'break', 'else', 'long', 'switch',
                  'case', 'enum', 'register', 'typedef', 'char', 'extern', 'return', 'union',
                  'const', 'float', 'short', 'unsigned', 'continue', 'for', 'signed', 'void',
                  'default', 'goto', 'sizeof', 'volatile', 'do', 'if', 'while', 'static','define','include']
result = []
index = 0  # 位置索引
strToken = []
while index <= len(sourse) - 1:
    string = ""
    #print(sourse,index)
    print(sourse[index])
    if sourse[index].isspace():
        pass
    elif sourse[index]=='#':
        strToken.append(('#', "宏定义符号"))
        #print(sourse)
        if sourse[index+1:index+8] == 'include':
            Flag=0
            string +='include'
            strToken.append((string, "关键字"))
            index += 7
            #print(sourse[index])
            if sourse[index+1]=='<':
                #print('iiii')
                string=sourse[index+1]
                strToken.append((string, "界符"))
                index+=1
            if sourse[index+1:index+7] in stdlib :
                string=sourse[index+1:index+7]
                strToken.append((string, "标准库"))
                Flag=1
                index += 6
            if Flag!=1 and sourse[index+1:index+8] in stdlib :
                string=sourse[index+1:index+8]
                strToken.append((string, "标准库"))
                index += 7
            if Flag!=1 and sourse[index+1:index+9] in stdlib:
                string=sourse[index+1:index+9]
                strToken.append((string, "标准库"))
                index += 8
            if sourse[index+1]=='>':
                string=sourse[index+1]
                strToken.append((string, "界符"))
                index+=1
    elif (sourse[index].isalpha() and sourse[index].islower() )or sourse[index] == "_":
        string += sourse[index]
        index += 1
        while sourse[index].isalnum() or sourse[index] == "_":
            string += sourse[index]
            index += 1
        if string in reverseWord:
            strToken.append((string,"关键字" ))
        else:
            strToken.append((string, "标识符"))
        index -= 1
        ##
    elif sourse[index].isalpha() and sourse[index] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:

        string += sourse[index]
        index += 1
        if sourse[index].isnumeric() or sourse[index] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
                string += sourse[index]
                index += 1
                while sourse[index].isnumeric() or sourse[index] in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
                    string += sourse[index]

                    index += 1
                if sourse[index] in ['u', 'U', 'I', 'L']:
                    string += sourse[index]
                    strToken.append((string,'常量' ))
                else:
                    strToken.append((string, '常量'))
                    index-=1
        else:
            result.append(string)
            index -= 1
        ##
    elif sourse[index] == '0':
        string += sourse[index]
        index += 1
        if sourse[index] in ['x', 'X']:
            string += sourse[index]
            index += 1
            if sourse[index].isnumeric() or sourse[index] in ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']:
                string += sourse[index]
                index += 1
                while sourse[index].isnumeric() or sourse[index] in ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']:
                    string += sourse[index]
                    index += 1
                if sourse[index] in ['u', 'U', 'I', 'L']:
                    string += sourse[index]
                    strToken.append((string,'常量' ))
                else:
                    strToken.append((string, '常量'))
                    index-=1
            else:
                result.append(string)
                index -= 1
        elif sourse[index].isnumeric():
            string += sourse[index]
            index += 1
            while sourse[index].isnumeric():
                string +=_sourse[index]
                index += 1
            if sourse[index] in ['u', 'U', 'l', 'L']:
                string += sourse[index]
                strToken.append((string, '常量'))
            elif sourse[index] == '.':
                string += sourse[index]
                index += 1
                while sourse[index].isnumeric():
                    string += sourse[index]
                    index += 1
                if sourse[index] in ['e', 'E']:
                    string += sourse[index]
                    index += 1
                    if sourse[index] in ['+', '-']:
                        string += sourse[index]
                        index += 1
                        if sourse[index].isnumeric():
                            string += sourse[index]
                            index += 1
                        else:
                            result.append(string)
                            index -= 1
                        while sourse[index].isnumeric():
                            string += sourse[index]
                            index += 1
                        if sourse[index] in ['f', 'F', 'l', 'L']:
                            string += sourse[index]
                            strToken.append((string, '常量'))
                        else:
                            strToken.append((string,'常量'))
                            index -= 1
                    elif sourse[index].isnumeric():
                        string += sourse[index]
                        index += 1
                        while sourse[index].isnumeric():
                            string += sourse[index]
                            index += 1
                        if sourse[index] in ['f', 'F', 'l', 'L']:
                            string += sourse[index]
                            strToken.append((string,'常量'))
                        else:
                            strToken.append((string,'常量'))
                            index -= 1
                    else:
                        result.append(string)
                        index -= 1
                elif sourse[index] in ['f', 'F', 'l', 'L']:
                    string += sourse[index]
                    strToken.append((string,'常量'))
                else:
                    strToken.append((string,'常量'))
                    index -= 1
            else:
                strToken.append((string,'常量'))
                index -= 1
        else:
            strToken.append(('0','常量'))
            index -= 1
    elif sourse[index].isnumeric() and sourse[index] != '0':
        print("IIII")
        print(strToken)
        string += sourse[index]
        index += 1
        print(sourse[index])
        while sourse[index].isnumeric():

            string += sourse[index]
            index += 1
        if sourse[index] in ['u', 'U', 'l', 'L']:
            string += sourse[index]
            strToken.append((string,'常量'))
        ##
        elif sourse[index].isalpha():
                string += sourse[index]
                index += 1
                while sourse[index].isnumeric() or (sourse[index].isalpha() and sourse[index].isupper()):
                    string += sourse[index]
                    index += 1
                if sourse[index] in ['u', 'U', 'I', 'L']:
                    string += sourse[index]
                    strToken.append((string,'常量' ))
                else:
                    strToken.append((string, '常量'))
                    index-=1
            ##
        elif sourse[index] == '.':
            string += sourse[index]
            index += 1
            while sourse[index].isnumeric():
                string += sourse[index]
                index += 1
            if sourse[index] in ['e', 'E']:
                string += sourse[index]
                index += 1
                if sourse[index] in ['+', '-']:
                    string += sourse[index]
                    index += 1
                    if sourse[index].isnumeric():
                        string += sourse[index]
                        index += 1
                    else:
                        result.append(string)
                        index -= 1
                    while sourse[index].isnumeric():
                        string += sourse[index]
                        index += 1
                    if sourse[index] in ['f', 'F', 'l', 'L']:
                        string += sourse[index]
                        strToken.append((string,'常量'))
                    else:
                        strToken.append((string,'常量'))
                        index -= 1
                elif sourse[index].isnumeric():
                    string += sourse[index]
                    index += 1
                    while sourse[index].isnumeric():
                        string += sourse[index]
                        index += 1
                    if sourse[index] in ['f', 'F', 'l', 'L']:
                        string += sourse[index]
                        strToken.append((string,'常量'))
                    else:
                        strToken.append((string,'常量'))
                        index -= 1
                else:
                    result.append(string)
                    index -= 1
            elif sourse[index] in ['f', 'F', 'l', 'L']:
                string += sourse[index]
                strToken.append((string,'常量'))
            else:
                strToken.append((string,'常量'))
                index -= 1
        elif sourse[index].isalpha() or sourse[index] =='_':
            while sourse[index].isalpha() or sourse[index] =='_':
                string += sourse[index]
                index += 1
            result.append(string)
            index -= 1
        else:
            strToken.append((string,'常量'))
            index -= 1
    elif sourse[index] == '+':
        index += 1
        if sourse[index] == '+':
            strToken.append(('++','运算符'))
        elif sourse[index] == '=':
            strToken.append(('+=','运算符'))
        else:
            strToken.append(( '+','运算符'))
            index -= 1
    elif sourse[index] == '-':
        index += 1
        if sourse[index] == '-':
            strToken.append(( '--','运算符'))
        elif sourse[index] == '=':
            strToken.append(('-=','运算符'))
        elif sourse[index] == '>':
            strToken.append(('->','运算符'))
        else:
            strToken.append(( '-','运算符'))
            index -= 1
    elif sourse[index] == '*':
        index += 1
        if sourse[index] == '=':
            strToken.append(('*=','运算符'))
        else:
            strToken.append(( '*','运算符'))
            index -= 1
    elif sourse[index] == '/':
        index += 1
        if sourse[index] == '/':
            strToken.append(( '/=','运算符'))
        else:
            strToken.append(( '/','运算符'))
            index -= 1
    elif sourse[index] == '<':
        index += 1
        if sourse[index] == '<':
            index += 1
            if sourse[index] == '=':
                strToken.append(('<<=','运算符',))
            else:
                strToken.append(( '<<','运算符'))
                index -= 1
        elif sourse[index] == '=':
            strToken.append(( '<=','运算符'))
        else:
            strToken.append(( '<','运算符'))
    elif sourse[index] == '>':
        index += 1
        if sourse[index] == '>':
            index += 1
            if sourse[index] == '=':
                strToken.append(( '>>=','运算符'))
            else:
                strToken.append(( '>>','运算符'))
                index -= 1
        elif sourse[index] == '=':
            strToken.append(( '>=','运算符'))
        else:
            strToken.append(( '>','运算符'))
    elif sourse[index] == '&':
        index += 1
        if sourse[index] == '&':
            strToken.append(( '&&','运算符'))
        elif sourse[index] == '=':
            strToken.append(( '&=','运算符'))
        else:
            strToken.append(( '&','运算符'))
            index -= 1
    elif sourse[index] == '|':
        index += 1
        if sourse[index] == '|':
            strToken.append(( '||','运算符'))
        elif sourse[index] == '=':
            strToken.append(( '|=','运算符'))
        else:
            strToken.append(('|','运算符'))
            index -= 1
    elif sourse[index] == '%':
        index += 1
        if sourse[index] == '=':
            strToken.append(( '%=','运算符'))
        else:
            strToken.append(('%','运算符',))
            index -= 1
    elif sourse[index] == '.':
        strToken.append(( '.','运算符'))
    elif sourse[index] == '~':
        strToken.append(( '~','运算符'))
    elif sourse[index] == '^':
        index += 1
        if sourse[index] == '^':
            strToken.append(( '^=','运算符'))
        else:
            strToken.append(( '^','运算符'))
            index -= 1
    elif sourse[index] == '!':
        index += 1
        if sourse[index] == '!':
            strToken.append(( '!=','运算符'))
        else:
            strToken.append(( '!','运算符'))
            index -= 1
    elif sourse[index] == '=':
        index += 1
        if sourse[index] == '=':
            strToken.append(('==','运算符'))
        else:
            strToken.append(('=','运算符'))
            index -= 1
    elif sourse[index] == '"':
        string += sourse[index]
        index += 1
        while sourse[index] != '"':
            string += sourse[index]
            index += 1
        string += sourse[index]
        strToken.append(( string,'常量'))
    elif sourse[index] == "'":
        string += sourse[index]
        index += 1
        if sourse[index].isascii() and sourse[index] != '\\':
            string += sourse[index]
            index += 1
        elif sourse[index] == '\\':
            string += sourse[index]
            index += 1
            if sourse[index] in ['a', 'b', 'f', 't', 'v', 'o', 'n', 'r', "'", '"', '?', '\\']:
                string += sourse[index]
                index += 1
        if sourse[index] == "'":
            string += sourse[index]
            strToken.append((string,'常量'))
        else:
            while sourse[index] != "'":
                string += sourse[index]
                index += 1
            string +=_sourse[index]
            index += 1
            result.append(string)
    elif sourse[index] in ['[', ']', '(', ')', '{', '}', ',', ';']:
        strToken.append(( sourse[index],'界符'))
    else:
        result.append(sourse[index])
    index += 1
flag=1
for i in strToken:
    print(flag,i)
    flag+=1



