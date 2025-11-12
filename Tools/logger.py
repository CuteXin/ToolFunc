"""
- 2025年11月12日
- 日志记录器
- 无依赖
- 使用方法
    logger = Logger().log("日志文件名字")
    logger.info("日志信息")
    logger.error("日志信息", exc_info=True)
"""
#-----日志配置-----#
log_path    = "./log/"#日志文件目录
#-----写入日志-----#
import logging
from datetime import datetime
import os

if not os.path.exists(log_path):
    os.makedirs(log_path)

class Logger():
    "打印日志"
    def log(self, name):
        # 配置日志
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # ===== 文件处理器（输出到文件，无颜色）=====
        file_handler = logging.FileHandler(f'{log_path}/{name}_{datetime.now().strftime('%Y-%m-%d')}.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 文件日志格式化器（包含线程名、文件名和行号）
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        return self.logger
