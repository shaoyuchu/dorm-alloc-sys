import 'package:flutter/material.dart';

// Specify the name of every dormitory
const String boyDorm  = 'men_campus_dorm';
const String girlDorm = 'women_campus_dorm';
const String bot_boy  = 'men_BOT'; // 長興
const String bot_girl = 'women_BOT'; // 水源

const List<String> dataName = [boyDorm, girlDorm, bot_boy, bot_girl];

// chinese name 
const String chi_boyDorm  = '男生宿舍';
const String chi_girlDorm = '女生宿舍';
const String chi_bot_boy  = 'BOT男生宿舍'; // 長興
const String chi_bot_girl = 'BOT女生宿舍'; // 水源

const List<String> chi_dataName = [chi_boyDorm, chi_girlDorm, chi_bot_boy, chi_bot_girl];

const Map dorm_eng2chi = {
  boyDorm  : chi_boyDorm, 
  girlDorm : chi_girlDorm, 
  bot_boy  : chi_bot_boy, 
  bot_girl : chi_bot_girl
};

const Map dorm_chi2eng = {
  chi_boyDorm  : boyDorm, 
  chi_girlDorm : girlDorm, 
  chi_bot_boy  : bot_boy, 
  chi_bot_girl : bot_girl
};

// data columns
const List<String> dataColumnNames = [
  '系所代碼', 
  '系所名稱', 
  '年級', 
  '學號', 
  '姓名', 
  '性別', 
  '入學年度', 
  '身分別', 
  '身分別1', 
  '身分別2', 
  '身分別3', 
  '校內外意願', 
  '區域志願1', 
  '區域志願2', 
  '區域志願3', 
  'BOT志願1', 
  'BOT志願2', 
  'BOT志願3', 
  '戶籍地', 
  '永久地址郵遞區號', 
  '永久地址', 
  '特殊身份別', 
  '身體狀況是否爬上鋪床', 
  '是否需要安排身障房間', 
  '審查狀態', 
  '審查備注', 
  '審查人員', 
  '審查時間', 
  '身份證/護照證號', 
  '居留證號', 
  '聯絡郵件1', 
  '聯絡郵件2', 
  '國內住家電話', 
  '國外電話', 
  '手機', 
  '郵遞區號', 
  '通訊地址', 
  '聯絡人姓名', 
  '與聯絡人關係', 
  '聯絡人電話', 
  '聯絡人手機', 
  '送出時間', 
  '現住床位', 
  '最後修改', 
  '操作人員'];
