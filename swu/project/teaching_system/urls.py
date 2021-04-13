from django.urls import path, re_path, include
from . import views, view2
from  django.views.static import serve
from django.conf import settings

app_name = 'teaching_system'
urlpatterns = [
    re_path(r'^upfile/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^upfile/$', views.upfile, name='upfile'),
    re_path(r'^savefile/$', views.savefile, name='savefile'),
    re_path(r'^download/$', views.download, name='download'),
    re_path(r'^video/$', views.video, name='video'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^check/$', views.check, name='check'),

    re_path(r'^teacher_getcourse/$', views.teacher_getcourse, name='teacher_getcourse'),
    re_path(r'^get_course/$', views.get_course, name='get_course'),
    re_path(r'^get_sourcetype/$', views.get_sourcetype, name='get_sourcetype'),
    re_path(r'^up_source/$', views.up_source, name='up_source'),
    re_path(r'^get_source/$', views.get_source, name='get_source'),
    re_path(r'^del_source/$', views.del_source, name='del_source'),
    re_path(r'^update_info/$', views.update_info, name='update_info'),
    re_path(r'^get_department/$', views.get_department, name='get_department'),
    re_path(r'^get_dallcourse/$', views.get_dallcourse, name='get_dallcourse'),
    re_path(r'^course_info/$', views.course_info, name='course_info'),
    re_path(r'^get_sourcebytype/$', views.get_sourcebytype, name='get_sourcebytype'),
    re_path(r'^tsearch_source/$', views.tsearch_source, name='tsearch_source'),
    re_path(r'^get_courseinfo/$', views.get_courseinfo, name='get_courseinfo'),
    re_path(r'^load_studentinfo/$', views.load_studentinfo, name='load_studentinfo'),
    re_path(r'^get_student/$', views.get_student, name='get_student'),
    re_path(r'^search_student/$', views.search_student, name='search_student'),
    re_path(r'^reset_password/$', views.reset_password, name='reset_password'),
    re_path(r'^reset_passwordall/$', views.reset_passwordall, name='reset_passwordall'),
    re_path(r'^check_password/$', views.check_password, name='check_password'),
    re_path(r'^updata_icon/$', views.updata_icon, name='updata_icon'),
    re_path(r'^get_studentinfo/$', views.get_studentinfo, name='get_studentinfo'),
    re_path(r'^create_course/$', views.create_course, name='create_course'),
    re_path(r'^delete_course/$', views.delete_course, name='delete_course'),
    re_path(r'^admin_getteacherinfo/$', views.admin_getteacherinfo, name='admin_getteacherinfo'),
    re_path(r'^admin_setpassword/$', views.admin_setpassword, name='admin_setpassword'),
    re_path(r'^admin_delteacher/$', views.admin_delteacher, name='admin_delteacher'),
    re_path(r'^load_teacherinfo/$', views.load_teacherinfo, name='load_teacherinfo'),
    re_path(r'^search_teacher/$', views.search_teacher, name='search_teacher'),
    re_path(r'^get_teachertemplate/$', views.get_teachertemplate, name='get_teachertemplate'),
    re_path(r'^search_course/$', views.search_course, name='search_course'),
    re_path(r'^update_stus_teacher/$', views.update_stus_teacher, name='update_stus_teacher'),
    re_path(r'^delete_student/$', views.delete_student, name='delete_student'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^test/$', views.test, name='test'),

    re_path(r'^publish_task/$', views.publish_task, name='publish_task'),
    re_path(r'^get_homework/$', views.get_homework, name='get_homework'),
    re_path(r'^get_work/$', views.get_work, name='get_work'),
    re_path(r'^getTableData/$', views.getTableData, name='getTableData'),
    re_path(r'^del_work/$', views.del_work, name='del_work'),
    re_path(r'^del_homework/$', views.del_homework, name='del_homework'),
    re_path(r'^teacherget_course/$', views.teacherget_course, name='teacherget_course'),
    re_path(r'^teacherget_garden/$', views.teacherget_garden, name='teacherget_garden'),
    re_path(r'^gettaskbycourse/$', views.gettaskbycourse, name='gettaskbycourse'),
    re_path(r'^studentget_course/$', views.studentget_course, name='studentget_course'),
    re_path(r'^studentget_garden/$', views.studentget_garden, name='studentget_garden'),
    re_path(r'^student_upfile_homework/$', view2.student_upfile_homework, name='student_upfile_homework'),
    re_path(r'^get_upfilework_info/$', view2.get_upfilework_info, name='get_upfilework_info'),
    re_path(r'^submit_score/$', view2.submit_score, name='submit_score'),
    re_path(r'^stu_getscore/$', view2.stu_getscore, name='stu_getscore'),
    re_path(r'^get_statics_data/$', view2.get_statics_data, name='stu_getscore'),
    re_path(r'^get_stackbar_data/$', view2.get_stackbar_data, name='get_stackbar_data'),
    re_path(r'^get_homework_data/$', view2.get_homework_data, name='get_homework_data'),
    re_path(r'^fetch_all_sheet_names/$', view2.fetch_all_sheet_names, name='fetch_all_sheet_names'),
    re_path(r'^get_fileds_for_sheet/$', view2.get_fileds_for_sheet,name='get_fileds_for_sheet'),
    re_path(r'^get_whole_sheet/$', view2.get_whole_sheet, name='get_whole_sheet'),
    re_path(r'^multi_backup/$', view2.multi_backup, name='multi_backup'),
    re_path(r'^fetch_routes/$', view2.fetch_routes, name='fetch_routes'),
    re_path(r'^fetch_user_routes/$', view2.fetch_user_routes, name='fetch_user_routes'),
    re_path(r'^fetch_route_for_teacher/$', view2.fetch_route_for_teacher, name='fetch_route_for_teacher'),
    re_path(r'^set_permission_for_teacher/$', view2.set_permission_for_teacher, name='set_permission_for_teacher'),
    re_path(r'^fetch_discipline_tabledata/$', view2.fetch_discipline_tabledata, name='fetch_discipline_tabledata'),
    re_path(r'^submit_discipline_change/$', view2.submit_discipline_change, name='submit_discipline_change'),
    re_path(r'^add_discipline/$', view2.add_discipline, name='add_discipline'),
    re_path(r'^add_route_for_discipline/$', view2.add_route_for_discipline, name='add_route_for_discipline'),
    re_path(r'^fetch_route_component_map/$', view2.fetch_route_component_map, name='fetch_route_component_map'),
    re_path(r'^del_displine/$', view2.del_displine, name='del_displine'),
    re_path(r'^get_all_majors/$', views.get_all_majors, name='get_all_majors'),
    re_path(r'^create_class_set_routes/$', views.create_class_set_routes, name="create_class_set_routes"),
    re_path(r'^search_teacher_with_no/$', views.search_teacher_with_no, name="search_teacher_with_no"),
    re_path(r'^search_with_no/$', views.search_with_no, name="search_with_no"),
    re_path(r'^modify_read_limit/$', view2.modify_read_limit, name="modify_read_limit"),
    re_path(r'^get_course_under_major/$', view2.get_course_under_major, name="get_course_under_major"),
    re_path(r'^get_source_under_course/$', view2.get_source_under_course, name="get_source_under_course"),
    re_path(r'^source_status_change/$', view2.source_status_change, name="source_status_change"),


    re_path(r'^teacher_data/$', views.teacher_data, name='teacher_data'),
    re_path(r'^getImg/$', views.getImg, name='getImg'),
]