# Django 表格管理系统

一个基于Django的项目管理系统，用于管理子项目详细信息，支持用户权限管理和验证码登录。

## 功能特性

### 🔐 用户认证
- 用户名密码登录
- 简单字母验证码（4位大写字母）
- 用户权限分级（管理员/普通用户）
- 会话管理

### 👥 用户管理
- **管理员权限**：
  - 创建新用户
  - 设置用户权限级别
  - 查看用户列表
  - 查看和修改项目报表
- **普通用户权限**：
  - 仅可查看和修改项目报表
  - 无法创建用户

### 📊 项目管理
- 子项目详细信息表管理
- 字段分类：
  - **只读字段**：id, parent_id, 备案项目主项目, 主项目地址, 子项目, 整改完成情况明细, 巡查日期明细
  - **可修改字段**：项目编号, 日期, 工程期限, 开工日期, 竣工日期, 地址, 建设单位, 联系人, 电话, 施工单位, 施工单位联系人, 业主, 面积, 建安造价, 现场开单记录明细, 备注
- 项目搜索功能
- 分页显示
- 数据保护（用户无法增加或删除记录）

### 🎨 用户界面
- 现代化Bootstrap 5设计
- 响应式布局
- 友好的用户体验
- 中文界面

## 技术栈

- **后端**：Python 3.8+ / Django 4.2
- **数据库**：MySQL 8.0+
- **前端**：Bootstrap 5, HTML5, CSS3, JavaScript
- **其他**：Pillow (验证码生成), crispy-forms (表单美化)

## 安装部署

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd django_table_manager

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

确保MySQL服务已启动，然后创建数据库：

```sql
CREATE DATABASE table_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `table_manager/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'table_manager',
        'USER': 'your_username',        # 修改为您的MySQL用户名
        'PASSWORD': 'your_password',    # 修改为您的MySQL密码
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
```

### 3. 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户（管理员）
python manage.py createsuperuser
```

### 4. 创建用户配置文件

创建超级用户后，需要为其创建UserProfile：

```bash
python manage.py shell
```

在Shell中执行：

```python
from django.contrib.auth.models import User
from projects.models import UserProfile

# 为超级用户创建管理员配置文件
admin_user = User.objects.get(is_superuser=True)
UserProfile.objects.create(user=admin_user, is_admin=True)
```

### 5. 运行服务

```bash
python manage.py runserver
```

访问 `http://127.0.0.1:8000/` 即可使用系统。

## 使用说明

### 初次使用

1. 使用创建的超级用户账号登录
2. 进入"用户管理"创建普通用户
3. 在Django管理后台 (`/admin/`) 添加项目数据
4. 普通用户登录后可查看和编辑项目信息

### 用户操作流程

1. **登录**：输入用户名、密码和验证码
2. **查看项目**：浏览子项目详细信息列表
3. **搜索项目**：使用搜索功能快速定位项目
4. **编辑项目**：点击编辑按钮修改可编辑字段
5. **用户管理**（仅管理员）：创建和管理系统用户

## 数据模型

### SubProject (子项目详细信息表)

| 字段名 | 类型 | 说明 | 可编辑 |
|--------|------|------|---------|
| id | AutoField | 主键 | ❌ |
| parent_id | CharField | 父项目ID | ❌ |
| main_project | CharField | 备案项目主项目 | ❌ |
| main_project_address | CharField | 主项目地址 | ❌ |
| sub_project | CharField | 子项目 | ❌ |
| rectification_details | TextField | 整改完成情况明细 | ❌ |
| inspection_details | TextField | 巡查日期明细 | ❌ |
| project_number | CharField | 项目编号 | ✅ |
| date | DateField | 日期 | ✅ |
| construction_period | CharField | 工程期限 | ✅ |
| start_date | DateField | 开工日期 | ✅ |
| completion_date | DateField | 竣工日期 | ✅ |
| address | CharField | 地址 | ✅ |
| construction_unit | CharField | 建设单位 | ✅ |
| contact_person | CharField | 联系人 | ✅ |
| phone | CharField | 电话 | ✅ |
| contractor | CharField | 施工单位 | ✅ |
| contractor_contact | CharField | 施工单位联系人 | ✅ |
| owner | CharField | 业主 | ✅ |
| area | DecimalField | 面积 | ✅ |
| construction_cost | DecimalField | 建安造价 | ✅ |
| on_site_records | TextField | 现场开单记录明细 | ✅ |
| remarks | TextField | 备注 | ✅ |

### UserProfile (用户扩展信息)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| user | OneToOneField | 关联Django用户 |
| is_admin | BooleanField | 是否为管理员 |
| created_at | DateTimeField | 创建时间 |

## 数据同步功能

### 自动数据同步

系统集成了自动数据同步功能，每30分钟从supervision数据库同步最新的项目数据：

- **自动启动**：服务器启动时自动执行一次数据同步
- **定时同步**：每30分钟自动执行一次数据同步
- **增量更新**：只更新变化的数据，保留其他字段

### 同步字段映射

| supervision数据库 | table_manager数据库 | 说明 |
|------------------|---------------------|------|
| id | sub_project_id | 子项目唯一标识 |
| project_name | sub_project | 项目名称 |
| status | status | 项目状态 |
| dxmjsdw_name | main_construction_unit | 大项目建设单位 |
| problem_Nums | on_site_records | 现场开单记录明细 |
| xcd_nums | inspection_details | 巡查日期明细 |
| problem_Nums_completed | rectification_details | 整改完成情况明细 |

### 手动数据同步

管理员可以手动执行数据同步：

```bash
# 立即执行数据同步
python manage.py sync_data

# 测试数据同步功能
python manage.py test_sync
```

### 日志文件

数据同步的详细日志记录在 `logs/sync.log` 文件中，包括：
- 同步开始和结束时间
- 新增和更新的记录数量
- 错误信息和异常处理

## 安全特性

- CSRF保护
- 用户认证和授权
- 图片验证码防止自动化攻击
- 会话管理
- SQL注入防护（Django ORM）
- XSS防护（模板自动转义）
- 数据同步安全性（数据库连接加密）

## 开发说明

### 项目结构

```
django_table_manager/
├── manage.py                 # Django管理脚本
├── requirements.txt          # 项目依赖
├── README.md                # 项目说明
├── table_manager/           # 项目配置
│   ├── __init__.py
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主URL配置
│   ├── wsgi.py              # WSGI配置
│   └── asgi.py              # ASGI配置
├── projects/                # 主应用
│   ├── __init__.py
│   ├── admin.py             # 管理后台配置
│   ├── apps.py              # 应用配置
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图函数
│   ├── forms.py             # 表单定义
│   ├── urls.py              # URL路由
│   └── migrations/          # 数据库迁移
└── templates/               # 模板文件
    ├── base.html            # 基础模板
    └── projects/            # 项目模板
        ├── login.html       # 登录页面
        ├── project_list.html # 项目列表
        ├── project_detail.html # 项目详情
        ├── project_edit.html  # 项目编辑
        ├── user_list.html     # 用户列表
        └── create_user.html   # 创建用户
```

### 自定义配置

可在 `settings.py` 中修改以下配置：

- `SECRET_KEY`：生产环境请使用安全的密钥
- `DEBUG`：生产环境设为 `False`
- `ALLOWED_HOSTS`：添加允许的域名
- 数据库连接参数
- 时区和语言设置

## 常见问题

### Q: 如何重置管理员密码？
A: 使用 `python manage.py changepassword <username>` 命令

### Q: 如何备份数据？
A: 使用 `python manage.py dumpdata > backup.json` 导出数据

### Q: 验证码看不清怎么办？
A: 点击验证码图片可以刷新

### Q: 忘记密码怎么办？
A: 联系管理员重置密码或使用Django管理命令

## 许可证

MIT License

## 支持

如有问题，请提交Issue或联系开发者。 