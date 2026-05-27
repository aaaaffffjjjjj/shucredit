-- ==============================================
-- 通信工程专业培养方案（完美分类版）
-- ==============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 清空旧数据
DELETE FROM course WHERE course_code LIKE 'GBK%' OR course_code LIKE 'JBK%';
DELETE FROM module WHERE id >= 200;

-- 根模块
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (200, '通信工程毕业要求', 160, NULL);

-- ===== 公共基础课程 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (201, '公共基础课程', 67.5, 200);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (202, '思政类', 18.5, 201);
-- 思政类 的课程
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3000, 'GBK2000001', '形势与政策', 1.0, 202);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3001, 'GBK2000003', '思想道德与法治', 3.0, 202);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3002, 'GBK2000004', '中国近现代史纲要', 3.0, 202);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3003, 'GBK2000002', '形势与政策（实践）', 1.0, 202);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3004, 'GBK2000005', '马克思主义基本原理', 3.0, 202);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3005, 'GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, 202);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3006, 'GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, 202);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (203, '军体类', 9, 201);
-- 军体类 的课程
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3007, 'GBK5100001', '军事技能', 2.0, 203);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3008, 'GBK2000008', '军事理论', 2.0, 203);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3009, 'GBK2800501', '体质健康促进（1）', 0.5, 203);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3010, 'GBK2800701', '体质健康促进（2）', 0.5, 203);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (204, '大学英语', 8, 201);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (205, '人工智能类', 5, 201);
-- 人工智能类 的课程
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3011, 'GBK1200001', '程序设计（C语言）', 3.0, 205);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3012, 'GBK1200005', '人工智能基础A', 2.0, 205);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (206, '国家安全教育', 1, 201);
-- 国家安全教育 的课程
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3013, 'GBK2000009', '国家安全教育', 1.0, 206);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (207, '自然科学类', 26, 201);
-- 自然科学类 的课程
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3014, 'GBK0101001', '高等数学A（1）', 5.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3015, 'GBK0101002', '高等数学A（2）', 5.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3016, 'GBK0103001', '大学物理A（1）', 4.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3017, 'GBK0103002', '大学物理A（2）', 4.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3018, 'GBK0103003', '大学物理实验A（1）', 1.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3019, 'GBK0103004', '大学物理实验A（2）', 1.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3020, 'GBK0104001', '大学化学', 2.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3021, 'GBK0104002', '大学化学实验', 1.0, 207);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3022, 'GBK0101006', '线性代数', 3.0, 207);

-- ===== 通识课程 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (208, '通识课程', 8, 200);

-- ===== 专业基础课程 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (209, '专业基础课程', 52, 200);

-- 专业基础课程 的课程
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3023, 'JBK1300001', '工程图学', 2.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3024, 'JBK5400003', '工程实践B', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3025, 'JBK1131001', '复变函数与积分变换', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3026, 'JBK1131002', '电路与电子线路基础（1）', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3027, 'JBK1131003', '电路与电子线路基础（2）', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3028, 'JBK1131004', '电路与电子线路基础实验（1）', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3029, 'JBK1131005', '电路与电子线路基础实验（2）', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3030, 'JBK1131006', '信号与系统（1）', 2.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3031, 'JBK1300001', '工程图学', 2.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3032, 'JBK5400003', '工程实践B', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3033, 'JBK1131001', '复变函数与积分变换', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3034, 'JBK1131002', '电路与电子线路基础（1）', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3035, 'JBK1131004', '电路与电子线路基础实验（1）', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3036, 'JBK1131003', '电路与电子线路基础（2）', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3037, 'JBK1131005', '电路与电子线路基础实验（2）', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3038, 'JBK1131006', '信号与系统（1）', 2.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3039, 'JBK1131007', '信号与系统（2）', 2.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3040, 'JBK1131008', '信号与系统实验', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3041, 'JBK1131012', '数字逻辑电路分析与设计', 4.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3042, 'JBK1131013', '数字逻辑电路分析与设计实验', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3043, 'JBK1131009', '面向对象程序设计', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3044, 'JBK1131011', '概率论与随机过程', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3045, 'JBK1131010', '微机原理', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3046, 'JBK1131015', '数字信号处理', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3047, 'JBK1131016', '数据结构与算法基础', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3048, 'JBK1131017', '电磁场理论', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3049, 'JBK1131018', '通信原理A', 3.0, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3050, 'JBK1131020', '通信原理实验', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3051, 'JBK1131021', '计算机网络', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3052, 'JBK1131022', '信息论与编码', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3053, 'JBK1131023', '通信电子线路', 2.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3054, 'JBK1131024', '通信电子线路实验', 0.5, 209);
INSERT INTO course (id, course_code, name, credit, module_id) VALUES 
  (3055, 'JBK1131014', '工程经济学与IT项目管理', 1.0, 209);

-- ===== 专业必修课程 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (210, '专业必修课程', 18.5, 200);

-- ===== 专业选修课程 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (211, '专业选修课程', 4, 200);

-- ===== 个性化教育课程 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (212, '个性化教育课程', 10, 200);

INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (213, '创新创业实践', 10, 212);

-- ===== 专业方向模块 =====
INSERT INTO module (id, name, required_credits, parent_id) VALUES 
  (214, '专业方向模块', 10, 200);

SET FOREIGN_KEY_CHECKS = 1;