
import codecs
import logging
import os

import chardet


class FileHolder():
    def getFileEncodeType(filePath):
        """
        获取文件编码信息
        :param filePath:
        :return:
        """
        f = open(filePath, mode='rb')
        data = f.readline()
        f.close()
        type = chardet.detect(data)['encoding']
        if 'ascii' == type.strip():
            type = 'ascii'
        if 'ISO-8859-1' == type.strip():
            type = 'ascii'
        try:
            fn = open(filePath, encoding=type).readline()
        except UnicodeDecodeError:
            type = 'utf-8'
        print(chardet.detect(data)['encoding'] + ">" + type.strip())
        return type.strip()

    def convert(filename, out_enc="UTF-8"):
        """
        编码转换
        :param filename:
        :param out_enc:
        :return:
        """
        try:
            source_encoding = FileHolder.getFileEncodeType(filename)
            # print(source_encoding)
            if source_encoding == 'ascii':
                print(source_encoding)
                content = codecs.open(filename, 'r', encoding=source_encoding).read()

                # content = content.decode(source_encoding).encode(out_enc)
                codecs.open(filename, 'w').write(content, encoding='utf-8')
        except BaseException as e:
            logging.exception(e)

    def writefile(filename, content, in_enc="UTF-8", mode='a'):
        """
        写入文件
        :param filename:
        :param content:
        :param out_enc:
        :param mode:
        :return:
        """
        try:
            codecs.open(filename, mode, encoding=in_enc).write(content)
        except BaseException as e:
            logging.exception(e)

    def readfile(filename, out_enc="UTF-8"):
        """
        读取SQL文件内容
        :param filename:
        :param out_enc:
        :return:
        """
        try:
            return codecs.open(filename, 'r', encoding=out_enc).read()
        except BaseException as e:
            logging.exception(e)

    def explore(dir):
        """
        递归文件夹
        :param dir:
        :return:
        """
        for root, dirs, files in os.walk(dir):
            if root.endswith('DDW_CODE'):
                for file in files:
                    if os.path.splitext(file)[1] == '.sql':
                        print(file)
            else:
                print(root)

    def mkdir(path):
        """
         创建多级文件夹
        :param path:
        :return:
        """
        import os
        path = path.strip().rstrip("\\")
        if not os.path.exists(path):
            os.makedirs(path)
        return True


if __name__ == "__main__":
    FileHolder.explore('、')
