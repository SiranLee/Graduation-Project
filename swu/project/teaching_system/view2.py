from django.shortcuts import render, HttpResponse
from django.http import FileResponse
import os
import sys
from django.conf import settings
from datetime import datetime
from django.utils.timezone import now, localtime
from django.utils.encoding import escape_uri_path
import cv2
from .models import Teacher, Student, Department, ImageStore, Course, Source, File, StudentStore, Mclass, StudentImage, TeacherImage, Admin, AdminImage, TeacherStore, StudentTime, StudentTimeNow, Work, Homework, StudentWork, Routes, TeacherRoutesMap, AdminRoutesMap, StudentRoutesMap, RouteComponentMap, StagingFile, StagingConvertPDF
import json
import base64
from .models import StudentWork, StudentWorkSource
import time
from django.apps import apps

modelMaps = [{'value': 'teacher','model':Teacher.teacherManage},
              {'value': 'department','model':Department.departmentManage},
              {'value': 'mclass','model':Mclass.mclassManager},
              {'value': 'source','model': Source.sourceManager},
              {'value': 'student','model': Student.studentManager},
              {'value': 'file', 'model': File.fileManager},
              {'value': 'course','model': Course.courseManager},
              {'value': 'admin','model': Admin.adminManage},
              {'value': 'homework','model': Homework.homeworkManager},
              {'value': 'work','model': Work.workManager},
              {'value': 'studentwork','model': StudentWork.studentWorkManager},
              {'value': 'studentworksource','model': StudentWorkSource.studentWorkSourceManager},
              {'value': 'routes', 'model': Routes.routeManager},
              {'value': 'teacherroutesmap', 'model': TeacherRoutesMap.teacherRoutesMapManager},
              {'value': 'adminroutesmap','model': AdminRoutesMap.adminRoutesMapManager},
              {'value': 'studentroutesmap', 'model': StudentRoutesMap.studentRoutesMapManager}]

def student_upfile_homework(request):
    # grade: '年级id'
    # major: '专业id'
    major = request.POST.get('major')
    # print(major)
    department = Department.departmentManage.get(dno=major)
    # course: '课程id'
    course_id = request.POST.get('course')
    course = Course.courseManager.get(no=course_id)
    # '作业id'
    task = request.POST.get('task')
    work = Homework.homeworkManager.get(pk=int(task))
    count = int(request.POST.get('count'))
    student_id = request.POST.get('id')
    students = Student.studentManager.filter(sno=student_id)
    mclass = course.mclass_set.get(department=department)
    student = None
    for item in students:
        print(item.mclass.cno)
        if item.mclass.cno == mclass.cno:
            print(item)
            student = item
            break
    #创建作业
    #为避免重复创建先进行检查
    studentworks = student.studentwork_set.all()
    for item in studentworks:
        if item.work.pk == work.pk:
            #已经有了，先删除
            item.delete()
    studentwork = StudentWork.studentWorkManager.createStudentWork(student, work)
    studentwork.save()
    #接着创建作业具体内容
    for i in range(count):
        file1 = request.FILES.get('file' + str(i))
        fileDir = os.path.join(settings.MEDIA_ROOT, 'student_homework')
        filePath = os.path.join(fileDir, file1.name)
        with open(filePath, 'wb') as fp:
            for info in file1.chunks():
                fp.write(info)
        # print(os.path.join('/upfile/source', file1.name))
        studentworksource = StudentWorkSource.studentWorkSourceManager.createStudentWorkSource(file1.name, r'/upfile/student_homework/' + file1.name, studentwork)
        studentworksource.save()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'message': 'ok',
            'record': {
                'task_id': task,
                'stu_major': department.dname,
                'stu_course': course.name,
                'stu_taskTitle': work.title,
                'stu_submitDate': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            }
        }
    }))

def get_upfilework_info(request):
    grade_id = request.GET.get('grade_id')
    # class_id = request.GET.get('class_id')
    course_id = request.GET.get('course_id')
    course = Course.courseManager.get(no=course_id)
    task_id = request.GET.get('task_id')
    # print(task_id)
    work = Homework.homeworkManager.get(pk=int(task_id))
    major_id = request.GET.get('major_id')
    department = Department.departmentManage.get(dno=major_id)
    limit = int(request.GET.get('limit'))
    page = int(request.GET.get('page'))
    status = request.GET.get('status')
    #print(status)

    studentWorks = work.studentwork_set.all()
    studentWorkslist = []
    for item in studentWorks:
        if status == 'success' and item.status == '已批改':
            studentWorkslist.append(item)
        if status == 'info' and item.status == '未批改':
            studentWorkslist.append(item)

    if status == 'all':
        studentWorkslist = studentWorks

    listTotal = len(studentWorkslist)

    if page * limit <= listTotal:
        studentWorkslist = studentWorkslist[(page - 1) * limit:(page - 1) * limit + limit]
    if int(page) * int(limit) - listTotal < int(limit) and int(page) * int(limit) > listTotal:
        studentWorkslist = studentWorkslist[(int(page) - 1) * int(limit):listTotal]
    if int(page) * int(limit) - listTotal > int(limit):
        return HttpResponse(json.dumps({
            'code': 20000,
            'data': {
                'listTotal': 0,
                'list': [],
            }
        }))


    list = []
    listTotal = len(studentWorkslist)
    for item in studentWorkslist:
        mtype = None
        if item.status == '未批改':
            mtype = 'info'
        else:
            mtype = 'success'
        dic = {
            'id': work.pk,
            'stu_number': item.student.sno,
            'stu_grade': grade_id,
            'stu_major':  department.dname,
            'stu_class': item.student.cs,
            'name': item.student.sname,
            'score': item.score,
            'type': mtype,
            'state':item.status,
            'task': work.title,
            'link': item.studentworksource_set.all()[0].url
        }
        list.append(dic)


    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'listTotal': listTotal,
            'list': list
        }
    }))

#打分
def submit_score(request):
    student_id = eval(request.body)['id']
    course_id = eval(request.body)['course_id']
    course = Course.courseManager.get(no=course_id).pk
    class_id = Mclass.mclassManager.get(con=course).pk
    student = Student.studentManager.get(sno=student_id, mclass=class_id)
    score = eval(request.body)['score']
    # course_id = eval(request.body)['course_id']
    task_id = eval(request.body)['task_id']
    print(task_id)
    work = Homework.homeworkManager.get(pk = int(task_id))
    studentwork = StudentWork.studentWorkManager.get(student=student, work=work)
    studentwork.score = int(score)
    studentwork.status = '已批改'
    studentwork.save()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'message': 'ok',
            'ack': {
                'id': task_id,
                'stu_number': student_id,
                'stu_grade': student.grade,
                'stu_major': student.department.dname,
                'stu_class': student.cs,
                'name': student.sname,
                'score': score,
                'type': 'success',
                'state': '已批改',
                'task': work.title,
                'link': studentwork.studentworksource_set.all()[0].url
            }
        }
    }))

# 学生查询成绩
def stu_getscore(request):
    stu_no = request.GET.get('id')
    dep_name = request.GET.get('dept')
    # 通过dep_name 找课程
    course = []
    dep_id = Department.departmentManage.get(dname=dep_name).dno
    courseModles = Course.courseManager.filter(dno=dep_id)
    for modle in courseModles:
        course.append(modle.name)
    # 找出学生上交的作业
    stu_avg_works_score = []
    stu_works_score = []
    stus = Student.studentManager.filter(sno=stu_no)
    for stu in stus:
        # 对每个stu求出其对应课程都提交了哪些作业
        course_id = Mclass.mclassManager.get(pk=stu.mclass.pk).con.pk
        course_name = Course.courseManager.get(pk=course_id).name
        publish_works = Homework.homeworkManager.filter(no=course_id)
        checked_works = []
        scores = []
        task_names = []
        for pub_work in publish_works:
            checked_work = StudentWork.studentWorkManager.get(work=pub_work.pk, student=stu.pk)
            if checked_work.status == '已批改':
                checked_works.append(checked_work)
        if len(checked_works) > 0:
            avarage_score = 0
            score = 0
            for checked_work in checked_works:
                task_names.append(checked_work.work.title)
                scores.append(checked_work.score)
                score = score + checked_work.score
            avarage_score = score/len(checked_works)
            item = {
                'course': course_name,
                'scores': scores,
                'tasks':task_names
            }
            dic = {
                'course': course_name,
                'avg_score': avarage_score,
                'max_score': 100
            }
            stu_avg_works_score.append(dic)
            stu_works_score.append(item)
        else:
            dic = {
                'course': course_name,
                'avg_score': 0,
                'max_score': 100
            }

    return HttpResponse(json.dumps({
        'code': 20000,
        'avg_scores': stu_avg_works_score,
        'scores': stu_works_score
    }))

# 管理员的数据统计请求
def get_statics_data(request):
    all_teachers = Teacher.teacherManage.filter(isDelete=0).count()
    all_courses = Course.courseManager.filter(isDelete=False).count()
    all_sources = File.fileManager.filter(isDelete=False).count()
    dep_homeworks = []
    stu_count = 0
    dep_stus = []
    try:   
        # 各专业作业数
        deps = Department.departmentManage.all()
        for dep in deps:
            courses = Course.courseManager.filter(dno=dep.pk)
            count = 0
            for course in courses:
                count = count + Homework.homeworkManager.filter(no=course.pk).count()
            dic = {
                'dep': dep.dname,
                'count': count
            }
            dep_homeworks.append(dic)
        # 学生总数
        all_classes = Mclass.mclassManager.all()
        one_class_stus = Student.studentManager.filter(mclass=all_classes[0].pk)
        one_class_stunos = []
        other_class_stunos = []
        stu_count = one_class_stus.count()
        for stu in one_class_stus:
            one_class_stunos.append(stu.sno)
        for single_class in all_classes:
            if single_class.pk != all_classes[0].pk:
                other_class_stus = Student.studentManager.filter(mclass=single_class.pk)
                for stu in other_class_stus:
                    other_class_stunos.append(stu.sno)
                commen_stunos = set(one_class_stunos).intersection(set(other_class_stunos))
                stu_count = stu_count + len(other_class_stunos) - len(commen_stunos)
                one_class_stunos = list(set(one_class_stunos).union(other_class_stunos))
                other_class_stunos = []
        # 各专业学生人数
        for dep in deps:
            raw_stus = Student.studentManager.filter(department=dep.pk)
            result = raw_stus.values('sno').distinct()
            dic = {
                'dep_name': dep.dname,
                'dep_stu_count': result.count(),
            }
            dep_stus.append(dic)
    except:
        pass

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'total_teachers': all_teachers,
            'total_stus': stu_count,
            'total_course': all_courses,
            'total_sources': all_sources,
            'dep_homeworks': dep_homeworks,
            'dep_stus': dep_stus
        }
    }))


def get_stackbar_data(request):
    dep_id = request.GET.get('dep_id')
    stack_bar_data = []
    # 此专业的课程
    course_in_dep = Mclass.mclassManager.filter(department=dep_id)
    source_types = Source.sourceManager.filter(stype=0)
    print(course_in_dep)
    for course in course_in_dep:
        sources_in_course = File.fileManager.filter(no=course.con)
        source_counts = []
        
        for source_type in source_types:
            dic = {
                'type': source_type.sname,
                'count': sources_in_course.filter(sno=source_type.pk).count()
            }
            source_counts.append(dic)
        dictionary = {
            'course': {
                'no': course.con.no,
                'name': course.cname
            },
            'sources_by_types': source_counts
        }
        stack_bar_data.append(dictionary)
    
    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'stack_bar_data': stack_bar_data 
        }
    }))

# 指定专业指定课程的各次作业批改情况
def get_homework_data(request):
    dep_id = request.GET.get('dep_id')
    course_id = request.GET.get('course_id')
    checked_data = []
    try:
        course = Course.courseManager.get(no=course_id)
        works_under_course = Homework.homeworkManager.filter(no=course.pk)
        index = 1
        for work in works_under_course:
            finished_works = StudentWork.studentWorkManager.filter(work=work.pk)
            checked = 0
            unchecked = 0
            for finished_work in finished_works:
                if finished_work.status == '已批改':
                    checked = checked + 1
                else:
                    unchecked = unchecked + 1
            dic = {
                'times': '第'+str(index)+'次',
                'status': {
                    'checked': checked,
                    'unchecked': unchecked,
                    'total': finished_works.count()
                }
            }
            index = index + 1
            checked_data.append(dic)
    except:
        pass

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'checked_data': checked_data
        }
    }))

# 获取所有表名
def fetch_all_sheet_names(request):
    result = []
    labels = ['教师表','专业表','班级表','资源类表','学生表','资源表',
              '课程表','管理员表','课程任务表',
              '课程任务资源表','学生提交作业表',
              '学生提交作业资源表','页面路由表','教师页面权限映射','管理员页面权限映射']
    values = ['teacher', 'department','mclass','source','student','file',
              'course','admin','homework','work',
              'studentwork','studentworksource','routes','teacherroutesmap','adminroutesmap']
    for index in range(len(labels)):
        dic = {
            'label': labels[index],
            'value': values[index]
        }
        result.append(dic)
    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'result': result
        }
    }))

# 获取所选择的表所有字段
def get_fileds_for_sheet(request):
    sheet = request.GET.get('sheet')
    modelObj = apps.get_model('teaching_system', sheet)
    fileds = []
    for field in modelObj._meta.fields:
        fileds.append(field.name)
    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'fileds': fileds
        }
    }))

# 获取整张表的内容
def get_whole_sheet(request):
    selectSheet = request.GET.get('sheet')
    targetModel = None
    for item in modelMaps:
        if item['value'] == selectSheet:
            targetModel = item['model']
            break
    targetItems = targetModel.all()
    modelObj = apps.get_model('teaching_system', selectSheet)
    fileds = []
    for field in modelObj._meta.fields:
        fileds.append(field.name)
    tableData = []
    for index in range(len(targetItems)):
        dic = {}
        for filed in fileds:
            
            if isinstance(getattr(targetItems[index], filed), int) or isinstance(getattr(targetItems[index], filed), bool) or isinstance(getattr(targetItems[index], filed), str) or getattr(targetItems[index], filed) is None:
                if filed != 'password':
                    dic[filed] = getattr(targetItems[index], filed)
            elif isinstance(getattr(targetItems[index], filed), datetime):
                dic[filed] = getattr(targetItems[index], filed).strftime("%Y-%m-%d %H:%M:%S")
            else:
                dic[filed] = getattr(getattr(targetItems[index], filed),'pk')
        tableData.append(dic)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'table': tableData
        }
    }))

# 多表备份
def multi_backup(request):
    settings = request.GET.get('settings')
    settings_obj = json.loads(settings)
    results = []
    for item in settings_obj:
        sheetName = item['sheetName']
        selectFields = item['selectFields']
        for element in modelMaps:
            if element['value'] == sheetName:
                sheetModel = element['model']
                break
        allObjects = []
        for obj in sheetModel.all():
            dic = {}
            for filed in selectFields:
                if isinstance(getattr(obj, filed), int) or isinstance(getattr(obj, filed), bool) or isinstance(getattr(obj, filed), str):
                    dic[filed] = getattr(obj, filed)
                elif isinstance(getattr(obj, filed), datetime):
                    dic[filed] = getattr(obj, filed).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    dic[filed] = getattr(getattr(obj, filed),'pk')
            allObjects.append(dic)
        result = {
            'sheetName': sheetName,
            'sheetData': allObjects
        }
        results.append(result)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'result': results
        }
    }))

# 获取路由表
def fetch_routes(request):
    all_parents = Routes.routeManager.filter(parent=0)
    routes = []
    for parent in all_parents:
        dic = {}
        dic['label'] = parent.title
        dic['route_id'] = parent.pk
        all_children = Routes.routeManager.filter(parent=parent.pk)
        dic['children'] = []
        for child in all_children:
            child_dic = {}
            child_dic['label'] = child.title
            child_dic['route_id'] = child.pk
            dic['children'].append(child_dic)
        routes.append(dic)
    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'routes': routes 
        }
    }))

# 获取特定权限的路由表
def fetch_user_routes(request):
    roles = json.loads(request.body)['roles']
    id = json.loads(request.body)['id']
    fileds = []
    result = []
    parent_routes = []
    routes = []

    for filed in apps.get_model('teaching_system', 'routes')._meta.fields:
        fileds.append(filed.name)
    
    if roles[0] == 'admin':
        admin_id = Admin.adminManage.get(ano=id).pk
        routesMap = AdminRoutesMap.adminRoutesMapManager.filter(admin=admin_id)
        for adminRoute in routesMap:
            if adminRoute.route.parent == 0:
                parent_routes.append(adminRoute.route)
            routes.append(adminRoute.route)
    elif roles[0] == 'teacher':
        teacher_id = Teacher.teacherManage.get(tno=id)
        routesMap = TeacherRoutesMap.teacherRoutesMapManager.filter(tea=teacher_id)
        for teacherRoute in routesMap:
            if teacherRoute.routes.parent == 0:
                parent_routes.append(teacherRoute.routes)
            routes.append(teacherRoute.routes)
    else:
        routesMap = StudentRoutesMap.studentRoutesMapManager.filter(stu_no=id)
        for stuRoute in routesMap:
            route_id = stuRoute.route_id
            target = Routes.routeManager.get(pk=route_id)
            if target.parent == 0:
                parent_routes.append(target)
            routes.append(target)
    
    for parent in parent_routes:
        dic = {}
        dic['path'] = parent.path
        dic['component'] = parent.component
        dic['meta'] = {}
        dic['meta']['title'] = parent.title
        dic['meta']['icon'] = parent.icon
        dic['meta']['roles'] = roles
        if parent.props == 1:
            dic['props'] = True
        else:
            dic['props'] = False
        if not(parent.redirect is None):
            dic['meta']['redirect'] = parent.redirect
        dic['children'] = []
        for route in routes:
            if route.parent == parent.pk:
                chil_dic = {}
                chil_dic['path'] = route.path
                chil_dic['name'] = route.name
                chil_dic['component'] = route.component
                chil_dic['meta'] = {}
                chil_dic['meta']['title'] = route.title
                chil_dic['meta']['icon'] = route.icon
                chil_dic['meta']['roles'] = roles
                if route.currentPage == 1 :
                    chil_dic['meta']['currentPage'] = route.currentPage
                else:
                    chil_dic['meta']['currentPage'] = -1
                if route.hidden == 1:
                    chil_dic['hidden'] = True
                else:
                    chil_dic['hidden'] = False
                if route.props == 1:
                    chil_dic['props'] = True
                else:
                    chil_dic['props'] = False
                dic['children'].append(chil_dic)
        result.append(dic)
    
        

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'routes': result
        }
    }))


# 获取特定教师的权限数组
def fetch_route_for_teacher(request):
    tea_no = request.GET.get('tea_no')
    target_teacher_id = Teacher.teacherManage.get(tno=tea_no).pk
    routes = TeacherRoutesMap.teacherRoutesMapManager.filter(tea=target_teacher_id)
    routes_id = []
    for route in routes:
        if route.routes.parent == 0:
            target_childs = []
            childroutes = Routes.routeManager.filter(parent=route.routes.parent)
            for chil_route in routes:
                if chil_route.routes.parent == route.routes.pk:
                    target_childs.append(chil_route)
            if childroutes.count()>len(target_childs):
                continue
            else:
                routes_id.append(route.routes.pk)
        else:
            routes_id.append(route.routes.pk)
    
    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'routes': routes_id
        }
    }))

# 设置教师的权限
def set_permission_for_teacher(request):
    obj = json.loads(request.body)
    add_permission = obj['add_permission']
    del_permission = obj['del_permission']
    
    target_teacher = Teacher.teacherManage.get(tno=obj['id'])
    tea_id = target_teacher.pk
    routes_id = []

    for permission in add_permission:
        try:
            route_self = Routes.routeManager.get(pk=permission)
            teacher_route_map = TeacherRoutesMap.teacherRoutesMapManager.createTeacherRoutesMap(target_teacher, route_self)
            teacher_route_map.save()
        except:
            pass
    for permission in del_permission:
        try:
            route_self = Routes.routeManager.get(pk=permission)
            teacher_route_map = TeacherRoutesMap.teacherRoutesMapManager.get(tea=target_teacher, routes=route_self)
            teacher_route_map.delete()
        except:
            pass

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            "message": "ok"
        }
    }))

#返回学科信息
def fetch_discipline_tabledata(request):
    all_departments = Department.departmentManage.all()
    index = 1
    result = []
    for department in all_departments:
        target_route = Routes.routeManager.get(title=department.dname)
        all_teachers = Course.courseManager.filter(dno=department).values('tno').distinct().count()
        all_students = Student.studentManager.filter(department=department).count()
        all_course = Course.courseManager.filter(dno=department, isDelete=False)
        names = []
        for name_str in list(all_course.values('name')):
            names.append(name_str['name'])
        course_str = ','.join(names)
        children = []

        for course in all_course:
            dic = {}
            index = index + 1
            dic['id'] = index 
            dic['sequence'] = index
            dic['name'] = department.dname
            dic['teachers'] = Course.courseManager.filter(name=course.name).count()
            # print(Student.studentManager.filter(mclass=Mclass.mclassManager.get(con=course)))
            try:
                dic['students'] = Student.studentManager.filter(mclass=Mclass.mclassManager.get(con=course)).count()
            except:
                pass
            dic['courses'] = course.name
            
            children.append(dic)
            print(index)
        wrapper = {}
        index = index + 1
        wrapper['id'] = index
        wrapper['sequence'] = index
        wrapper['name'] = department.dname
        wrapper['en_name'] = target_route.name
        wrapper['teachers'] = all_teachers
        wrapper['students'] = all_students
        wrapper['courses'] = course_str
        wrapper['children'] = children
        wrapper['key'] = department.pk
        result.append(wrapper)
        
    return HttpResponse(json.dumps({
      'code': 20000,
      'data':{
        'table': result
      }
    }))

# 更改学科信息
def submit_discipline_change(request):
    target = json.loads(request.body)['discipline']
    changedName = target['name']
    key = target['key']
    try:
        target_dep = Department.departmentManage.get(pk=key)
        target_dep.dname = changedName
        target_dep.save()
    except:
        pass


    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'message': 'ok'
        }
    }))

# 添加学科
def add_discipline(request):
    discipline_name = json.loads(request.body)['disciplineName']
    new_discipline = {}
    try:
        suffix = Routes.routeManager.filter(parent=list(Routes.routeManager.filter(parent=0))[0].pk).count()
        dno = Department.departmentManage.last().pk+1
        target_item = Department.departmentManage.createDepartment(dno, discipline_name, False)
        target_item.save()
        new_discipline['name'] = discipline_name
        new_discipline['teachers'] = 0
        new_discipline['students'] = 0
        new_discipline['courses'] = ''
        new_discipline['children'] = []
        new_discipline['key'] = target_item.pk
    except:
        pass


    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'item': new_discipline,
            'suffix': suffix,
        }
    }))

# 为刚刚添加的学科添加路由
def add_route_for_discipline(request):
    requestBody = json.loads(request.body)
    add_discipline_cn_name = requestBody['disciplineName_cn']
    add_discipline_en_name = requestBody['disciplineName_en']
    add_discipline_icon = requestBody['icon']
    controller_id = requestBody['id']
    component_path = requestBody['path']
    
    route = Routes.routeManager.createRoutesManager(add_discipline_en_name, add_discipline_en_name, add_discipline_en_name, add_discipline_cn_name, add_discipline_icon, 1, 0, None, 1)
    route.save()
    admin = Admin.adminManage.get(ano=controller_id)
    admin_map = AdminRoutesMap.adminRoutesMapManager.createAdminRoutesMap(admin, route)
    admin_map.save()
    route_component = RouteComponentMap.routeComponentMapManager.createRouteComponentMap(add_discipline_en_name, component_path)
    route_component.save()

    

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'data': 'ok',
        }
    }))

# 获取组件映射
def fetch_route_component_map(request):
    result = []
    component_map_set = RouteComponentMap.routeComponentMapManager.all()
    for component_map in component_map_set:
        dic = {}
        dic['component_key'] = component_map.component_key
        dic['component_path'] = component_map.component_path
        result.append(dic)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'map':result
        }
    }))

# 删除学科
def del_displine(request):
    body = json.loads(request.body)
    discipline_id = body['id']
    discipline_name = body['discipline_name']
    discipline_en_name = body['discipline_en_name']
    
    department = Department.departmentManage.get(pk=discipline_id)
    route = Routes.routeManager.get(title=discipline_name)
    admin_route_map = AdminRoutesMap.adminRoutesMapManager.get(route=route)
    route_component_map = RouteComponentMap.routeComponentMapManager.get(component_key=discipline_en_name)
    department.delete()
    route.delete()
    admin_route_map.delete()
    route_component_map.delete()
    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'message': 'ok'
        }
    }))
    # except:
    #     pass
    # return HttpResponse(json.dumps({
    #         'code': 20000,
    #         'data':{
    #             'message': '网络出错，请稍后再试'
    #         }
    #     }))

def add_download_times(request):
    target_source_id = json.loads(request.body)['source_id']

    target_source = File.fileManager.get(pk=target_source_id)
    target_source.download_times = target_source.download_times + 1
    target_source.save()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'message': 'ok'
        }
    }))

def modify_read_limit(request):
    source_id = json.loads(request.body)['source_id']
    read_limit = json.loads(request.body)['read_limit']

    source = File.fileManager.get(pk=source_id)
    source.not_available2all = read_limit
    source.save()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            "message": 'ok'
        }
    }))

from django.db.models import Count
def create_source_dic(source, staging=False):
    if staging :
        dic = {
            'source_id': source.id,
            'up_date': str(source.up_time).split()[0],
            'source_type': source.sno.sname,
            'source_title': source.title,
            'source_name': source.filename,
            'source_course': source.cno.name,
            'source_des': source.fileDes,
            'source_link': source.url,
            'source_status': str(source.fileStatus),
            'source_not_available2all': source.not_available2all,
            'source_fail_resaon': source.failReason
        }
    else:
        dic = {
            'up_date': str(source.time).split()[0],
            'source_type': source.sno.sname,
            'source_title': source.title,
            'source_name': source.filename,
            'source_course': source.no.name,
            'source_des': source.describe,
            'source_download_time': source.download_times,
        }
    return dic

def split_page(sources, current_page, page_size, start_index, totalCount, result, staging=False):
    if start_index - 1 + page_size >= totalCount:
        for source in sources[start_index-1:totalCount]:
            # 此时不足一页或者刚好一页
            result.append(create_source_dic(source, staging))
    else:
        #此时超出一页,只获取一页的数据
        for source in sources[start_index-1:start_index+page_size-1]:
            result.append(create_source_dic(source, staging))
    

# 根据专业id来查已上传已审核的资源
def get_sourse_under_major(request):
    major_id = request.GET.get('major_id')
    source_type = request.GET.get('currentType')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))
    dep = Department.departmentManage.get(pk=major_id).dno   
    all_types = Source.sourceManager.all()[0:3]
    if source_type == '-1':
        sources = File.fileManager.filter(dno=dep)
    else:
        source_no = Source.sourceManager.get(sno=source_type)
        sources = File.fileManager.filter(dno=dep, sno=source_no)
        
    totalCount = len(sources)
    result = []
    heatMap = []
    pieData = []
    for file_type in all_types:
        dic = {
            'name': file_type.sname,
            'value': 0
        }
        for source in sources:
            if source.sno == file_type:
                dic['value'] = dic['value'] + 1
        pieData.append(dic)

    start_index = (current_page-1) * page_size + 1
    
    # 从start_index开始获取，当不足一页的量的时获取到最后一个，当超出一页的量时获取一页的量
    split_page(sources, current_page, page_size, start_index, totalCount, result)

    heats = sources.extra(select={"time": "DATE_FORMAT(time,'%%Y-%%m-%%d')"}).values('time').annotate(Count('time'))
    for heat in heats:
        dic = {
            'time':heat['time'],
            'heat':heat['time__count']
        }
        heatMap.append(dic)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'sources': result,
            'total': totalCount,
            'heat': heatMap,
            'pieData': pieData
        }
    }))
# 根据课程id来过滤资源
def get_source_under_course(request):
    course_id = request.GET.get('course_id')
    source_type = request.GET.get('currentType')
    current_page = int(request.GET.get('currentPage'))
    page_size = int(request.GET.get('pageSize'))
    all_types = Source.sourceManager.all()[0:3]
    sources = None
    if source_type == '-1':
        sources = File.fileManager.filter(no=course_id)
    else:
        source_no = Source.sourceManager.get(sno=source_type)
        sources = File.fileManager.filter(no=course_id, sno=source_no)

    totalCount = len(sources)
    result = []
    heatMap = []
    pieData = []
    for file_type in all_types:
        dic = {
            'name': file_type.sname,
            'value': 0
        }
        for source in sources:
            if source.sno == file_type:
                dic['value'] = dic['value'] + 1
        pieData.append(dic)
    start_index = start_index = (current_page-1) * page_size + 1

    split_page(sources, current_page, page_size, start_index, totalCount, result)
    heats = sources.extra(select={"time": "DATE_FORMAT(time,'%%Y-%%m-%%d')"}).values('time').annotate(Count('time'))
    for heat in heats:
        dic = {
            'time':heat['time'],
            'heat':heat['time__count']
        }
        heatMap.append(dic)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'sources': result,
            'total': totalCount,
            'heat': heatMap,
            'pieData': pieData
        }
    }))

# 根据资源类型来过滤资源
def source_type_change(request):
    major_id = request.GET.get('major_id')
    course_id = request.GET.get('course_id')
    source_type = request.GET.get('type')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))

    sources = None
    source_no = Source.sourceManager.get(sno=source_type)
    result = []

    # 首先判断是已知课程过滤资源还是未知课程过滤资源
    if course_id == '-1':
        # 未知课程过滤资源
        dep = Department.departmentManage.get(pk=major_id).dno
        sources = File.fileManager.filter(dno=dep, sno=source_no)
    else:
        # 已知课程过滤资源
        source_no = Source.sourceManager.get(sno=source_type)
        sources = File.fileManager.filter(no=course_id, sno=source_no)
    
    totalCount = len(sources)
    start_index = start_index = (current_page-1) * page_size + 1
    split_page(sources, current_page, page_size, start_index, totalCount, result)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'sources': result,
            'total': totalCount
        }
    }))

# 获取审核状态选项
def get_staging_types(request):

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'staging_types':[
                {'name': '待审核', 'value': 1},
                {'name': '通过', 'value': 2},
                {'name': '未通过', 'value': 3}
            ]
        }
    }))

# 按专业获取待审核的资源
def get_staging_file_under_major(request):
    major_id = request.GET.get('major_id')
    source_type = request.GET.get('current_type')
    source_status = request.GET.get('current_status')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))

    sources = None
    if source_type == '-1' and source_status == '-1':
        #不过滤
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id)
    elif source_type == '-1':
        # 按状态过滤
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, fileStatus=source_status)
    elif source_status == '-1':
        # 按类型过滤
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, sno=Source.sourceManager.get(isDelete=False, sno=staging_type))
    else:
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, sno=Source.sourceManager.get(isDelete=False, sno=staging_type), fileStatus=source_status)
    
    totalCount = len(sources)
    start_index = (current_page-1) * page_size + 1
    result = []

    split_page(sources, current_page, page_size, start_index, totalCount, result, True)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'sources': result,
            'total': totalCount
        }
    }))

# 管理员根据课程来获取待审核资源
def get_staging_sources_under_course(request):
    course_id = request.GET.get('course_id')
    staging_type = request.GET.get('current_type')
    staging_status = request.GET.get('current_status')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))

    sources = None
    if staging_type == '-1' and staging_status == '-1':
        #不过滤
        sources = StagingFile.stagingFileManager.filter(isDelete=False, cno=course_id)
    elif staging_type == '-1':
        # 按状态过滤
        sources = StagingFile.stagingFileManager.filter(isDelete=False, cno=course_id, fileStatus=staging_status)
    elif staging_status == '-1':
        # 按类型过滤
        source_type = Source.sourceManager.get(isDelete=False, sno=staging_type)
        sources = StagingFile.stagingFileManager.filter(isDelete=False, cno=course_id, sno=source_type)
    else:
        source_type = Source.sourceManager.get(isDelete=False, sno=staging_type)
        sources = StagingFile.stagingFileManager.filter(isDelete=False, cno=course_id, sno=source_type, fileStatus=staging_status)

    totalCount = len(sources)
    start_index = (current_page - 1) * page_size + 1
    result = []

    split_page(sources, current_page, page_size, start_index, totalCount, result, True)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'sources': result,
            'total': totalCount
        }
    }))

# 管理员根据资源类型来获取staging资源
def get_staging_source_under_type(request):
    major_id = request.GET.get('major_id')
    course_id = request.GET.get('course_id')
    current_type = request.GET.get('current_type')
    current_status = request.GET.get('current_status')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))

    source_type = Source.sourceManager.get(sno=current_type)

    sources = None
    if course_id == '-1' and current_status == '-1':
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, sno=source_type)
    elif course_id == '-1':
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, fileStatus=current_status, sno=source_type)
    elif current_status == '-1':
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, cno=course_id, sno=source_type)
    else:
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, fileStatus=current_status, cno=course_id, sno=source_type)
    
    totalCount = len(sources)
    start_index = (current_page - 1) * page_size + 1
    result = []

    split_page(sources, current_page, page_size, start_index, totalCount, result, True)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'sources': result,
            'total': totalCount
        }
    }))

# 根据资源状态的判断 status已知
def judge_base_on_status(course_id, current_type, sources, major_id, current_status):
    if course_id == '-1' and current_type == '-1':
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, fileStatus=current_status)
    elif course_id == '-1':
        source_type = Source.sourceManager.get(sno=current_type)
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, fileStatus=current_status, sno=source_type)
    elif current_type == '-1':
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, cno=course_id, fileStatus=current_status)
    else:
        source_type = Source.sourceManager.get(sno=current_type)
        sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, fileStatus=current_status, cno=course_id, sno=source_type)
    return sources
# 管理员通过资源状态来获取staging资源
def get_staging_source_under_status(request):
    major_id = request.GET.get('major_id')
    course_id = request.GET.get('course_id')
    current_type = request.GET.get('current_type')
    current_status = request.GET.get('current_status')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))

    sources = None
    
    sources = judge_base_on_status(course_id, current_type, sources, major_id, current_status)

    totalCount = len(sources)
    start_index = (current_page - 1) * page_size + 1
    result = []

    split_page(sources, current_page, page_size, start_index, totalCount, result, True)

    return HttpResponse(json.dumps({
        'code': 20000,
        'data': {
            'sources': result,
            'total': totalCount
        }
    }))
    

def create_staging_sources_dic(source):
    dic = {
        'upload_id': source.pk,
        'upload_date': str(source.up_time).split()[0],
        'upload_type': source.sno.sname,
        'upload_title': source.title,
        'upload_filename': source.filename,
        'upload_status': str(source.fileStatus),
        'upload_intro': source.fileDes,
        'upload_filelink': source.url,
        'not_available2all': source.not_available2all,
        'upload_fail_reason': source.failReason
    }
    return dic

def split_staging_page(sources, page_size, start_index, totalCount, result):
    if start_index - 1 + page_size >= totalCount:
        for source in sources[start_index-1:totalCount]:
            # 此时不足一页或者刚好一页
            result.append(create_staging_sources_dic(source))
    else:
        #此时超出一页,只获取一页的数据
        for source in sources[start_index-1:start_index+page_size-1]:
            result.append(create_staging_sources_dic(source))

# 教师按照课程来获取待审核和未通过的资源
def get_staging_under_course(request):
    course_no = request.GET.get('course_id')
    current_page = int(request.GET.get('page'))
    page_size = int(request.GET.get('limit'))
    course = Course.courseManager.get(isDelete=False, no=course_no)
    
    sources = StagingFile.stagingFileManager.filter(cno=course, fileStatus__in=[1, 3])
    totalCount = len(sources)
    start_index = (current_page - 1) * page_size + 1
    result = []

    split_staging_page(sources, page_size, start_index, totalCount, result)
    
    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'sources': result,
            'total': totalCount
        }
    }))

import shutil
# 改变staging资源的状态
def change_staging_status(request):
    is_fail = request.GET.get('isFail')
    reason_for_fail = request.GET.get('reasonForFail')
    staging_id = request.GET.get('staging_id')

    staging_source = StagingFile.stagingFileManager.get(isDelete=False, pk=staging_id)
    if is_fail == 'true':
        # 打回
        staging_source.isDelete = False
        staging_source.fileStatus = 3
        staging_source.failReason = reason_for_fail
    else:
        # 通过
        #修改状态
        # staging_source.isDelete = True
        staging_source.fileStatus = 2
        # 将staging_source文件夹下的对应资源拷贝到source文件夹下，然后删除原文件
        origin_path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'stagingSource'), staging_source.filename)
        dest_path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'source'), staging_source.filename)
        shutil.move(origin_path, dest_path)
        # 向File模型中添加对应项目 
        source_file = File.fileManager.createFileFromStaging(staging_source.fileDes, 
        r'/upfile/source/'+staging_source.filename, staging_source.title, staging_source.filename, 
        0, staging_source.dno.dno, staging_source.not_available2all, staging_source.tno, 
        staging_source.sno, staging_source.cno, staging_source.up_time)
        source_file.save()
        # 删除stagingConvertFiles文件夹中的对应文件
        convertpdf_path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'stagingConvertFiles'), os.path.splitext(staging_source.filename)[0]+'.pdf') 
        if os.path.isfile(convertpdf_path):
            os.remove(convertpdf_path)
            # 删除staging_convert_pdf中的对应记录
            StagingConvertPDF.stagingConvertPDFManager.get(staging_pdf_name=staging_source.filename).delete()
        
    # staging_source记录保存
    staging_source.save()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'message': 'ok'
        }
    }))

# 删除已经通过的文件
def del_pass_staging(request):
    pass_staging_id = json.loads(request.body)['id']

    pass_staging_source = StagingFile.stagingFileManager.get(pk=pass_staging_id)

    pass_staging_source.delete()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'message': 'ok'
        }
    }))

# 按照资源标题关键字来搜索资源，包括审核通过资源和staging资源
def search_source_with_value(request):
    key_word = request.GET.get('value')
    is_staging = request.GET.get('staging')
    major_id = request.GET.get('current_major')
    current_course = request.GET.get('current_course')
    current_type = request.GET.get('current_type')
    current_status = request.GET.get('current_status')
    current_page = int(request.GET.get('current_page'))
    page_size = int(request.GET.get('page_size'))

    dep = Department.departmentManage.get(pk=major_id).dno
    sources = None
    result = []
    start_index = (current_page - 1) * page_size + 1

    if is_staging == 'false':
        # 搜索所有通过的资源
        is_staging = False
        if current_course == '-1' and current_type == '-1':
            sources = File.fileManager.filter(isDelete=False, dno=dep, title__contains=key_word)
        elif current_course == '-1':
            source_no = Source.sourceManager.get(sno=current_type)
            sources = File.fileManager.filter(isDelete=False, dno=dep, sno=source_no, title__contains=key_word)
        elif current_type == '-1':
            sources = File.fileManager.filter(isDelete=False, dno=dep, no=current_course, title__contains=key_word)
        else:
            source_no = Source.sourceManager.get(sno=current_type)
            sources = File.fileManager.filter(isDelete=False, dno=dep, no=current_course, sno=source_no, title__contains=key_word)
    else:
        is_staging = True
        if current_status == '-1': # 只考虑course, type
            if current_course == '-1' and current_type == '-1':
                sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, title__contains=key_word)
            elif current_course == '-1':
                source_type = Source.sourceManager.get(sno=current_type)
                sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id)
            elif current_type == '-1':
                sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, cno=current_course, title__contains=key_word)
            else:
                source_type = Source.sourceManager.get(sno=current_type)
                sources = StagingFile.stagingFileManager.filter(isDelete=False, dno=major_id, cno=current_course, sno=source_type, title__contains=key_word)
        else: #把status当做已知，考虑course, type
            sources = judge_base_on_status(current_course, current_type, sources, major_id, current_status)
            sources = sources.filter(title__contains=key_word)
    
    totalCount = len(sources)
    split_page(sources, current_page, page_size, start_index, totalCount, result, is_staging)
    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'sources': result,
            'total': totalCount
        }
    }))


from .convert2pdf import word2pdf_entrance, excel2pdf_entrance, ppt2pdf_entrance
# 上传的资源预览
def preview_staging_source(request):
    source_id = request.GET.get('id')
    source_link = request.GET.get('link')
    source_name = request.GET.get('name')
    # 先到文件夹中查看是否存在缓存，有就直接返回
    target_staging_pdfs = StagingConvertPDF.stagingConvertPDFManager.filter(isDelete=False, staging_pdf_name=source_name)
    if len(target_staging_pdfs) > 0:
        return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'preview_link': target_staging_pdfs[0].staging_pdf_path
        }
    }))
    
    source_exact_path = settings.BASE_DIR + source_link
    
    suffix = os.path.splitext(source_link)[1]
    preview_url = ''
    if suffix == '.pptx' or suffix == '.ppt':
        preview_url = ppt2pdf_entrance(source_exact_path, settings.BASE_DIR)
    elif suffix == '.docx' or suffix == '.doc':
        preview_url = word2pdf_entrance(source_exact_path, settings.BASE_DIR)
    elif suffix == '.xls' or suffix == '.xlsx':
        preview_url = excel2pdf_entrance(source_exact_path, settings.BASE_DIR)

    stagingConvertedPDF = StagingConvertPDF.stagingConvertPDFManager.createStagingConvertPDF(preview_url, source_name)
    stagingConvertedPDF.save()

    return HttpResponse(json.dumps({
        'code': 20000,
        'data':{
            'preview_link': preview_url
        }
    }))