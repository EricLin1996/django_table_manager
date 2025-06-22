from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = '测试数据同步功能'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始测试数据同步...'))
        
        try:
            call_command('sync_data', '--force')
            self.stdout.write(self.style.SUCCESS('数据同步测试完成!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'数据同步测试失败: {str(e)}')) 