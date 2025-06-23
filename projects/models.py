from django.db import models
from django.contrib.auth.models import User


class SubProject(models.Model):
    """子项目详细信息表"""
    
    # 只读字段
    parent_id = models.CharField(max_length=100, verbose_name="父项目ID", blank=True, null=True)
    main_project = models.CharField(max_length=200, verbose_name="备案项目主项目", blank=True, null=True)
    main_project_address = models.CharField(max_length=300, verbose_name="主项目地址", blank=True, null=True)
    sub_project = models.CharField(max_length=200, verbose_name="名称", blank=True, null=True)
    status = models.CharField(max_length=10, verbose_name="项目状态", blank=True, null=True)
    sub_project_id = models.CharField(max_length=100, verbose_name="子项目ID", unique=True, blank=True, null=True)
    main_construction_unit = models.CharField(max_length=200, verbose_name="大项目建设单位", blank=True, null=True)
    inspection_details = models.IntegerField(verbose_name="巡查日期明细（共几次）", blank=True, null=True)
    on_site_records = models.IntegerField(verbose_name="现场开单记录明细（共几项）", blank=True, null=True)
    
    # 可修改字段
    project_number = models.CharField(max_length=100, verbose_name="项目编号", blank=True, null=True)
    date = models.DateField(verbose_name="日期", blank=True, null=True)
    construction_period = models.CharField(max_length=100, verbose_name="工程期限", blank=True, null=True)
    start_date = models.DateField(verbose_name="开工日期", blank=True, null=True)
    completion_date = models.DateField(verbose_name="竣工日期", blank=True, null=True)
    address = models.CharField(max_length=300, verbose_name="地址", blank=True, null=True)
    construction_unit = models.CharField(max_length=200, verbose_name="建设单位", blank=True, null=True)
    contact_person = models.CharField(max_length=100, verbose_name="联系人", blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name="电话", blank=True, null=True)
    contractor = models.CharField(max_length=200, verbose_name="施工单位", blank=True, null=True)
    contractor_contact = models.CharField(max_length=100, verbose_name="施工单位联系人", blank=True, null=True)
    owner = models.CharField(max_length=100, verbose_name="业主", blank=True, null=True)
    area = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="面积", blank=True, null=True)
    construction_cost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="建安造价", blank=True, null=True)
    rectification_details = models.IntegerField(verbose_name="整改完成情况明细（完成几项）", blank=True, null=True)
    remarks = models.TextField(verbose_name="备注", blank=True, null=True)
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'sub_projects'
        verbose_name = "子项目详细信息"
        verbose_name_plural = "子项目详细信息"
        ordering = ['-created_at']
    
    def get_status_display_custom(self):
        """获取项目状态的中文显示"""
        status_mapping = {
            '1': '正常',
            '2': '完成',
            '3': '需要整改',
            '4': '停工'
        }
        return status_mapping.get(self.status, '未知状态')
    
    def get_status_badge_class(self):
        """获取状态对应的CSS样式类"""
        status_class_mapping = {
            '1': 'bg-success',    # 绿色 - 正常
            '2': 'bg-primary',    # 蓝色 - 完成
            '3': 'bg-warning',    # 黄色 - 需要整改
            '4': 'bg-danger'      # 红色 - 停工
        }
        return status_class_mapping.get(self.status, 'bg-secondary')
    
    def __str__(self):
        return f"{self.project_number or 'N/A'} - {self.sub_project or 'N/A'}"


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False, verbose_name="是否为管理员")
    organization = models.CharField(max_length=200, verbose_name="所属单位", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"
    
    def __str__(self):
        return f"{self.user.username} - {'管理员' if self.is_admin else '普通用户'}" 