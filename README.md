# Test
实体对齐

一、环境：java，jdk11
    https://www.oracle.com/java/technologies/downloads/#java11-windows
    
二、code是加工脚本，按步骤执行即可
    Excel是自己标的三元组，如果不支持.xlsx就用.xls
    
三、result是知识图谱，按说明文档操作

四、图数据库检索常用语句：
1、检索实体数据：
	# 查询'69-4 型潜水装具'的相关部件；
	MATCH p=(n:Nodes{name:'69-4 型潜水装具'})-[r:predicate]-(m:Nodes) 
	where r.name = '部件'
	RETURN p	
	
	# 查询'69-4 型潜水装具'的所有的关联关系
	MATCH p=(n:Nodes{name:'69-4 型潜水装具'})-[r:predicate]-(m:Nodes) 
	RETURN p
	
2、创建索引
	创建索引：CREATE INDEX ON :Nodes(name)
	查询创建的索引   :schema 
	删除索引：DROP INDEX ON :Nodes(name)
	
3、显示全部节点（默认显示300个节点，若实体超过300，在设置中“Initial Node Display”设置显示数值）           
  match(n) return n	
