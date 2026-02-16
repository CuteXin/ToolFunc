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
from datetime import date
import os

if not os.path.exists(log_path):
    os.makedirs(log_path)

class AutoSplitFileHandler(logging.Handler):
    """
    每次写日志时自动按日期切文件的 Handler
    """
    def __init__(self, name: str, encoding="utf-8"):
        super().__init__()
        self.base_name = name
        self.encoding  = encoding
        self.current_date = None
        self._inner_handler = None          # 真正的 FileHandler
        self._reset_if_needed()             # 初始化当天文件

    # ---------- 内部：检测日期并重建 FileHandler ----------
    def _reset_if_needed(self):
        today = date.today()
        if self.current_date == today:
            return                          # 仍是同一天，什么都不做

        # 关闭旧 handler（如果有）
        if self._inner_handler:
            self._inner_handler.close()

        # 新文件路径  name_2025-01-05.log
        new_path = os.path.join(log_path,
                                f"{self.base_name}_{today.strftime('%Y-%m-%d')}.log")
        self._inner_handler = logging.FileHandler(new_path, encoding=self.encoding)
        self._inner_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))
        self.current_date = today

    # ---------- 每次日志写入都会先走这里 ----------
    def emit(self, record):
        self._reset_if_needed()             # 自动检测+切换
        self._inner_handler.emit(record)    # 把日志写到真正的文件

class Logger:
    def log(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(AutoSplitFileHandler(name))
        return logger
