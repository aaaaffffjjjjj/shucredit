-- ==============================================
-- 通信工程专业培养方案（根模块版）
-- ==============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 清空旧数据
DELETE FROM enrollment;
DELETE FROM course;
DELETE FROM module;

-- ==============================================
-- 模块定义
-- ==============================================

-- ===== 根模块 ======
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (1, '公共基础课程', 67.5, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (8, '通识课程', 8, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (9, '专业基础课程', 52, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (10, '专业必修课程', 18.5, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (11, '专业选修课程', 4, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (12, '个性化教育课程', 10, NULL);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (14, '专业方向模块', 10, NULL);

-- ===== 子模块 ======
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (2, '思政类', 18.5, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (3, '军体类', 9, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (4, '大学英语', 8, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (5, '人工智能类', 5, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (6, '国家安全教育', 1, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (7, '自然科学类', 26, 1);
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (13, '创新创业实践', 10, 12);

-- ==============================================
-- 课程定义
-- ==============================================

-- ===== 思政类 =====
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (100, 'GBK2000001', '形势与政策', 1.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (101, 'GBK2000003', '思想道德与法治', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (102, 'GBK2000004', '中国近现代史纲要', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (103, 'GBK2000002', '形势与政策（实践）', 1.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (104, 'GBK2000005', '马克思主义基本原理', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (105, 'GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, 2);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (106, 'GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, 2);

-- ===== 军体类 =====
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (107, 'GBK5100001', '军事技能', 2.0, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (108, 'GBK2000008', '军事理论', 2.0, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (109, 'GBK2800501', '体质健康促进（1）', 0.5, 3);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (110, 'GBK2800701', '体质健康促进（2）', 0.5, 3);

-- ===== 人工智能类 =====
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (111, 'GBK1200001', '程序设计（C语言）', 3.0, 5);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (112, 'GBK1200005', '人工智能基础A', 2.0, 5);

-- ===== 国家安全教育 =====
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (113, 'GBK2000009', '国家安全教育', 1.0, 6);

-- ===== 自然科学类 =====
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (114, 'GBK0101001', '高等数学A（1）', 5.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (115, 'GBK0101002', '高等数学A（2）', 5.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (116, 'GBK0103001', '大学物理A（1）', 4.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (117, 'GBK0103002', '大学物理A（2）', 4.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (118, 'GBK0103003', '大学物理实验A（1）', 1.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (119, 'GBK0103004', '大学物理实验A（2）', 1.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (120, 'GBK0104001', '大学化学', 2.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (121, 'GBK0104002', '大学化学实验', 1.0, 7);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (122, 'GBK0101006', '线性代数', 3.0, 7);

-- ===== 专业基础课程 =====
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (123, 'JBK1300001', '工程图学', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (124, 'JBK5400003', '工程实践B', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (125, 'JBK1131001', '复变函数与积分变换', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (126, 'JBK1131002', '电路与电子线路基础（1）', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (127, 'JBK1131003', '电路与电子线路基础（2）', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (128, 'JBK1131004', '电路与电子线路基础实验（1）', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (129, 'JBK1131005', '电路与电子线路基础实验（2）', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (130, 'JBK1131006', '信号与系统（1）', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (131, 'JBK1300001', '工程图学', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (132, 'JBK5400003', '工程实践B', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (133, 'JBK1131001', '复变函数与积分变换', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (134, 'JBK1131002', '电路与电子线路基础（1）', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (135, 'JBK1131004', '电路与电子线路基础实验（1）', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (136, 'JBK1131003', '电路与电子线路基础（2）', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (137, 'JBK1131005', '电路与电子线路基础实验（2）', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (138, 'JBK1131006', '信号与系统（1）', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (139, 'JBK1131007', '信号与系统（2）', 2.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (140, 'JBK1131008', '信号与系统实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (141, 'JBK1131012', '数字逻辑电路分析与设计', 4.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (142, 'JBK1131013', '数字逻辑电路分析与设计实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (143, 'JBK1131009', '面向对象程序设计', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (144, 'JBK1131011', '概率论与随机过程', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (145, 'JBK1131010', '微机原理', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (146, 'JBK1131015', '数字信号处理', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (147, 'JBK1131016', '数据结构与算法基础', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (148, 'JBK1131017', '电磁场理论', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (149, 'JBK1131018', '通信原理A', 3.0, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (150, 'JBK1131020', '通信原理实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (151, 'JBK1131021', '计算机网络', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (152, 'JBK1131022', '信息论与编码', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (153, 'JBK1131023', '通信电子线路', 2.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (154, 'JBK1131024', '通信电子线路实验', 0.5, 9);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (155, 'JBK1131014', '工程经济学与IT项目管理', 1.0, 9);

SET FOREIGN_KEY_CHECKS = 1;