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

 Date: 15/04/2021 15:33:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for staging_convert_pdf
-- ----------------------------
DROP TABLE IF EXISTS `staging_convert_pdf`;
CREATE TABLE `staging_convert_pdf`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isDelete` tinyint(1) NOT NULL,
  `staging_pdf_path` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `staging_pdf_name` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of staging_convert_pdf
-- ----------------------------
INSERT INTO `staging_convert_pdf` VALUES (1, 0, '/upfile/stagingConvertFiles/操作系统简答.pdf', '操作系统简答.doc');
INSERT INTO `staging_convert_pdf` VALUES (2, 0, '/upfile/stagingConvertFiles/答辩.pdf', '答辩.pptx');
INSERT INTO `staging_convert_pdf` VALUES (3, 0, '', '20WEPM028.pdf');
INSERT INTO `staging_convert_pdf` VALUES (4, 0, '/upfile/stagingConvertFiles/17计科.pdf', '17计科.xls');

SET FOREIGN_KEY_CHECKS = 1;
