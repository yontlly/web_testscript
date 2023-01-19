# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/14 18:05
@Auth ： tj
@Function ：xlsx格式excel文件读取
"""
import os, openpyxl


class Reader:
    """
        用来读取Excel文件内容
        只支持xlsx格式excel文件读取
        pip install -U openpyxl
    """

    def __init__(self):
        # 整个excel工作簿缓存
        self.workbook = None
        # 当前工作sheet
        self.sheet = None
        # 当前sheet的行数
        self.rows = 0
        # 当前读取到的行数
        self.r = 0

    # 打开excel
    def open_excel(self, srcfile):
        if not os.path.isfile(srcfile):
            print("%s not exist!" % (srcfile))
            return

        openpyxl.Workbook.encoding = "utf8"
        self.workbook = openpyxl.load_workbook(filename=srcfile)
        self.sheet = self.workbook[self.workbook.sheetnames[0]]
        self.rows = self.sheet.max_row
        self.r = 0
        return

    # 获取sheet页面
    def get_sheets(self):
        sheets = self.workbook.sheetnames
        # print(sheets)
        return sheets

    # 切换sheet页面
    def set_sheet(self, name):
        # 通过sheet名字，切换sheet页面
        self.sheet = self.workbook[name]
        self.rows = self.sheet.max_row
        self.r = 0
        return

    # 逐行读取
    def readline(self):
        lines = []
        for row in self.sheet.rows:
            line = []
            for cell in row:
                if cell.value is None:
                    line.append('')
                else:
                    line.append(cell.value)

            lines.append(line)

        return lines
