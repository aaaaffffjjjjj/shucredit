-- ============================================
-- 多学院培养方案支持 - 数据库迁移脚本
-- 执行方式: mysql -u root -p student_system < migrations/001_add_college_support.sql
-- ============================================

SET FOREIGN_KEY_CHECKS = 0;

-- 1. 创建学院表
CREATE TABLE IF NOT EXISTS college (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 插入 28 个学院（幂等：使用 IGNORE 或先检查）
INSERT IGNORE INTO college (name, code) VALUES
    ('理学院', 'science'),
    ('微电子学院', 'microelectronics'),
    ('力学与工程科学学院', 'mechanics'),
    ('文学院', 'literature'),
    ('社会学院', 'sociology'),
    ('外国语学院', 'foreign_lang'),
    ('经济学院', 'economics'),
    ('管理学院', 'management'),
    ('文化遗产与信息管理学院', 'cultural_heritage'),
    ('法学院', 'law'),
    ('通信与信息工程学院', 'communication'),
    ('翔英学院', 'xiangying'),
    ('计算机工程与科学学院', 'cs'),
    ('机电工程与自动化学院', 'mechatronics'),
    ('材料科学与工程学院', 'materials'),
    ('环境与化学工程学院', 'env_chem'),
    ('生命科学学院', 'life_science'),
    ('上海美术学院', 'fine_arts'),
    ('上海电影学院', 'film'),
    ('新闻传播学院', 'journalism'),
    ('马克思主义学院', 'marxism'),
    ('国际教育学院', 'intl_edu'),
    ('钱伟长学院', 'qwc'),
    ('悉尼工商学院', 'sydney_business'),
    ('中欧工程技术学院', 'ceeu'),
    ('音乐学院', 'music'),
    ('里斯本学院', 'lisbon'),
    ('未来技术学院', 'future_tech');

-- 3. 获取通信学院 ID
SET @comm_id = (SELECT id FROM college WHERE code = 'communication' LIMIT 1);

-- 4. 为 module 表添加 college_id 列（如果尚未添加）
--    注意：如已存在此列请注释掉下面两行
ALTER TABLE module ADD COLUMN college_id INT NOT NULL DEFAULT 1;
ALTER TABLE module ADD CONSTRAINT fk_module_college FOREIGN KEY (college_id) REFERENCES college(id);

-- 5. 为 student 表添加 college_id 列（如果尚未添加）
ALTER TABLE student ADD COLUMN college_id INT;
ALTER TABLE student ADD CONSTRAINT fk_student_college FOREIGN KEY (college_id) REFERENCES college(id);

-- 6. 将现有通信学院的模块数据关联到通信学院
UPDATE module SET college_id = @comm_id WHERE college_id = 1 OR college_id IS NULL;

-- 7. 将现有学生关联到通信学院
UPDATE student SET college_id = @comm_id WHERE college_id IS NULL;

SET FOREIGN_KEY_CHECKS = 1;