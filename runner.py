# -*- coding: utf-8 -*-
"""
@Time : 2022/12/15 13:44
@Auth : tj
@Function :数据驱动运行入口
"""
import os

from ddt.excel_ddt import ddt

if __name__ == '__main__':
    # 删除之前的报告文件
    os.system('rd /s/q result')
    # 删除之前生成的报告
    os.system('rd /s/q report')
    # 用ddt读取用例
    ddt.run_web_case('./lib/cases/test_cases.xlsx', '[0, 1]')

    # ddt.run_web_case('./lib/cases/test_cases.xlsx')
    # 执行用例并生成报告
    os.system('allure generate result -o report --clean')
