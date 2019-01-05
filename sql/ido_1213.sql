/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50716
 Source Host           : localhost
 Source Database       : ido

 Target Server Type    : MySQL
 Target Server Version : 50716
 File Encoding         : utf-8

 Date: 12/13/2018 17:32:27 PM
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Records of `admin`
-- ----------------------------
BEGIN;
INSERT INTO `admin` VALUES ('1', 'idoido', 'pbkdf2:sha256:50000$Mgzjj0y9vbzcNs6T$dad8b462d7c5277b1278411f2373073c4ec5c42e1939b2ed9bc10a1c1f6f9539', '123', '1', '1');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `event_option`
-- ----------------------------
DROP TABLE IF EXISTS `event_option`;
CREATE TABLE `event_option` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT '0' COMMENT '活动id',
  `gift_id` int(11) DEFAULT '0' COMMENT '奖品id',
  `price` bigint(11) unsigned DEFAULT '0' COMMENT '金额　 *100.兼容微信支付',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态 0删除 1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `gift`
-- ----------------------------
DROP TABLE IF EXISTS `gift`;
CREATE TABLE `gift` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT '' COMMENT '礼物名称',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态 0删除 1正常',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
