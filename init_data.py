#!/usr/bin/env python
"""
初始化数据脚本
运行此脚本可以创建示例数据
"""

import os
import django
import sys
from datetime import date, datetime

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'table_manager.settings')
django.setup()

from django.contrib.auth.models import User
from projects.models import SubProject, UserProfile


def create_sample_data():
    """创建示例数据"""
    
    print("开始创建示例数据...")
    
    # 创建示例项目数据
    sample_projects = [
        {
            'parent_id': 'P001',
            'main_project': '城市基础设施改造项目',
            'main_project_address': '北京市朝阳区建国路88号',
            'sub_project': '道路升级改造子项目',
            'main_construction_unit': '北京市政建设有限公司',
            'rectification_details': 3,
            'inspection_details': 5,
            'project_number': 'PRJ-2024-001',
            'date': date(2024, 1, 15),
            'construction_period': '6个月',
            'start_date': date(2024, 2, 1),
            'completion_date': date(2024, 7, 31),
            'address': '北京市朝阳区建国路段',
            'construction_unit': '北京市政建设有限公司',
            'contact_person': '张经理',
            'phone': '138-0000-1001',
            'contractor': '北京路桥施工集团',
            'contractor_contact': '李工程师',
            'owner': '北京市朝阳区政府',
            'area': 15000.50,
            'construction_cost': 2500000.00,
            'on_site_records': 8,
            'remarks': '该项目为重点民生工程，需严格按照时间节点完成'
        },
        {
            'parent_id': 'P002',
            'main_project': '智慧社区建设项目',
            'main_project_address': '上海市浦东新区陆家嘴金融区',
            'sub_project': '安防监控系统子项目',
            'main_construction_unit': '上海智慧科技有限公司',
            'rectification_details': 2,
            'inspection_details': 3,
            'project_number': 'PRJ-2024-002',
            'date': date(2024, 2, 20),
            'construction_period': '4个月',
            'start_date': date(2024, 3, 1),
            'completion_date': date(2024, 6, 30),
            'address': '上海市浦东新区世纪大道2000号',
            'construction_unit': '上海智慧科技有限公司',
            'contact_person': '王主任',
            'phone': '139-0000-2002',
            'contractor': '上海安防工程有限公司',
            'contractor_contact': '赵技术员',
            'owner': '浦东新区管委会',
            'area': 8500.25,
            'construction_cost': 1800000.00,
            'on_site_records': 5,
            'remarks': '需与物业管理系统对接，确保兼容性'
        },
        {
            'parent_id': 'P003',
            'main_project': '绿色环保产业园区建设',
            'main_project_address': '深圳市南山区科技园南区',
            'sub_project': '污水处理设施子项目',
            'main_construction_unit': '深圳环保建设集团',
            'rectification_details': 6,
            'inspection_details': 2,
            'project_number': 'PRJ-2024-003',
            'date': date(2024, 3, 10),
            'construction_period': '8个月',
            'start_date': date(2024, 4, 1),
            'completion_date': date(2024, 11, 30),
            'address': '深圳市南山区科技园南区环保大道',
            'construction_unit': '深圳环保建设集团',
            'contact_person': '陈总监',
            'phone': '135-0000-3003',
            'contractor': '深圳水务工程有限公司',
            'contractor_contact': '刘工',
            'owner': '深圳市环保局',
            'area': 12000.75,
            'construction_cost': 3200000.00,
            'on_site_records': 5,
            'remarks': '严格执行环保标准，定期监测水质指标'
        }
    ]
    
    # 创建项目数据
    for project_data in sample_projects:
        project, created = SubProject.objects.get_or_create(
            project_number=project_data['project_number'],
            defaults=project_data
        )
        if created:
            print(f"✓ 创建项目: {project.project_number} - {project.sub_project}")
        else:
            print(f"- 项目已存在: {project.project_number}")
    
    print(f"\n示例数据创建完成！")
    print(f"共创建 {len(sample_projects)} 个项目记录")
    print("\n您现在可以:")
    print("1. 运行 python manage.py runserver 启动服务")
    print("2. 访问 http://127.0.0.1:8000/ 查看项目")
    print("3. 使用管理员账号登录查看和编辑数据")


def create_demo_users():
    """创建演示用户"""
    print("创建演示用户...")
    
    # 创建普通用户
    regular_user, created = User.objects.get_or_create(
        username='user001',
        defaults={
            'first_name': '张',
            'last_name': '三',
            'email': 'user001@example.com',
        }
    )
    if created:
        regular_user.set_password('password123')
        regular_user.save()
        UserProfile.objects.create(user=regular_user, is_admin=False, organization='北京市政建设有限公司')
        print("✓ 创建普通用户: user001 (密码: password123, 所属单位: 北京市政建设有限公司)")
    else:
        print("- 普通用户已存在: user001")
    
    # 创建第二个普通用户
    regular_user2, created = User.objects.get_or_create(
        username='user002',
        defaults={
            'first_name': '王',
            'last_name': '五',
            'email': 'user002@example.com',
        }
    )
    if created:
        regular_user2.set_password('password123')
        regular_user2.save()
        UserProfile.objects.create(user=regular_user2, is_admin=False, organization='上海智慧科技有限公司')
        print("✓ 创建普通用户: user002 (密码: password123, 所属单位: 上海智慧科技有限公司)")
    else:
        print("- 普通用户已存在: user002")
    
    # 创建管理员用户
    admin_user, created = User.objects.get_or_create(
        username='admin001',
        defaults={
            'first_name': '李',
            'last_name': '四',
            'email': 'admin001@example.com',
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        UserProfile.objects.create(user=admin_user, is_admin=True)
        print("✓ 创建管理员用户: admin001 (密码: admin123)")
    else:
        print("- 管理员用户已存在: admin001")


if __name__ == '__main__':
    print("=" * 50)
    print("Django 表格管理系统 - 初始化数据脚本")
    print("=" * 50)
    
    create_demo_users()
    print()
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("初始化完成！")
    print("=" * 50) 