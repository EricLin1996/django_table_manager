-- 更新项目状态码
-- 旧状态码 -> 新状态码映射：
-- 0 (未开始) -> 1 (正常)
-- 10 (进行中) -> 1 (正常)  
-- 20 (已完结) -> 2 (完成)
-- 30 (已停工) -> 4 (停工)

UPDATE sub_projects 
SET status = CASE 
    WHEN status = '0' THEN '1'
    WHEN status = '10' THEN '1'
    WHEN status = '20' THEN '2'
    WHEN status = '30' THEN '4'
    ELSE status
END
WHERE status IN ('0', '10', '20', '30');

-- 查询更新后的状态分布
SELECT status, 
       CASE 
           WHEN status = '1' THEN '正常'
           WHEN status = '2' THEN '完成'
           WHEN status = '3' THEN '需要整改'
           WHEN status = '4' THEN '停工'
           ELSE '未知状态'
       END as status_name,
       COUNT(*) as count
FROM sub_projects 
WHERE status IS NOT NULL
GROUP BY status
ORDER BY status; 