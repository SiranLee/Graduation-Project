/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : teaching_system

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 11/04/2021 11:11:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for routes
-- ----------------------------
DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `component` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `icon` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `currentPage` int(1) NULL DEFAULT NULL,
  `hidden` tinyint(1) NULL DEFAULT NULL,
  `redirect` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `props` tinyint(1) NULL DEFAULT NULL,
  `parent` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of routes
-- ----------------------------
INSERT INTO `routes` VALUES (1, '/source', 'Layout', '', '学习资源', 'resource', NULL, NULL, '/source/computer', NULL, 0);
INSERT INTO `routes` VALUES (2, 'computer', 'computer', 'computer', '计算机科学与技术', 'computer', 1, NULL, NULL, NULL, 1);
INSERT INTO `routes` VALUES (3, 'infomanage', 'infomanage', 'infomanage', '信息技术管理', 'info', 1, NULL, NULL, NULL, 1);
INSERT INTO `routes` VALUES (4, 'market', 'market', 'market', '市场营销', 'market', 1, NULL, NULL, NULL, 1);
INSERT INTO `routes` VALUES (5, 'publicmanage', 'publicmanage', 'publicmanage', '公共事业管理', 'public', 1, NULL, NULL, NULL, 1);
INSERT INTO `routes` VALUES (6, '/source/:coursename/:courseid', 'SourceDetail', 'SourceDetail', '课程资源详情', NULL, NULL, 1, NULL, 1, 1);
INSERT INTO `routes` VALUES (7, '/task', 'Layout', '', '作业管理', 'resource', NULL, NULL, '/task/uploadTask', NULL, 0);
INSERT INTO `routes` VALUES (8, 'uploadTask', 'UploadTask', 'UploadTask', '上传作业', 'upload', NULL, NULL, NULL, NULL, 7);
INSERT INTO `routes` VALUES (9, 'taskGlimpse', 'TaskGlimpse', 'TaskGlimpse', '作业成绩', 'glimpse', NULL, NULL, NULL, NULL, 7);
INSERT INTO `routes` VALUES (10, '/courseManage', 'Layout', NULL, '课程管理', 'coursemanage', NULL, NULL, NULL, 1, 0);
INSERT INTO `routes` VALUES (11, '/courseManage/index', 'CourseManage', 'CourseManage', '课程管理', 'coursemanage', NULL, NULL, NULL, NULL, 10);
INSERT INTO `routes` VALUES (12, '/detail/:course_id', 'Detail', 'Detail', '课程明细', NULL, NULL, 1, NULL, 1, 10);
INSERT INTO `routes` VALUES (13, '/create', 'Create', 'Create', '创建课程', 'add', NULL, NULL, NULL, NULL, 10);
INSERT INTO `routes` VALUES (14, '/checkTask', 'CheckTask', 'CheckTask', '批改作业', 'check', NULL, NULL, NULL, NULL, 10);
INSERT INTO `routes` VALUES (15, '/studensManage', 'Layout', NULL, '学生管理', 'students', NULL, NULL, NULL, NULL, 0);
INSERT INTO `routes` VALUES (16, '/studensManage/index', 'StudensManage', 'StudensManage', '学生管理', 'students', NULL, NULL, NULL, NULL, 15);
INSERT INTO `routes` VALUES (17, '/teachers', 'Layout', NULL, '教师管理', 'students', NULL, NULL, NULL, NULL, 0);
INSERT INTO `routes` VALUES (18, 'index', 'Teachers', 'Teachers', '教师管理', 'students', NULL, NULL, NULL, NULL, 17);
INSERT INTO `routes` VALUES (19, '/dataStatics', 'Layout', NULL, '数据统计', 'statics', NULL, NULL, NULL, NULL, 0);
INSERT INTO `routes` VALUES (20, 'index', 'DataStatics', 'DataStatics', '数据统计', 'statics', NULL, NULL, NULL, NULL, 19);
INSERT INTO `routes` VALUES (21, '/dataBackup', 'Layout', NULL, '数据备份', 'backup', NULL, NULL, NULL, NULL, 0);
INSERT INTO `routes` VALUES (22, 'index', 'dataBackup', 'dataBackup', '数据备份', 'backup', NULL, NULL, NULL, NULL, 21);
INSERT INTO `routes` VALUES (23, '/discipline', 'Layout', '', '学科管理', 'discipline', NULL, NULL, NULL, NULL, 0);
INSERT INTO `routes` VALUES (24, 'index', 'DisciplineManagement', 'DisciplineManagement', '学科管理', 'discipline', NULL, NULL, NULL, NULL, 23);
INSERT INTO `routes` VALUES (25, '/sourceCheck', 'Layout', NULL, '资源相关', 'relation', NULL, NULL, '/sourceCheck/sourceBrowse', NULL, 0);
INSERT INTO `routes` VALUES (26, 'sourceBrowse', 'SourceBrowse', 'SourceCheck', '资源总览', 'browse', NULL, NULL, NULL, NULL, 25);
INSERT INTO `routes` VALUES (27, 'sourceCheck', 'SourceCheck', 'SourceCheck', '资源审核', 'sourceCheck', NULL, NULL, NULL, NULL, 25);

SET FOREIGN_KEY_CHECKS = 1;
