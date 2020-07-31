-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-07-31 11:27:54
-- 服务器版本： 5.7.28-log
-- PHP 版本： 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `ddns`
--

-- --------------------------------------------------------

--
-- 表的结构 `ddnsTodo`
--

CREATE TABLE `ddnsTodo` (
  `id` int(11) NOT NULL,
  `v4todo` json NOT NULL,
  `v6todo` json NOT NULL,
  `remark` varchar(50) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `History`
--

CREATE TABLE `History` (
  `id` int(11) NOT NULL,
  `CliId` int(11) NOT NULL,
  `ip` varchar(40) NOT NULL,
  `ipVersion` tinyint(1) UNSIGNED NOT NULL,
  `ServicerReturn` text NOT NULL,
  `Time` datetime NOT NULL,
  `Status` tinyint(1) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `ipRec`
--

CREATE TABLE `ipRec` (
  `id` int(11) NOT NULL,
  `bit1` tinyint(3) UNSIGNED NOT NULL,
  `bit2` tinyint(3) UNSIGNED NOT NULL,
  `bit3` tinyint(3) UNSIGNED NOT NULL,
  `LoginToken` varchar(64) NOT NULL,
  `remark` varchar(25) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- 转储表的索引
--

--
-- 表的索引 `ddnsTodo`
--
ALTER TABLE `ddnsTodo`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `History`
--
ALTER TABLE `History`
  ADD PRIMARY KEY (`id`),
  ADD KEY `CliId` (`CliId`),
  ADD KEY `Status` (`Status`);

--
-- 表的索引 `ipRec`
--
ALTER TABLE `ipRec`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Bits` (`bit1`,`bit2`,`bit3`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `ddnsTodo`
--
ALTER TABLE `ddnsTodo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `History`
--
ALTER TABLE `History`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `ipRec`
--
ALTER TABLE `ipRec`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
