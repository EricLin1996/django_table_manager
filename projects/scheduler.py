import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def sync_data_job():
    """数据同步任务"""
    try:
        logger.info("开始执行定时数据同步...")
        call_command('sync_data')
        logger.info("定时数据同步完成")
    except Exception as e:
        logger.error(f"定时数据同步失败: {str(e)}")


def start_scheduler():
    """启动定时任务调度器"""
    if not scheduler.running:
        # 添加定时任务：每30分钟执行一次
        scheduler.add_job(
            sync_data_job,
            trigger=IntervalTrigger(minutes=30),
            id='sync_data_job',
            name='数据同步任务',
            replace_existing=True,
            max_instances=1  # 确保同时只有一个任务实例运行
        )
        
        # 启动调度器
        scheduler.start()
        logger.info("数据同步定时任务已启动，每30分钟执行一次")
        
        # 立即执行一次数据同步
        try:
            logger.info("服务启动时执行初始数据同步...")
            call_command('sync_data')
            logger.info("初始数据同步完成")
        except Exception as e:
            logger.error(f"初始数据同步失败: {str(e)}")


def stop_scheduler():
    """停止定时任务调度器"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("数据同步定时任务已停止")


# 确保在Django关闭时停止调度器
import atexit
atexit.register(stop_scheduler) 