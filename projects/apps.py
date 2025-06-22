from django.apps import AppConfig
import os


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
    
    def ready(self):
        # 只在主进程中启动调度器，避免在Django重载时重复启动
        if os.environ.get('RUN_MAIN') != 'true':
            return
            
        try:
            from .scheduler import start_scheduler
            start_scheduler()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"启动数据同步调度器失败: {str(e)}")
    verbose_name = '项目管理' 