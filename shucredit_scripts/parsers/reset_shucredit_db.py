import pymysql
import sys
import os

# 数据库配置
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '24567@Zzy',
    'database': 'student_system',
    'charset': 'utf8mb4'
}

def reset_database():
    print("="*60)
    print("🗑️ 重置 shucredit-1 数据库（完整模块结构）")
    print("="*60)
    
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        # 禁用外键检查，彻底清空
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 1. 清空表（用DELETE而不是TRUNCATE，避免外键问题）
        print("\n📋 清空数据库...")
        
        cursor.execute("DELETE FROM enrollment")
        print(f"  - 删除 enrollment: {cursor.rowcount} 条")
        
        cursor.execute("DELETE FROM course")
        print(f"  - 删除 course: {cursor.rowcount} 条")
        
        cursor.execute("DELETE FROM module")
        print(f"  - 删除 module: {cursor.rowcount} 条")
        
        # 检查是否有user_progress表
        cursor.execute("SHOW TABLES LIKE 'user_progress'")
        if cursor.fetchone():
            cursor.execute("DELETE FROM user_progress")
            print(f"  - 删除 user_progress: {cursor.rowcount} 条")
        
        # 重置自增ID
        cursor.execute("ALTER TABLE module AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE course AUTO_INCREMENT = 100")
        
        connection.commit()
        print("✅ 数据库已完全清空")
        
        # 2. 插入完整的模块结构
        print("\n📦 插入完整模块结构...")
        modules = [
            # --- 根模块 ---
            (1, '公共基础课程', 67.5, None),
            (8, '通识课程', 8.0, None),
            (9, '专业基础课程', 52.0, None),
            (10, '专业必修课程', 18.5, None),
            (11, '专业选修课程', 4.0, None),
            (12, '个性化教育课程', 10.0, None),
            (14, '专业方向模块', 10.0, None),
            
            # --- 公共基础课程的子模块 ---
            (2, '思政类', 18.5, 1),
            (3, '军体类', 9.0, 1),
            (4, '大学英语', 8.0, 1),
            (5, '人工智能类', 5.0, 1),
            (6, '国家安全教育', 1.0, 1),
            (7, '自然科学类', 26.0, 1),
            
            # --- 通识课程的子模块 ---
            (15, '核心通识课', 2.0, 8),
            (16, '跨类通识课', 2.0, 8),
            (17, '其他通识课', 4.0, 8),
            
            # --- 专业选修课程的子模块 ---
            (18, '专业选修子模块1', 2.0, 11),
            (19, '专业选修子模块2', 2.0, 11),
            
            # --- 个性化教育课程的子模块 ---
            (13, '综合工程实践能力培养模块', 10.0, 12),
            
            # --- 专业方向模块的子模块 ---
            (20, '通信方向', 4.0, 14),
            (21, '光通信方向', 4.0, 14),
            (22, 'AI方向', 2.0, 14),
        ]
        
        for m in modules:
            parent_str = str(m[3]) if m[3] is not None else 'NULL'
            cursor.execute(f"INSERT INTO module (id, name, required_credits, parent_id) VALUES ({m[0]}, '{m[1]}', {m[2]}, {parent_str})")
        
        print(f"✅ 插入了 {len(modules)} 个模块")
        
        # 3. 插入课程（主要放在现有模块下，其他模块保持课程可扩展）
        print("\n📚 插入课程...")
        courses = [
            # --- 思政类（模块2） ---
            (100, 'GBK2000001', '形势与政策', 1.0, 2),
            (101, 'GBK2000003', '思想道德与法治', 3.0, 2),
            (102, 'GBK2000004', '中国近现代史纲要', 3.0, 2),
            (103, 'GBK2000002', '形势与政策（实践）', 1.0, 2),
            (104, 'GBK2000005', '马克思主义基本原理', 3.0, 2),
            (105, 'GBK2000006', '毛泽东思想和中国特色社会主义理论体系概论', 3.0, 2),
            (106, 'GBK2000007', '习近平新时代中国特色社会主义思想概论', 3.0, 2),
            
            # --- 军体类（模块3） ---
            (107, 'GBK5100001', '军事技能', 2.0, 3),
            (108, 'GBK2000008', '军事理论', 2.0, 3),
            (109, 'GBK2800501', '体质健康促进（1）', 0.5, 3),
            (110, 'GBK2800701', '体质健康促进（2）', 0.5, 3),
            
            # --- 人工智能类（模块5） ---
            (111, 'GBK1200001', '程序设计（C语言）', 3.0, 5),
            (112, 'GBK1200005', '人工智能基础A', 2.0, 5),
            
            # --- 国家安全教育（模块6） ---
            (113, 'GBK2000009', '国家安全教育', 1.0, 6),
            
            # --- 自然科学类（模块7） ---
            (114, 'GBK0101001', '高等数学A（1）', 5.0, 7),
            (115, 'GBK0101002', '高等数学A（2）', 5.0, 7),
            (116, 'GBK0103001', '大学物理A（1）', 4.0, 7),
            (117, 'GBK0103002', '大学物理A（2）', 4.0, 7),
            (118, 'GBK0103003', '大学物理实验A（1）', 1.0, 7),
            (119, 'GBK0103004', '大学物理实验A（2）', 1.0, 7),
            (120, 'GBK0104001', '大学化学', 2.0, 7),
            (121, 'GBK0104002', '大学化学实验', 1.0, 7),
            (122, 'GBK0101006', '线性代数', 3.0, 7),
            
            # --- 专业基础课程（模块9） ---
            (123, 'JBK1300001', '工程图学', 2.0, 9),
            (124, 'JBK5400003', '工程实践B', 3.0, 9),
            (125, 'JBK1131001', '复变函数与积分变换', 2.5, 9),
            (126, 'JBK1131002', '电路与电子线路基础（1）', 3.0, 9),
            (127, 'JBK1131003', '电路与电子线路基础（2）', 3.0, 9),
            (128, 'JBK1131004', '电路与电子线路基础实验（1）', 0.5, 9),
            (129, 'JBK1131005', '电路与电子线路基础实验（2）', 0.5, 9),
            (130, 'JBK1131006', '信号与系统（1）', 2.0, 9),
            (131, 'JBK1131007', '信号与系统（2）', 2.0, 9),
            (132, 'JBK1131008', '信号与系统实验', 0.5, 9),
            (133, 'JBK1131012', '数字逻辑电路分析与设计', 4.0, 9),
            (134, 'JBK1131013', '数字逻辑电路分析与设计实验', 0.5, 9),
            (135, 'JBK1131009', '面向对象程序设计', 2.5, 9),
            (136, 'JBK1131011', '概率论与随机过程', 2.5, 9),
            (137, 'JBK1131010', '微机原理', 2.5, 9),
            (138, 'JBK1131015', '数字信号处理', 2.5, 9),
            (139, 'JBK1131016', '数据结构与算法基础', 3.0, 9),
            (140, 'JBK1131017', '电磁场理论', 3.0, 9),
            (141, 'JBK1131018', '通信原理A', 3.0, 9),
            (142, 'JBK1131020', '通信原理实验', 0.5, 9),
            (143, 'JBK1131021', '计算机网络', 2.5, 9),
            (144, 'JBK1131022', '信息论与编码', 2.5, 9),
            (145, 'JBK1131023', '通信电子线路', 2.5, 9),
            (146, 'JBK1131024', '通信电子线路实验', 0.5, 9),
            (147, 'JBK1131014', '工程经济学与IT项目管理', 1.0, 9),
            (148, 'JBK1231001', '模拟电子线路A', 3.5, 9),
            (149, 'JBK1231002', '模拟电子线路实验A', 0.5, 9),
            (150, 'JBK1231003', '数字电子线路A', 3.0, 9),
            (151, 'JBK1231004', '数字电子线路实验A', 0.5, 9),
            (152, 'JBK1231005', '高频电子线路', 3.0, 9),
            (153, 'JBK1231006', '高频电子线路实验', 0.5, 9),
            (154, 'JBK1300004', '计算机导论', 1.0, 9),
            (155, 'JBK1300005', '计算机实验', 1.0, 9),
            
            # --- 专业必修课程（模块10） ---
            (156, 'BBK1131001', '认识实习', 0.5, 10),
            (157, 'BBK1131003', '工程教育', 2.0, 10),
            (158, 'BBK1131004', '综合工程设计', 3.0, 10),
            (159, 'BBK1131002', '生产实习', 5.0, 10),
            (160, 'BBK1131005', '毕业论文（设计）', 8.0, 10),
        ]
        
        # 插入所有课程
        for c in courses:
            cursor.execute(
                f"INSERT INTO course (id, course_code, name, credit, module_id) VALUES "
                f"({c[0]}, '{c[1]}', '{c[2]}', {c[3]}, {c[4]})"
            )
        
        print(f"✅ 插入了 {len(courses)} 门课程")
        
        # 启用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        
        # 验证
        cursor.execute("SELECT COUNT(*) FROM module")
        m_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM course")
        c_count = cursor.fetchone()[0]
        
        print("\n" + "="*60)
        print("🎉 数据库重置成功！")
        print("="*60)
        print(f"\n📊 当前数据：")
        print(f"   模块数：{m_count}")
        print(f"   课程数：{c_count}")
        
        print(f"\n📁 完整模块结构：")
        cursor.execute("SELECT id, name, required_credits, parent_id FROM module ORDER BY id")
        for m in cursor.fetchall():
            indent = "  " if m[3] is not None else ""
            cursor.execute(f"SELECT COUNT(*) FROM course WHERE module_id = {m[0]}")
            cc = cursor.fetchone()[0]
            print(f"{indent}{m[0]}. {m[1]} ({m[2]}学分) - {cc}门课")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ shucredit-1 数据库已重置完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    reset_database()
