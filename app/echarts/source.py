import pymysql
import pandas as pd

con = pymysql.connect(host='localhost', port=3306, db='education', user='lookup', passwd='lookup123456')

list_score = [400, 450, 500, 550, 600, 650, 700, 750]

a = 0
b = 1
sql_list = []
while a<= 6:
	s = list_score[a]
	t = list_score[b]
	a = a + 1
	b = b + 1
	sql = 'select count(*) from like_1op_score_2020 where 总分 between %s and %s' % (s, t)
	sql_list.append(sql)

i = 0
result = []
while i <= len(sql_list)-1:
	k = sql_list[i]
	i += 1
	Kr = pd.read_sql(k, con)
	Kw = Kr.iat[0, 0]
	result.append(Kw)

score_level = ['400-450', '450-500', '500-550', '550-600', '600-650', '650-700', '700+']