-- ==============================================
-- 2025通信工程专业培养方案数据库
-- ==============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 清空旧数据
DELETE FROM enrollment;
DELETE FROM course;
DELETE FROM module;

-- ==============================================
-- 插入模块
-- ==============================================

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (1, '公共基础课程', 67.5, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (2, '思政类', 18.5, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (3, '军体类', 9.0, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (4, '大学英语', 8.0, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (5, '人工智能类', 5.0, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (6, '国家安全教育', 1.0, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (7, '自然科学类', 26.0, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (8, '通识课程', 8.0, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (15, '核心通识课', 2.0, 8);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (16, '跨类通识课', 2.0, 8);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (17, '其他通识课', 4.0, 8);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (9, '专业基础课程', 52.0, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (10, '专业必修课程', 18.5, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (11, '专业选修课程', 4.0, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (18, '专业选修子模块1', 2.0, 11);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (19, '专业选修子模块2', 2.0, 11);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (12, '个性化教育课程', 10.0, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (13, '综合工程实践能力培养模块', 10.0, 12);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (14, '专业方向模块', 10.0, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (20, '通信方向', 4.0, 14);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (21, '光通信方向', 4.0, 14);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (22, 'AI方向', 2.0, 14);

-- ==============================================
-- 插入课程
-- ==============================================

INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (100, 'GBK200001', '形势与政策', 1.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (101, 'GBK200002', '思想道德与法治', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (102, 'GBK200003', '中国近现代史纲要', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (103, 'GBK200004', '形势与政策(实践)', 1.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (104, 'GBK200005', '马克思主义基本原理', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (105, 'GBK200006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (106, 'GBK200007', '习近平新时代中国特色社会主义思想概论', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (107, 'GBK510001', '军事技能', 2.0, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (108, 'GBK200008', '军事理论', 2.0, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (109, 'GBK280071', '体质健康促进(1)', 0.5, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (110, 'GBK280072', '体质健康促进(2)', 0.5, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (111, 'GBK130001', '大学英语(1)', 2.0, 4);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (112, 'GBK130002', '大学英语(2)', 2.0, 4);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (113, 'GBK130003', '大学英语(3)', 2.0, 4);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (114, 'GBK130004', '大学英语(4)', 2.0, 4);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (115, 'GBK120001', '程序设计(C语言)', 3.0, 5);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (116, 'GBK120002', '人工智能基础A', 2.0, 5);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (117, 'GBK200009', '国家安全教育', 1.0, 6);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (118, 'GBK010101', '高等数学A(1)', 5.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (119, 'GBK010102', '高等数学A(2)', 5.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (120, 'GBK010301', '大学物理A(1)', 4.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (121, 'GBK010302', '大学物理A(2)', 4.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (122, 'GBK010303', '大学物理实验A(1)', 1.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (123, 'GBK010304', '大学物理实验A(2)', 1.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (124, 'GBK010401', '大学化学', 2.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (125, 'GBK010402', '大学化学实验', 1.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (126, 'GBK010103', '线性代数', 3.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (127, 'JBK130001', '工程图学', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (128, 'JBK540001', '工程实践B', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (129, 'JBK113101', '信号与系统(1)', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (130, 'JBK113102', '电路与电子线路基础(1)', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (131, 'JBK113103', '复变函数与积分变换', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (132, 'JBK113104', '面向对象程序设计', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (133, 'JBK113105', '电路与电子线路基础实验(1)', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (134, 'JBK113106', '数字逻辑电路分析与设计', 4.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (135, 'JBK113107', '电路与电子线路基础实验(2)', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (136, 'JBK113108', '电路与电子线路基础(2)', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (137, 'JBK113109', '概率论与随机过程', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (138, 'JBK113110', '微机原理', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (139, 'JBK113111', '数字逻辑电路分析与设计实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (140, 'JBK113112', '信号与系统实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (141, 'JBK113113', '信号与系统(2)', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (142, 'JBK113114', '工程经济学与IT项目管理', 1.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (143, 'JBK113115', '数字信号处理', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (144, 'JBK113116', '数据结构与算法基础', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (145, 'JBK113117', '电磁场理论', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (146, 'JBK113118', '通信原理A', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (147, 'JBK113119', '计算机网络', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (148, 'JBK113120', '信息论与编码', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (149, 'JBK113121', '通信电子线路', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (150, 'JBK113122', '通信电子线路实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (151, 'JBK113123', '通信原理实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (152, 'BBK113101', '认识实习', 0.5, 10);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (153, 'BBK113102', '工程教育', 2.0, 10);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (154, 'BBK113103', '综合工程设计', 3.0, 10);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (155, 'BBK113104', '生产实习', 5.0, 10);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (156, 'BBK113105', '毕业论文(设计)', 8.0, 10);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (157, 'XBK113101', '电磁波开发的得与失', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (158, 'XBK113102', '认识物联网', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (159, 'XBK113103', '面向复杂对象的可测性设计与故障容错设计', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (160, 'XBK113001', '智能信息感知与识别', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (161, 'XBK113002', '科技写作与交流', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (162, 'XBK113003', '电生理技术的应用', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (163, 'XBK113104', '现代光通信网和无线通信技术', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (164, 'XBK113105', '5G物联网时代的光纤接入技术', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (165, 'XBK113106', '信息科技前沿与发展前景', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (166, 'XBK113004', '从傅里叶分析到小波分析', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (167, 'XBK113005', '多媒体信息安全', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (168, 'XBK113006', '智能视觉信息处理技术', 2.0, 18);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (169, 'XBK113107', '科技英语', 2.0, 19);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (170, 'XBK113108', '信息科技前瞻', 2.0, 19);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (171, 'XBK113109', '嵌入式系统设计基础', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (172, 'XBK113110', '天线工程自动设计原理', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (173, 'XBK113007', '网络程序设计', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (174, 'XBK113111', '嵌入式系统项目设计', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (175, 'XBK113112', '射频电路设计', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (176, 'XBK113113', '信息安全理论与应用', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (177, 'XBK113114', '物联网技术', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (178, 'XBK113115', '多媒体技术与通信', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (179, 'XBK113008', '超大规模集成电路设计', 2.0, 13);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (180, 'XBK113116', '宽带无线通信技术', 2.0, 20);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (181, 'XBK113117', '微波技术', 2.0, 20);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (182, 'XBK113118', '通信天线', 2.0, 20);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (183, 'XBK113119', '移动通信', 2.0, 20);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (184, 'XBK113120', '光子学基础', 2.0, 21);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (185, 'XBK113121', '光电信息技术', 2.0, 21);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (186, 'XBK113122', '宽带光网络', 2.0, 21);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (187, 'XBK113123', '现代信息光子技术', 2.0, 21);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (188, 'XBK113124', '数字图像处理A', 2.0, 22);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (189, 'XBK113125', '神经网络与深度学习', 2.0, 22);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (190, 'XBK113009', '机器学习', 2.0, 22);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (191, 'XBK113126', '自然语言处理', 2.0, 22);

SET FOREIGN_KEY_CHECKS = 1;

-- ==============================================
-- 完成!
-- ==============================================