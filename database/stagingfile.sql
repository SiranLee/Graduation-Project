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

 Date: 14/04/2021 17:59:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stagingfile
-- ----------------------------
DROP TABLE IF EXISTS `stagingfile`;
CREATE TABLE `stagingfile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `up_time` datetime(6) NOT NULL,
  `url` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `filename` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `isDelete` tinyint(255) NOT NULL,
  `fileDes` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fileStatus` tinyint(1) NOT NULL,
  `not_available2all` tinyint(1) NOT NULL,
  `cno_id` int(11) NOT NULL,
  `tno_id` int(11) NOT NULL,
  `sno_id` int(11) NOT NULL,
  `dno_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `stagingfile_fk_cno`(`cno_id`) USING BTREE,
  INDEX `stagingfile_fk_sno`(`sno_id`) USING BTREE,
  INDEX `stagingfile_fk_dno`(`dno_id`) USING BTREE,
  INDEX `stagingfile_fk_tno`(`tno_id`) USING BTREE,
  CONSTRAINT `stagingfile_fk_cno` FOREIGN KEY (`cno_id`) REFERENCES `course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `stagingfile_fk_dno` FOREIGN KEY (`dno_id`) REFERENCES `department` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `stagingfile_fk_tno` FOREIGN KEY (`tno_id`) REFERENCES `teacher` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `stagingfile_fk_sno` FOREIGN KEY (`sno_id`) REFERENCES `source` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of stagingfile
-- ----------------------------
INSERT INTO `stagingfile` VALUES (2, '2021-04-14 09:22:30.252101', '/upfile/stagingSource/earth.jpg', '测试staging图片', 'earth.jpg', 0, '<ol><li>绝对不意气用事</li><li>绝对不漏判任何一件坏事</li><li>绝对裁判得公正漂亮</li></ol>', 1, 1, 42, 122, 3, 1);
INSERT INTO `stagingfile` VALUES (3, '2021-04-14 09:49:22.244136', '/upfile/stagingSource/操作系统简答.doc', '测试staging文件', '操作系统简答.doc', 0, '<p>无</p>', 1, 0, 42, 122, 2, 1);

SET FOREIGN_KEY_CHECKS = 1;
