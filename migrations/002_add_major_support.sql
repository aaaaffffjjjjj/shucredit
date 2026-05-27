-- ============================================
-- 专业层级支持 - 数据库迁移脚本
-- 执行方式: mysql -u root -p student_system < migrations/002_add_major_support.sql
-- ============================================

SET FOREIGN_KEY_CHECKS = 0;

-- 1. 创建专业表
CREATE TABLE IF NOT EXISTS major (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50),
    college_id INT NOT NULL,
    FOREIGN KEY (college_id) REFERENCES college(id),
    UNIQUE KEY uk_college_major (college_id, name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 为 module 表添加 major_id 列（可选，优先使用 major_id，兼容 college_id）
ALTER TABLE module ADD COLUMN major_id INT;
ALTER TABLE module ADD CONSTRAINT fk_module_major FOREIGN KEY (major_id) REFERENCES major(id);

-- 3. 修改 college 表的 code 为更规范的（可选）
-- 保持现有结构

SET FOREIGN_KEY_CHECKS = 1;
