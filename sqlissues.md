# sql问题

## 1. metalock
查询阻塞事务

``` sql
select * from information_schema.innodb_trx;
```

生成删除代码

``` sql
select concat('kill ',trx_mysql_thread_id,';') from (select trx_mysql_thread_id from information_schema.innodb_trx) as kills;

```
杀死对应ip和user的connection

``` sql
set @_host='117.136.30.199:%';
select concat('kill ',id,';') from (select * FROM information_schema.processlist
where user='enteam' and HOST LIKE @_host) as kills;
```

粘贴运行生出的删除代码

``` sql
kill 24378;
kill 24377;
kill 24376;
kill 24375;
kill 24374;
kill 24373;
kill 24372;
kill 24371;
kill 24370;
kill 24369;
kill 24368;
kill 24367;
kill 24366;
```
## 2. sleep连接
生成删除代码
``` sql
select concat('KILL ',id,';') from information_schema.processlist
where user='enteam' 
```
##  3.连接过多问题
查看ip连接数量

``` sql
SET @_host='223.104.251.48:%';
select * from information_schema.processlist
where user='enteam'  and HOST LIKE @_host;
SELECT COUNT(*) FROM information_schema.processlist
where user='enteam' and HOST LIKE @_host;
```
