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

 Date: 11/04/2021 11:11:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin_routes_map
-- ----------------------------
DROP TABLE IF EXISTS `admin_routes_map`;
CREATE TABLE `admin_routes_map`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NULL DEFAULT NULL,
  `route_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `admin`(`admin_id`) USING BTREE,
  INDEX `route`(`route_id`) USING BTREE,
  CONSTRAINT `admin` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `route` FOREIGN KEY (`route_id`) REFERENCES `routes` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_routes_map
-- ----------------------------
INSERT INTO `admin_routes_map` VALUES (1, 1, 1);
INSERT INTO `admin_routes_map` VALUES (2, 1, 2);
INSERT INTO `admin_routes_map` VALUES (3, 1, 3);
INSERT INTO `admin_routes_map` VALUES (4, 1, 4);
INSERT INTO `admin_routes_map` VALUES (5, 1, 5);
INSERT INTO `admin_routes_map` VALUES (6, 1, 6);
INSERT INTO `admin_routes_map` VALUES (7, 1, 17);
INSERT INTO `admin_routes_map` VALUES (8, 1, 18);
INSERT INTO `admin_routes_map` VALUES (9, 1, 19);
INSERT INTO `admin_routes_map` VALUES (10, 1, 20);
INSERT INTO `admin_routes_map` VALUES (11, 1, 21);
INSERT INTO `admin_routes_map` VALUES (12, 1, 22);
INSERT INTO `admin_routes_map` VALUES (13, 1, 23);
INSERT INTO `admin_routes_map` VALUES (14, 1, 24);
INSERT INTO `admin_routes_map` VALUES (15, 1, 25);
INSERT INTO `admin_routes_map` VALUES (16, 1, 26);
INSERT INTO `admin_routes_map` VALUES (17, 1, 27);

SET FOREIGN_KEY_CHECKS = 1;
