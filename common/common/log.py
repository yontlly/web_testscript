# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/15 16:03
@Auth ： tj
@Function ：曰志
"""

import logging
import os

import yaml


class Logger:
    def __init__(self, path: str = './'):
        if not os.path.isfile(path + "lib/conf.yaml"):
            path = '../'

        file = open(file=path + "lib/conf.yaml", mode='r', encoding="utf-8")
        logging_yaml = yaml.safe_load(stream=file).get('logger')
        logging_yaml['filename'] = path + logging_yaml.get('filename')
        # print(logging_yaml)
        # 配置logging日志：主要从文件中读取handler的配置、formatter（格式化日志样式）、logger记录器的配置
        logging.basicConfig(**logging_yaml)

        # 获取根记录器：配置信息从yaml文件中获取
        self.logger = logging.getLogger()

        # 创建输出到控制台的输出流
        console = logging.StreamHandler()
        # 设置日志等级
        console.setLevel(logging_yaml['level'])
        # 设置日志格式
        console.setFormatter(logging.Formatter(logging_yaml['format']))
        # 添加到logger输出
        self.logger.addHandler(console)

    def debug(self, msg: str = ''):
        self.logger.debug(msg)

    def info(self, msg: str = ''):
        self.logger.info(msg)

    def warning(self, msg: str = ''):
        self.logger.warning(msg)

    def error(self, msg: str = ''):
        self.logger.error(msg)

    def exception(self, e):
        self.logger.exception(e)


logger = Logger()

if __name__ == "__main__":
    # 等级顺序
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning('WARNING')
    logger.error('ERROR')
    try:
        int('a')
    except Exception as e:
        logger.exception(e)
