-- ============================================
-- 为 student 表添加 major_id 字段
-- ============================================

SET FOREIGN_KEY_CHECKS = 0;

-- 为 student 表添加 major_id 列
ALTER TABLE student ADD COLUMN major_id INT;
ALTER TABLE student ADD CONSTRAINT fk_student_major FOREIGN KEY (major_id) REFERENCES major(id);

SET FOREIGN_KEY_CHECKS = 1;
