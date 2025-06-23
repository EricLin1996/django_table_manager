from django.core.management.base import BaseCommand
from django.db import connections
from django.utils import timezone
from projects.models import SubProject
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '从supervision数据库同步项目数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='强制执行同步，忽略时间限制',
        )

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS(f'开始数据同步... {timezone.now()}'))
            
            # 获取supervision数据库连接
            supervision_conn = connections['supervision']
            
            # 执行复杂SQL查询
            sql_query = """
            with t1_mxm as (
                select id,parent_id,project_name as zxm_mc
                from t_project_info where project_type = '1' and parent_id = '0'
            ),t2_sxm as (
                select id,parent_id,project_name,project_flag as status
                from t_project_info where parent_id in (
                select id from t_project_info where project_type = '1' and parent_id = '0'
                )
            ),t3_dxmjsdw as (
                select t1.project_id,t1.company_id,t2.name from (select distinct project_id, company_id
                           from t_project_user
                           where project_id in (select id
                                                from t_project_info
                                                where project_type = '1' and parent_id = '0'))
                as t1 join (select id, name
                            from t_company
                            where type = '0') as t2 on t1.company_id = t2.id
            ),t4_zgdsl as (
            select project_id,count(1) as 'problem_Nums' from t_project_problem where parent_project_id in (
                select id from t_project_info where project_type = '1' and parent_id = '0'
                )
            group by project_id
            ),t5_xcdsl as (
                select project_id,count(1) as 'xcd_nums' from t_project_work_log where parent_project_id in (
                select id from t_project_info where project_type = '1' and parent_id = '0'
                )
            group by project_id
            )
            select t2_sxm.id,t2_sxm.project_name,t2_sxm.status,t3_dxmjsdw.name as `dxmjsdw_name`,
                   t4_zgdsl.problem_Nums,t5_xcdsl.xcd_nums,t4_zgdsl.problem_Nums as `problem_Nums_completed`
            from t2_sxm join t1_mxm on t2_sxm.parent_id = t1_mxm.id
            join t3_dxmjsdw on t2_sxm.parent_id = t3_dxmjsdw.project_id
            left join t4_zgdsl on t2_sxm.id = t4_zgdsl.project_id
            left join t5_xcdsl on t2_sxm.id = t5_xcdsl.project_id
            """
            
            with supervision_conn.cursor() as cursor:
                cursor.execute(sql_query)
                results = cursor.fetchall()
                
                # 获取列名
                columns = [col[0] for col in cursor.description]
                
                self.stdout.write(f'从supervision数据库获取到 {len(results)} 条记录')
                
                # 处理查询结果
                updated_count = 0
                created_count = 0
                
                for row in results:
                    data = dict(zip(columns, row))
                    
                    # 映射字段
                    sub_project_id = str(data['id'])
                    sub_project_name = data['project_name']
                    status = str(data['status']) if data['status'] is not None else None
                    main_construction_unit = data['dxmjsdw_name']
                    on_site_records = data['problem_Nums']
                    inspection_details = data['xcd_nums']
                    rectification_details = data['problem_Nums_completed']
                    
                    try:
                        # 尝试获取已存在的记录
                        subproject, created = SubProject.objects.get_or_create(
                            sub_project_id=sub_project_id,
                            defaults={
                                'sub_project': sub_project_name,
                                'status': status,
                                'main_construction_unit': main_construction_unit,
                                'on_site_records': on_site_records,
                                'inspection_details': inspection_details,
                                'rectification_details': rectification_details,
                            }
                        )
                        
                        if created:
                            created_count += 1
                            self.stdout.write(f'创建新记录: {sub_project_name} (ID: {sub_project_id})')
                        else:
                            # 更新已存在的记录
                            update_fields = []
                            
                            if subproject.sub_project != sub_project_name:
                                subproject.sub_project = sub_project_name
                                update_fields.append('sub_project')
                            
                            if subproject.status != status:
                                subproject.status = status
                                update_fields.append('status')
                            
                            if subproject.main_construction_unit != main_construction_unit:
                                subproject.main_construction_unit = main_construction_unit
                                update_fields.append('main_construction_unit')
                            
                            if subproject.on_site_records != on_site_records:
                                subproject.on_site_records = on_site_records
                                update_fields.append('on_site_records')
                            
                            if subproject.inspection_details != inspection_details:
                                subproject.inspection_details = inspection_details
                                update_fields.append('inspection_details')
                            
                            if subproject.rectification_details != rectification_details:
                                subproject.rectification_details = rectification_details
                                update_fields.append('rectification_details')
                            
                            if update_fields:
                                update_fields.append('updated_at')  # 更新时间戳
                                subproject.save(update_fields=update_fields)
                                updated_count += 1
                                self.stdout.write(f'更新记录: {sub_project_name} (ID: {sub_project_id}) - 字段: {", ".join(update_fields)}')
                    
                    except Exception as e:
                        self.stderr.write(f'处理记录失败 (ID: {sub_project_id}): {str(e)}')
                        logger.error(f'数据同步错误 - ID: {sub_project_id}, 错误: {str(e)}')
                        continue
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'数据同步完成! 创建: {created_count} 条, 更新: {updated_count} 条, 总计: {len(results)} 条'
                    )
                )
                
        except Exception as e:
            error_msg = f'数据同步失败: {str(e)}'
            self.stderr.write(self.style.ERROR(error_msg))
            logger.error(f'数据同步失败: {str(e)}')
            raise 