/*
 Navicat Premium Data Transfer

 Source Server         : cars04_local_root
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost
 Source Database       : ido

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : utf-8

 Date: 01/02/2019 08:49:15 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `address`
-- ----------------------------
DROP TABLE IF EXISTS `address`;
CREATE TABLE `address` (
  `id` bigint(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(11) DEFAULT '0' COMMENT '用户id',
  `name` varchar(128) DEFAULT '' COMMENT '昵称',
  `phone` varchar(16) DEFAULT '' COMMENT '手机',
  `province` varchar(64) DEFAULT '' COMMENT '省',
  `country` varchar(64) DEFAULT '' COMMENT '市',
  `city` varchar(64) DEFAULT '' COMMENT '区',
  `street` varchar(512) DEFAULT '' COMMENT '街道',
  `is_default` tinyint(1) DEFAULT '0' COMMENT '是否默认 0非默认 1默认',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 1正常 0 删除',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Table structure for `admin`
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT '',
  `password` varchar(255) DEFAULT '',
  `authtoken` varchar(127) DEFAULT '' COMMENT 'wechat_authtoken',
  `role` tinyint(1) DEFAULT '0',
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Records of `admin`
-- ----------------------------
BEGIN;
INSERT INTO `admin` VALUES ('1', 'idoido', 'pbkdf2:sha256:50000$2KbqlsJHoCny0CTn$6ee5f5cccc8c5e0fc545ab3df3216045dfa93f4d575e8fe5bd1bb4767d90f3c5', '123', '1', '1');
COMMIT;

-- ----------------------------
--  Table structure for `donation_record`
-- ----------------------------
DROP TABLE IF EXISTS `donation_record`;
CREATE TABLE `donation_record` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT '0' COMMENT '用户id',
  `event_id` int(11) DEFAULT '0' COMMENT '活动id',
  `event_option_id` int(11) DEFAULT '0' COMMENT '活动选项id',
  `gift_id` int(11) DEFAULT '0' COMMENT '实物id',
  `address_id` int(11) DEFAULT '0' COMMENT '地址id',
  `price` bigint(11) unsigned DEFAULT '0' COMMENT '金额　 *100.兼容微信支付',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 0删除 1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Table structure for `event`
-- ----------------------------
DROP TABLE IF EXISTS `event`;
CREATE TABLE `event` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT '' COMMENT '活动名称',
  `cover` varchar(2000) DEFAULT '' COMMENT '封面图',
  `summary` text COMMENT '详情',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 0删除 1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Records of `event`
-- ----------------------------
BEGIN;
INSERT INTO `event` VALUES ('1', '祝福青海心心相映321', '/upload/2018-12-31/1546257677.jpg', '<p>\n\n色分</p><p><u>发广</u>告</p><p><img src=\"http://localhost:7878/static/upload/2018-12-31/1546257666.jpg\"><br></p><p>32<span style=\"background-color: rgb(0, 255, 0); font-size: 18px;\">3</span>23 </p><p><img src=\"http://localhost:7878/static/upload/2018-12-31/1546257633.jpg\"><br></p>', '1', '2018-12-23 19:29:06'), ('2', '海拉尔花捐赠123', '/upload/2018-12-31/1546188708.jpg,/upload/2018-12-31/1546188709.jpg,/upload/2018-12-31/1546188710.jpg', '234', '1', '2018-12-23 19:29:33'), ('3', '444', '/upload/2018-12-31/1546188837.jpg', '222', '1', '2018-12-23 20:33:48');
COMMIT;

-- ----------------------------
--  Table structure for `event_option`
-- ----------------------------
DROP TABLE IF EXISTS `event_option`;
CREATE TABLE `event_option` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT '0' COMMENT '活动id',
  `gift_id` int(11) DEFAULT '0' COMMENT '奖品id',
  `price` decimal(9,2) unsigned DEFAULT '0.00' COMMENT '金额　 *100.兼容微信支付',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态 0删除 1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Records of `event_option`
-- ----------------------------
BEGIN;
INSERT INTO `event_option` VALUES ('1', '1', '0', '1.00', '1', '2018-12-23 19:55:28'), ('2', '1', '0', '5.00', '1', '2018-12-23 19:55:37'), ('3', '1', '6', '50.00', '1', '2018-12-23 19:55:47'), ('4', '1', '3', '500.00', '1', '2018-12-23 19:55:53'), ('5', '1', '7', '1000.00', '1', '2018-12-30 01:31:51'), ('6', '1', '1', '5000.00', '1', '2018-12-30 01:32:37'), ('7', '2', '4', '1.00', '1', '2018-12-30 01:32:48'), ('8', '2', '3', '0.10', '1', '2018-12-30 01:32:55'), ('9', '2', '0', '5.00', '1', '2018-12-30 01:35:18'), ('10', '2', '7', '3.00', '1', '2018-12-30 01:35:25'), ('11', '3', '0', '1.00', '1', '2018-12-30 01:35:55'), ('12', '3', '0', '5.00', '1', '2018-12-30 01:35:59'), ('13', '3', '4', '50.00', '1', '2018-12-30 01:36:06'), ('14', '3', '3', '100.00', '1', '2018-12-30 01:36:13');
COMMIT;

-- ----------------------------
--  Table structure for `gift`
-- ----------------------------
DROP TABLE IF EXISTS `gift`;
CREATE TABLE `gift` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT '' COMMENT '礼物名称',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 0删除 1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Records of `gift`
-- ----------------------------
BEGIN;
INSERT INTO `gift` VALUES ('1', '奥迪', '1', '2018-12-18 23:25:42'), ('2', '奔驰', '1', '2018-12-18 23:25:43'), ('3', '宝马', '1', '2018-12-18 23:25:45'), ('4', '本田', '1', '2018-12-18 23:25:48'), ('5', '尼桑', '1', '2018-12-23 18:28:55'), ('6', '凯迪拉克', '1', '2018-12-23 20:32:07'), ('7', '丰田', '1', '2018-12-23 20:32:58');
COMMIT;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `open_id` varchar(128) DEFAULT '',
  `union_id` varchar(128) DEFAULT '',
  `nickname` varchar(128) DEFAULT '' COMMENT '昵称',
  `sex` smallint(1) DEFAULT '0' COMMENT '0保密 1男 2女',
  `avatar` varchar(128) DEFAULT '' COMMENT '头像',
  `province` varchar(64) DEFAULT '' COMMENT '省',
  `country` varchar(64) DEFAULT '' COMMENT '市',
  `city` varchar(64) DEFAULT '' COMMENT '区',
  `phone` varchar(16) DEFAULT '' COMMENT '手机号',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 1正常 0 删除',
  `reg_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', '', '', '用户1', '0', '', '北京', '北京', '海淀区', '', '1', '2018-12-23 18:38:18'), ('2', '', '', '用户2', '1', '', '日本', '秋名山', '山岭', '', '1', '2018-12-23 18:38:19'), ('3', '', '', '用户3', '1', '', '河北', '保定', '张家湾', '', '1', '2018-12-23 18:38:21'), ('4', '', '', '用户4', '2', '', '', '', '', '', '1', '2018-12-23 18:38:22'), ('5', '', '', '用户5', '0', '', '', '', '', '', '1', '2018-12-23 18:38:24'), ('6', '', '', '用户6', '2', '', '', '', '', '', '1', '2018-12-23 18:38:26'), ('7', '', '', '用户7', '1', '', '', '', '', '', '1', '2018-12-23 18:38:27'), ('8', '', '', '用户8', '0', '', '', '', '', '', '0', '2018-12-23 18:38:29'), ('9', '', '', '用户9', '2', '', '', '', '', '', '0', '2018-12-23 18:38:30'), ('10', '', '', '用户10', '0', '', '', '', '', '', '1', '2018-12-23 18:38:32');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
