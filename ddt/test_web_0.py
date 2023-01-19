# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/15 10:11
@Auth ： tj
@Function ：pytest执行用例
"""

import os
import time
import traceback

import allure
import pytest

from ddt.excel_ddt import ddt


# 报告上显示项目标题
@allure.feature('#' + str(ddt.feature_idx) + ' ' + ddt.feature)
class Test_web:
    # 用来报告上显示用例步骤调用的函数和里面的参数
    @allure.step
    def run_step(self, func, params):
        """用来在报告中显示出用例步骤所调用的函数和参数"""
        if params:
            return func(*params)
        else:
            return func()

    # 报告上显示功能模块标题
    @allure.story('#' + str(ddt.story_idx) + ' ' + ddt.story)
    @pytest.mark.parametrize('cases', ddt.cases)
    def test_case(self, cases):
        """测试用例"""
        # 报告上显示用例标题
        allure.dynamic.title(cases[0][1])
        cases = cases[1:]
        try:
            for case in cases:
                func = getattr(ddt.web, case[3])
                params = case[4:8]
                params = params[:params.index('')]
                with allure.step(case[2]):
                    res = self.run_step(func, params)
                    if res is False:
                        # 断言失败截图
                        time.sleep(2)
                        allure.attach(ddt.web.driver.get_screenshot_as_png(), '断言失败', allure.attachment_type.PNG)
                        pytest.fail("断言失败")
            # 成功后截图
            time.sleep(2)
            allure.attach(ddt.web.driver.get_screenshot_as_png(), '成功截图', allure.attachment_type.PNG)
        except Exception as e:
            # 失败后截图
            time.sleep(1)
            allure.attach(ddt.web.driver.get_screenshot_as_png(), '失败截图', allure.attachment_type.PNG)
            pytest.fail(str(traceback.format_exc()))


if __name__ == '__main__':
    os.system('rd /s/q result')
    os.system('rd /s/q report')
    pytest.main(["-s", "test_web_0.py", '--alluredir', './result'])
    os.system('allure generate result -o report --clean')
