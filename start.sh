#!/bin/bash

echo "================================================"
echo "Django 表格管理系统 - 快速启动脚本"
echo "================================================"

echo "1. 安装依赖包..."
pip install -r requirements.txt

echo ""
echo "2. 创建数据库迁移文件..."
python manage.py makemigrations

echo ""
echo "3. 执行数据库迁移..."
python manage.py migrate

echo ""
echo "4. 创建示例数据..."
python init_data.py

echo ""
echo "5. 测试数据同步功能..."
python manage.py test_sync

echo ""
echo "6. 启动开发服务器..."
echo "系统将在 http://127.0.0.1:8000/ 运行"
echo ""
echo "演示账号:"
echo "管理员: admin001 / admin123"
echo "普通用户: user001 / password123"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================================"

python manage.py runserver 