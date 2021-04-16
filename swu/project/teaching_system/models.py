from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
import time
from .storage import mystorage

# Create your models here.
#1、教师
class TeacherManager(models.Manager):
    def get_queryset(self):
        return super(TeacherManager, self).get_queryset().filter(isDelete=False)
    def createTeacher(self, tno, tname, image, botany, password, email, department, isDelete=False):
        teacher = self.model()
        #print(type(grade))
        teacher.tno = tno
        teacher.tname = tname
        teacher.image = image
        teacher.botany = botany
        teacher.password = password
        teacher.email = email
        teacher.department = department
        teacher.isDelete = isDelete
        return teacher

class Teacher(models.Model):
    teacherManage = TeacherManager()
    tno = models.CharField(max_length=10, unique=True)
    tname = models.CharField(max_length=16)
    image = models.TextField()
    botany = models.CharField(max_length=24)
    password = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    isDelete = models.BooleanField(default=False)
    #所在系部
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    class Meta:
        db_table = "teacher"

#2、系部
class DepartmentManager(models.Manager):
    def get_queryset(self):
        return super(DepartmentManager, self).get_queryset().filter(isDelete=False)
    def createDepartment(self, dno, dname, isDelete=False):
        department = self.model()
        #print(type(grade))
        department.dno = dno
        department.dname = dname
        department.isDelete = isDelete
        return department

class Department(models.Model):
    departmentManage = DepartmentManager()
    dno = models.CharField(max_length=18, unique=True)
    dname = models.CharField(max_length=30)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "department"

#3、课程
class CourseManager(models.Manager):
    def get_queryset(self):
        return super(CourseManager, self).get_queryset()
    def createCourse(self, no, name, tno, dno, intro, image='', isDelete=False):
        course = self.model()
        #print(type(grade))
        course.no = no
        course.name = name
        course.image = image
        course.intro = intro
        course.tno = tno
        course.dno = dno
        course.isDelete = isDelete
        return course

class Course(models.Model):
    courseManager = CourseManager()
    no = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=39)
    image = models.TextField()
    intro = models.TextField()
    isDelete = models.BooleanField(default=False)
    tno = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    dno = models.ForeignKey('Department', on_delete=models.CASCADE)
    class Meta:
        db_table = "course"

#4、资源表
class SourceManager(models.Manager):
    def get_queryset(self):
        return super(SourceManager, self).get_queryset().filter(isDelete=False)
    def createSource(self, sno, sname, isDelete=False, stype=False):
        stu = self.model()
        #print(type(grade))
        stu.sno = sno
        stu.sname = sname
        stu.isDelete = isDelete
        stu.stype = stype
        return stu

class Source(models.Model):
    sourceManager = SourceManager()
    sno = models.CharField(max_length=10, unique=True)
    sname = models.CharField(max_length=21)
    isDelete = models.BooleanField(default=False)
    stype = models.BooleanField(default=False)
    class Meta:
        db_table = "source"

#5、资源具体内容
class FileManager(models.Manager):
    def get_queryset(self):
        return super(FileManager, self).get_queryset().filter(isDelete=False)
    def createFile(self, describe, url, title, filename, download_times, dno, not_available2all, tno, sno, no, vtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), isDelete=False):
        stu = self.model()
        #print(type(grade))
        # stu.fno = fno
        stu.describe = describe
        stu.time = vtime
        stu.url = url
        stu.title = title
        stu.filename = filename
        stu.tno = tno
        stu.sno = sno
        stu.no = no
        stu.isDelete = isDelete
        stu.download_times = download_times
        stu.dno = dno
        stu.not_available2all = not_available2all
        return stu

class File(models.Model):
    fileManager = FileManager()
    # fno = models.CharField(max_length=10, unique=True)
    describe = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    url = models.TextField()
    title = models.CharField(max_length=30)
    filename = models.TextField()
    isDelete = models.BooleanField(default=False)
    download_times = models.IntegerField(default=0)
    dno = models.CharField(max_length=10)
    # 0对应false
    not_available2all = models.BooleanField(default=False)
    tno = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    sno = models.ForeignKey('Source', on_delete=models.CASCADE)
    no = models.ForeignKey('Course', on_delete=models.CASCADE)
    class Meta:
        db_table = "file"

# 待审核资源
class StagingFileManager(models.Manager):
    def createStagingFile(self, url, title, filename, fileDes, fileStatus, not_available2all, failReason, cno, tno, sno, dno, vtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), isDelete=False):
        stagingfile = self.model()
        stagingfile.up_time = vtime
        stagingfile.url = url
        stagingfile.title = title
        stagingfile.filename = filename
        stagingfile.isDelete = isDelete
        stagingfile.fileDes = fileDes
        stagingfile.fileStatus = fileStatus
        stagingfile.not_available2all = not_available2all
        stu.failReason = failReason
        stagingfile.cno = cno
        stagingfile.sno = sno
        stagingfile.tno = tno
        stagingfile.dno = dno
        return stagingfile

class StagingFile(models.Model):
    stagingFileManager = StagingFileManager()
    up_time = models.DateTimeField(auto_now_add=True)
    url = models.TextField()
    title = models.CharField(max_length=30)
    filename = models.TextField()
    isDelete = models.BooleanField(default=False)
    fileDes = models.TextField()
    # 0: 未审核; 1: 审核中; 2: 审核通过; 3: 审核未通过
    fileStatus = models.SmallIntegerField()
    not_available2all = models.BooleanField(default=False)
    failReason = models.TextField()
    
    cno = models.ForeignKey('Course', on_delete=models.CASCADE)
    sno = models.ForeignKey('Source', on_delete=models.CASCADE)
    tno = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    dno = models.ForeignKey('department', on_delete=models.CASCADE)

    class Meta:
        db_table = "stagingfile"

class StagingConvertPDFManager(models.Manager):
    def createStagingConvertPDF(self, staging_pdf_path, staging_pdf_name, isDelete=False):
        stagingConvertPDF = self.model()
        stagingConvertPDF.isDelete = isDelete
        stagingConvertPDF.staging_pdf_path = staging_pdf_path
        stagingConvertPDF.staging_pdf_name = staging_pdf_name
        return stagingConvertPDF

class StagingConvertPDF(models.Model):
    stagingConvertPDFManager = StagingConvertPDFManager()
    isDelete = models.BooleanField(default=False)
    staging_pdf_path = models.TextField()
    staging_pdf_name = models.TextField()

    class Meta:
        db_table = "staging_convert_pdf"

#6、学生表
class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(isDelete=False)
    def createStudent(self, sno, grade, sname, image, cs, password, mclass, department, isDelete=False):
        teacher = self.model()
        #print(type(grade))
        teacher.sno = sno
        teacher.grade = grade
        teacher.sname = sname
        teacher.image = image
        teacher.cs = cs
        teacher.password = password
        # teacher.email = email
        teacher.mclass = mclass
        teacher.department = department
        teacher.isDelete = isDelete
        return teacher

class Student(models.Model):
    studentManager = StudentManager()
    sno = models.CharField(max_length=15)
    grade = models.CharField(max_length=4)
    sname = models.CharField(max_length=18)
    image = models.TextField()
    cs = models.CharField(max_length=3)
    password = models.CharField(max_length=40)
    # email = models.CharField(max_length=30)
    isDelete = models.BooleanField(default=False)
    #所在系部
    mclass = models.ForeignKey('Mclass', on_delete=models.DO_NOTHING)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)
    class Meta:
        db_table = "student"

#7、班级
class MclassManager(models.Manager):
    def get_queryset(self):
        return super(MclassManager, self).get_queryset().filter(isDelete=False)
    def createMclass(self, cno, cname, grade, department, con, isDelete=False):
        teacher = self.model()
        #print(type(grade))
        teacher.cno = cno
        teacher.cname = cname
        teacher.grade = grade
        teacher.department = department
        teacher.con = con
        teacher.isDelete = isDelete
        return teacher

class Mclass(models.Model):
    mclassManager = MclassManager()
    cno = models.CharField(max_length=30, unique=True)
    cname = models.CharField(max_length=39)
    #年级
    grade = models.CharField(max_length=6)
    isDelete = models.BooleanField(default=False)
    #所在系部
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    con = models.ForeignKey('Course', on_delete=models.CASCADE)
    class Meta:
        db_table = "mclass"


class ImageStore(models.Model):
    name = models.CharField(max_length=150, null=True)
    img = models.ImageField(upload_to='course_img')
    class Meta:
        db_table = 'ImageStore'

class StudentStore(models.Model):
    name = models.CharField(max_length=150, null=True)
    src = models.ImageField(upload_to='studentStore')
    class Meta:
        db_table = 'studentStore'

class TeacherStore(models.Model):
    name = models.CharField(max_length=150, null=True)
    src = models.FileField(upload_to='teacherStore',  storage=mystorage())
    class Meta:
        db_table = 'teacherStore'

class StudentImage(models.Model):
    name = models.CharField(max_length=150, null=True)
    src = models.ImageField(upload_to='studentImage')
    class Meta:
        db_table = 'studentImage'

class TeacherImage(models.Model):
    name = models.CharField(max_length=150, null=True)
    src = models.ImageField(upload_to='teacherImage')
    class Meta:
        db_table = 'teacherImage'

class AdminImage(models.Model):
    name = models.CharField(max_length=150, null=True)
    src = models.ImageField(upload_to='adminImage')
    class Meta:
        db_table = 'adminImage'

class AdminManager(models.Manager):
    def get_queryset(self):
        return super(AdminManager, self).get_queryset().filter(isDelete=False)
    def createAdmin(self, ano, aname, image, password, isDelete=False):
        teacher = self.model()
        #print(type(grade))
        teacher.ano = ano
        print(ano)
        teacher.aname = aname
        teacher.image = image
        teacher.password = password
        teacher.isDelete = isDelete
        return teacher

class Admin(models.Model):
    adminManage = AdminManager()
    ano = models.CharField(max_length=10, unique=True)
    aname = models.CharField(max_length=16)
    image = models.TextField()
    password = models.CharField(max_length=40)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "admin"

#在线时间表
class StudentTimeManager(models.Manager):
    def get_queryset(self):
        return super(StudentTimeManager, self).get_queryset().filter(isDelete=False)
    def createStudentTime(self, sno, timelong, time, isDelete=False):
        teacher = self.model()
        #print(type(grade))
        teacher.sno = sno
        teacher.timelong = timelong
        teacher.time = time
        teacher.isDelete = isDelete
        return teacher

class StudentTime(models.Model):
    studentTimeManager = StudentTimeManager()
    sno = models.CharField(max_length=30)
    timelong = models.FloatField()#0.5h
    time = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "studentTime"

import datetime
#记录登录
class StudentTimeNowManager(models.Manager):
    def createStudentTimeNow(self, sno, time=datetime.datetime.now()):
        teacher = self.model()
        #print(type(grade))
        teacher.sno = sno
        teacher.time = time
        return teacher

class StudentTimeNow(models.Model):
    studentTimeNowManager = StudentTimeNowManager()
    sno = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "studentTimeNow"

#发布作业
class HomeworkManager(models.Manager):
    def createHomework(self, describe, title, sno, no, vtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))):
        stu = self.model()
        #print(type(grade))
        # stu.fno = fno
        stu.describe = describe
        stu.time = vtime
        stu.title = title
        stu.sno = sno
        stu.no = no
        return stu

class Homework(models.Model):
    homeworkManager = HomeworkManager()
    # fno = models.CharField(max_length=10, unique=True)
    describe = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    sno = models.ForeignKey('Source', on_delete=models.CASCADE)
    no = models.ForeignKey('Course', on_delete=models.CASCADE)
    class Meta:
        db_table = "homework"

#具体作业
class WorkManager(models.Manager):
    def createWork(self, title, url, hno):
        stu = self.model()
        stu.title = title
        stu.url = url
        stu.hno = hno
        return stu

class Work(models.Model):
    workManager = WorkManager()
    title = models.TextField()
    url = models.TextField()
    hno = models.ForeignKey('Homework', on_delete=models.CASCADE)
    class Meta:
        db_table = "work"

#学生提交作业
class StudentWorkManager(models.Manager):
    def createStudentWork(self, student, work, score=0, status='未批改', stu_submitDate=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))):
        stu = self.model()
        stu.student = student
        stu.work = work
        stu.stu_id = student.sno
        stu.score = score
        stu.status = status
        stu.stu_submitDate = stu_submitDate
        return stu

class StudentWork(models.Model):
    studentWorkManager = StudentWorkManager()
    stu_submitDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    score = models.IntegerField()
    stu_id = models.CharField(max_length=20)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    work = models.ForeignKey('Homework', on_delete=models.CASCADE)
    class Meta:
        db_table = "studentworkManager"

#学生作业资源
class StudentWorkSourceManager(models.Manager):
    def createStudentWorkSource(self, title, url, workmanage):
        stu = self.model()
        stu.title = title
        stu.url = url
        stu.workmanage = workmanage
        return stu

class StudentWorkSource(models.Model):
    studentWorkSourceManager = StudentWorkSourceManager()
    title = models.TextField()
    url = models.TextField()

    workmanage = models.ForeignKey('StudentWork', on_delete=models.CASCADE)
    class Meta:
        db_table = "studentworksource"

class RoutesManager(models.Manager):
    def createRoutesManager(self, path, component, name, title, icon, currentPage, hidden, redirect, parent):
        manager = self.model()
        manager.path = path
        manager.component = component
        manager.name = name
        manager.title = title
        manager.icon = icon
        manager.currentPage = currentPage
        manager.hidden = hidden
        manager.redirect = redirect
        manager.parent = parent
        return manager

class Routes(models.Model):
    routeManager = RoutesManager()
    path = models.CharField(max_length=50)
    component = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    currentPage = models.IntegerField()
    hidden = models.BooleanField(default=False)
    redirect = models.CharField(max_length=50)
    props = models.BooleanField(default=False)
    parent = models.IntegerField()

    class Meta:
        db_table = "routes"

class TeacherRoutesMapManager(models.Manager):
    def createTeacherRoutesMap(self, tea_id, routes_id):
        mapper = self.model()
        mapper.tea = tea_id
        mapper.routes = routes_id
        return mapper
class TeacherRoutesMap(models.Model):
    teacherRoutesMapManager = TeacherRoutesMapManager()
    tea = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    routes = models.ForeignKey('Routes', on_delete=models.CASCADE)

    class Meta:
        db_table = "teacher_routes_map"

class AdminRoutesMapManager(models.Manager):
    def createAdminRoutesMap(self, admin_id, routes_id):
        mapper = self.model()
        mapper.admin = admin_id
        mapper.route = routes_id
        return mapper

class AdminRoutesMap(models.Model):
    adminRoutesMapManager = AdminRoutesMapManager()
    admin = models.ForeignKey('Admin', on_delete=models.CASCADE)
    route = models.ForeignKey('Routes', on_delete=models.CASCADE)
    class Meta:
        db_table = "admin_routes_map"


class StudentRoutesMapManager(models.Manager):
    def createStudentRoutesMap(self, stu_no, routes_id):
        mapper = self.model()
        mapper.stu_no = stu_no
        mapper.route_id = routes_id
        return mapper

class StudentRoutesMap(models.Model):
    studentRoutesMapManager = StudentRoutesMapManager()
    stu_no = models.CharField(max_length=50)
    route_id = models.IntegerField()
    class Meta:
        db_table = "student_routes_map"

class RouteComponentMapManager(models.Manager):
    def createRouteComponentMap(self, component_key, component_path):
        mapper = self.model()
        mapper.component_key = component_key
        mapper.component_path = component_path
        return mapper

class RouteComponentMap(models.Model):
    routeComponentMapManager = RouteComponentMapManager()
    component_key = models.CharField(max_length = 255)
    component_path = models.CharField(max_length = 255)
    class Meta:
        db_table = 'route_component'






admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Source)
admin.site.register(File)
admin.site.register(StagingFile)
admin.site.register(StagingConvertPDF)
admin.site.register(Student)
admin.site.register(Mclass)
admin.site.register(ImageStore)
admin.site.register(StudentStore)
admin.site.register(StudentImage)
admin.site.register(TeacherImage)
admin.site.register(Admin)
admin.site.register(AdminImage)
admin.site.register(StudentTime)
admin.site.register(StudentTimeNow)
admin.site.register(Homework)
admin.site.register(Work)
admin.site.register(StudentWork)
admin.site.register(StudentWorkSource)
admin.site.register(Routes)
admin.site.register(TeacherRoutesMap)
admin.site.register(AdminRoutesMap)
admin.site.register(StudentRoutesMap)