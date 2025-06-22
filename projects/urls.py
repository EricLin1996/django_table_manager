from django.urls import path
from . import views

urlpatterns = [
    # 登录相关
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('captcha/', views.captcha_image, name='captcha_image'),
    
    # 项目相关
    path('', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('export/excel/', views.export_projects_excel, name='export_projects_excel'),
    
    # 用户管理（仅管理员）
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
] 