# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/14 18:07
@Auth ： tj
@Function ：统一读取excel
"""
import os
from common.Excels import NewExcel
from common.common.log import logger

def get_reader(srcfile='') -> NewExcel.Reader:
    """
    获取读取excel的对象
    :param srcfile: excel文件路径
    :return: 读取excel的对象
    """
    reader = None

    # 如果打开的文件不存在，就报错
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
        return reader

    if srcfile.endswith('.xls'):
        logger.info("excel的版本格式不对")

    if srcfile.endswith('.xlsx'):
        reader = NewExcel.Reader()
        reader.open_excel(srcfile)
        return reader
