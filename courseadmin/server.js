const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const jwt = require("json-web-token");
const multer = require("multer");
const path = require('path')
const storage = multer.diskStorage({
  destination:function(req, file, cb){
    cb(null, './uploads/')
  },
  filename:function(req, file, cb){
    let suffix = file.originalname.substring(file.originalname.lastIndexOf('.'));
    cb(null, Date.now()+suffix)
  }
})
const upload = multer({storage: storage});
const app = express();
const url = "https://api.github.com/users";

app.use('/uploads', express.static(path.join(__dirname,'./uploads/')));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Content-Type,  x-token");
  if (req.method == "OPTIONS") {
    res.header(
      "Access-Control-Allow-Methods",
      "PUT, GET, POST, DELETE, OPTIONS"
    );
    return res.status(200).json({});
  }
  next();
});
app.post("/coursemanage/user/login", (req, res, next) => {
  jwt.encode("Mocking", req.body.username, (err, token) => {
    if (err) return res.json({ code: 0, data: { message: "Internal Error" } });
    res.json({ code: 20000, data: { token: token } });
    next();
  });
});
app.get("/coursemanage/user/info", (req, res, next) => {
  jwt.decode("Mocking", req.query.token, (err, token) => {
    if (err) return res.json({ code: 0, data: { message: "Internal Error" } });
    res.json({
      code: 20000,
      data: {
        name: token,
        avatar:
          "https://wpimg.wallstcn.com/fb57f689-e1ab-443c-af12-8d4066e202e2.jpg?",
        roles: [token],
        id:"611530",
        teach:[{course_id:1,course_name:"数据结构"}],
        major:"计算机科学与技术"
      }
    });
    next();
  });
});
app.get("/coursemanage/public/getMajors", (req, res, next) => {
  res.json({code: 20000,data:{
    majors:[
        {title:"计算机科学与技术", major_id:'0'},
        {title:"信息技术管理", major_id:'1'},
        {title:"市场营销", major_id:'2'},
        {title:"公共事业管理", major_id:'3'},
      ]
    }
  })
});
app.get("/coursemanage/public/getCourseResources", async (req, res, next) => {
  let start = parseInt(req.query.page);
  let limit = parseInt(req.query.limit);
  console.log(req.query);
  let base = 250
  // console.log(start);
  res.json({
    code: 20000,
    data:{
      total: 20,
      courses:[
       {
        course_cover:'https://picsum.photos/seed/picsum/200/300',                
        course_name:'JavaEE程序设计',//课程名称,                
        upload_count: 5,             
        course_teacher:'肖兴江',//资源上传者 
        course_id:'1' 
      },
      {
        course_cover:'https://picsum.photos/seed/picsum/200/300',                
        course_name:'JavaEE程序设计',//课程名称,                
        upload_count: 5,             
        course_teacher:'肖兴江',//资源上传者 
        course_id:'1' 
      }
      ]
    }
  })
  next();
});
// 教师
app.get("/coursemanage/teacher/teacherCourse", async (req, res, next) => {
  console.log(req.query);
  res.json({
    code: 20000,
    data: {
      course: [
        {
          title: "算法",
          cover_link: "https://picsum.photos/400/300/?blur=1",
          course_id: "0"
        },
        {
          title: "数据结构",
          cover_link: "https://picsum.photos/400/300/?blur=1",
          course_id: "1"
        },
        {
          title: "计算机组成原理",
          cover_link: "https://picsum.photos/400/300/?blur=1",
          course_id: "2"
        },
        {
          title: "计算机网络",
          cover_link: "https://picsum.photos/400/300/?blur=1",
          course_id: "3"
        }
      ]
    }
  });
  next();
});
app.get("/coursemanage/teacher/getClasses", (req, res, next) => {
  res.json({
    code: 20000,
    data: {
      optionsGrade: [
        { label: "2016", value: "0" },
        { label: "2017", value: "1" },
        { label: "2018", value: "2" },
        { label: "2019", value: "3" }
      ],
      optionsClass: [
        { label: "计科1班", value: "0" },
        { label: "计科2班", value: "1" },
        { label: "计科3班", value: "2" },
        { label: "计科4班", value: "3" }
      ]
    }
  });
});
app.get("/coursemanage/teacher/getStudentsAtCatgories", (req, res, next) => {
  console.log(req.query);
  res.json({
    code: 20000,
    data: {
      stus: [
        {
          id: 1,
          stu_number: 12138,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Mockingjay"
        },
        {
          id: 2,
          stu_number: 9527,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Jacob"
        },
        {
          id: 3,
          stu_number: 7788,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Dragon"
        },
        {
          id: 4,
          stu_number: 1256,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Simpson"
        }
      ]
    }
  });
});

app.get("/coursemanage/teacher/getDataAtPage", (req, res, next) => {
  res.json({
    code: 20000,
    data: {
      stus: [
        {
          id: 4,
          stu_number: 1256,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Simpson"
        },
        {
          id: 3,
          stu_number: 7788,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Dragon"
        },
        {
          id: 1,
          stu_number: 12138,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Mockingjay"
        },
        {
          id: 2,
          stu_number: 9527,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Jacob"
        },
        {
          id: 2,
          stu_number: 9527,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Jacob"
        },
        {
          id: 2,
          stu_number: 9527,
          stu_grade: 2017,
          stu_class: "1",
          stu_major: "计算机科学与技术",
          name: "Jacob"
        }
      ]
    }
  });
});

app.get("/coursemanage/teacher/getSourceListType", (req, res, next) => {
  res.status(200).json({
    code: 20000,
    data: {
      listTotal: 8,
      list:[
        {
          upload_id: 0,
          upload_date: '2019-11-22',
          upload_type: '文件',
          upload_title: '课程报告',
          upload_intro: '<ol><li>测试</li></ol>',
          upload_filename: '课程报告模板',
          upload_fileLink: 'http://localhost:5000/uploads/222017602053016李斯然.doc'
        },
        {
          upload_id: 1,
          upload_date: '2019-10-12',
          upload_type: '文件',
          upload_title: '课程报告',
          upload_intro: '<ol><li>测试</li></ol>',
          upload_filename: '课程报告模板',
          upload_fileLink: 'http://localhost:5000/uploads/222017602053016李斯然.doc'
        },
        {
          upload_id: 2,
          upload_date: '2019-11-15',
          upload_type: '文件',
          upload_title: '课程报告',
          upload_intro: '<ol><li>测试</li></ol>',
          upload_filename: '课程报告模板',
          upload_fileLink: 'http://localhost:5000/uploads/222017602053016李斯然.doc'
        },
        {
          upload_id: 3,
          upload_date: '2019-09-29',
          upload_type: '文件',
          upload_title: '课程报告',
          upload_intro: '<ol><li>测试</li></ol>',
          upload_filename: '课程报告模板',
          upload_fileLink: 'http://localhost:5000/uploads/222017602053016李斯然.doc'
        },
        {
          upload_id: 4,
          upload_date: '2019-10-07',
          upload_type: '文件',
          upload_title: '课程报告',
          upload_intro: '<ol><li>测试</li></ol>',
          upload_filename: '课程报告模板',
          upload_fileLink: 'http://localhost:5000/uploads/222017602053016李斯然.doc'
        }
      ],
      types:[
        {
          label:'视频',
          value: '0'
        },
        {
          label:'文件',
          value: '1'
        },
        {
          label:'压缩包',
          value: '2'
        }
      ]
    }
  })
})

app.get("/coursemanage/teacher/getCourseDetail", (req, res, next) => {
  res.status(200).json({
    code: 20000,
    data: {
      title: 'JavaEE程序设计',
      teacher: "肖兴江",
      intro:
        "<ol><li>测试</li><ol>",
      cover:"https://picsum.photos/400/300/?blur=1"
    }
  });
});

app.post("/coursemanage/teacher/setCourseDetail",upload.single('cover'),(req, res, next) => {
  console.log(req.body);
  console.log(req.file);
  if(req.file){
    res.status(200).json({code:20000,data:{
      info: req.body,
      filePath: 'uploads/'+req.file.filename
    }});
  }else{
    res.status(200).json({code:20000,data:{
      info: req.body,
    }});
  }
})

app.post("/coursemanage/teacher/mutipleFiles", upload.any(), (req, res, next) => {
  console.log(req.files);
  console.log(req.body);
  res.status(200).json({code:20000, data:{}});
})



app.listen(5000, () => {
  console.log("Server Runing...");
});
