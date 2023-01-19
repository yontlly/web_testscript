# -*- coding: utf-8 -*-
"""
@Time : 2022/12/14 16:23
@Auth : tj
@Function : 把用例读成pytest可执行的列表，通过修改文件名，复用test_web.py运行所有的用例
"""
import os

import pytest

from common.Excels.Excel import get_reader
from webtest.webkryword import Web
from common.common.log import logger

class DDT:

    def __init__(self):
        """初始化实例变量"""
        self.web = Web()
        # 记录项目的名字 和分组的名字
        self.feature = ''
        self.story = ''
        # 记录重命名的序号
        self.story_idx = 0
        # 记录项目模块的序号，用于报告排序
        self.feature_idx = 0

        # 记录一个模块的用例
        self.cases = []

    def __run_pytest_case(self):
        # 通过更改文件名，去运行数据驱动
        os.rename('./ddt/test_web_%d.py' % (self.story_idx - 1,), './ddt/test_web_%d.py' % (self.story_idx,))
        pytest.main(["-s", './ddt/test_web_%d.py' % (self.story_idx,), '--alluredir', './result'])

    def run_web_case(self, filepath='../lib/cases/test_cases.xlsx', ix=''):
        reader = get_reader(filepath)
        sheetname = reader.get_sheets()
        logger.info(sheetname)
        sheetnames = []
        try:
            t = eval(ix)
            logger.info(t)
            for i in t:
                sheetna = sheetname[i]
                sheetnames.append(sheetna)
            sheetname = sheetnames
        except:
            sheetname = sheetname
            logger.info('指定执行哪些用例的参数没有传递，将全部执行')
        finally:
            for sheet in sheetname:
                # 设置当前读取的sheet页面
                reader.set_sheet(sheet)
                # 设置项目模块名
                self.feature = sheet
                self.feature_idx += 1
                lines = reader.readline()
                case = []
                # 表头不需要
                for i in range(1, len(lines)):
                    line = lines[i]
                    # 第一格子有内容说明是用例分组名称
                    if len(line[0]) > 0:
                        # 如果模块用例不为空，说明上一个模块统计完成
                        # 把上一个用例添加到cases里面去，并且执行整个模块用例
                        if self.cases:
                            self.cases.append(case)
                            logger.info(self.cases)
                            logger.info('执行用例')
                            self.__run_pytest_case()

                        self.cases = []
                        case = []
                        # 记录用例功能模块名称
                        self.story = line[0]
                        # 加模块名的序号
                        self.story_idx += 1
                    # 第二个单元格有内容，说明是一个模块
                    elif len(line[1]) > 0:
                        # 如果case不为空，就说明上一组用例统计完成
                        # 我们把用例放到模块用例cases里面去
                        if case:
                            self.cases.append(case)
                        # 用一个列表准备存放一组用例数据
                        case = []
                        case.append(line)

                    else:
                        # 记录一组用例的数据
                        case.append(line)

                # 一个sheet统计完成，把最后一个用例添加到cases模块用例里面
                # 并且执行最后一个sheet
                if case:
                    self.cases.append(case)
                    logger.info(self.cases)
                    logger.info('执行用例')
                    self.__run_pytest_case()
                # 主要置空，否则，每一个sheet,最后一个分组可能会多次执行
                self.cases = []
                case = []

            # 所有用例跑完之后，文件名还原
            os.rename('./ddt/test_web_%d.py' % (self.story_idx,), './ddt/test_web_0.py')


ddt = DDT()
# ddt.run_web_case()

