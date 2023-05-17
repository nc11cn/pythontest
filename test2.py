#!/usr/bin/python3
#coding=utf-8

import re

# ------------- 表头名 -----------
tbid = ['', 'a1', 'a2', 'a3']


# ------------- 定义函数：加表前缀的字段List.  输入：字段List, 输出：加前缀标记的字段List -------------
# 定义函数,根据输入List、标记、输出List
def f_tbid(collist1, collist2, mk):
    for i in collist1:
        if mk == '':
            i = i
        else:
            i = mk + '.' + i
        collist2.append(i) 

# ## ex.
# col = ['x','y']
# col1 = []
# f_tbid(col, col1, tbid[2])
# print(col1)

# ------------- 定义函数：join语句. 输入：主键List、join表头1, join表头2, 输出: join相等语句 -------------
# 输出例如 a1=a2 的等式List （更改ax,则修改 tdid[x]）
def f_keypjoin(keyp, tbid1, tbid2):
    keypjoin = []
    for i in keyp:
        i = f'{tbid1}.{i} = {tbid2}.{i}'
        keypjoin.append(i)
    keypjoin = '\nand '.join(keypjoin)
    return keypjoin

# ## ex.
# tdid1 = tbid[1]
# tdid2 = tbid[2]
# keyp = ['openid', 'gameid', 'idate']
# keypjoin = f_keypjoin( keyp, tdid1, tdid2 )
# print(keypjoin)

# ------------- 定义函数：字段语句as字段名. 输入：字典{字段名：字段语句}, 输出：, 字段语句 + as 字段名 \n -------------
def f_selas(a):
    i = ''
    for k,v in a.items():
        # 因为前加了逗号, 为了换行后对齐, 换行时用正则增加2个空格
        v = re.sub('\n', '\n  ', v)
        i =  i + ', '+ v + ' as ' + k + '\n'
    return i  

# ## ex.
# exsubstr = {'col1':'substr(col1, \n1\n, 2 )', 'col2':'substr(col2, 1, 2 )'}
# selas = f_selas(exsubstr)
# print(selas)

# ------------- 定义函数：登录bitmap转回流日期ID.  输入：字符串 - 数字 - 登录 - bitmap, 输出：回流日期ID -------------
def f_backmapid(vilbmp, m=0):
    i = f"strpos(\n" + '\t'*(1+m) + f"{vilbmp}\n" + '\t'*(1+m) + f", concat('1', array_join(repeat('0',30),'')), 1 )"
    return i

# ## ex.
# vilbmp = 'xxx'
# x = f_backmapid(vilbmp)
# print(x)

# ------------- 定义函数, 数字日期转timestamp. 输入：数字日期, 输出：timastamp -------------
def f_idate2ts(idate,m=0):
    i = "date_parse( cast(\n" + '\t'*(1+m) + f"{idate}\n" + '\t'*(1+m) + "as varchar), '%Y%m%d')"
    return i

# ## ex.
# print(f_idate2ts('idate'))

# -------------定义函数：所有数字日期转timestamp as新字段名. 输入：所有数字日期List, 输出：timastamp字段as更名 -------------
def f_allidate2ts(idatecol, idate2ts):
    for i in list:
        idate2ts['ts'+i] = f_idate2ts(i)

## ex.
# # # 定义空字典
# idate2ts = {}
# # # 把数字日期字段, 放入一个List中
# idatecol = ['regdate', 'idate']
# list = idatecol
# # 执行函数：循环读数字日期字段列表, 执行函数：数字日期转timastamp, 把函数执行结果的ts日期, 放入字典中. 字典key增加ts前缀
# f_allidate2ts(list, idate2ts)
# # # 打印字典
# # # print(idate2ts)
# # # 逐条打印select 语句
# print( f_selas(idate2ts) )

# ------------- 定义函数, 字符串日期时间转timestamp. 输入：字符串日期时间, 输出：timastamp -------------
def f_vdttm2ts(vdttm,m=0):
    i = "date_parse(\n" + '\t'*(1+m) + f"{vdttm}\n" + '\t'*(1+m) + ", '%Y-%m-%d %H:%i:%s')"
    return i

# ## ex.
# print(f_vdttm2ts('vdttm'))

# ------------- 定义函数：timestamp加减日期. 输入：加减类型, 加减数量, ts字段, , 输出：加减后ts日期 -------------
def f_tsaday(addtype, addnum, tsin, m=0 ):
    i = f"date_add(\n" + '\t'*(1+m) + f"{addtype}\n" + '\t'*(1+m) + f", {addnum}\n" + '\t'*(1+m) + f", {tsin} )"
    return i

# ## ex.
# x = f_tsaday("'day'", '+1', 'idate')
# print(x)

# ------------- 定义函数：timestamp转数字日期. 输入：ts日期. 输出：数字日期 -------------
def f_ts2idate(ts, m=0):
    i = f"cast( date_format(\n" + '\t'*(1+m) + f" {ts}\n" + '\t'*(1+m) + f", '%Y%m%d') as int)"
    return i 

# ## ex.
# x = f_ts2idate('xxxx')
# print(x)

# ------------- 定义交叉函数：数字日期加减日期 -------------
# ------------- 输入：数字日期转ts函数、ts加减函数、ts转数字函数、加减类型、加减数量. 输出：加减后数字日期 -------------
def f_idateaday(f_idate2ts , f_tsaday, f_ts2idate, addtype, addnum ,idate):
    i = f_ts2idate( f_tsaday( addtype , addnum ,f_idate2ts(idate, 2) , 1 ) )  # 附加\t数
    return i

# ## ex.
# x = f_idateaday(f_idate2ts, f_tsaday, f_ts2idate, "'day'", '+1' , 'idate')
# print(x)

# ------------- 使用交叉函数：数字日期加减 f_backmapid日期  -------------
# ------------- 输入：数字日期转ts函数、ts加减函数、ts转数字函数、加减类型、加减数量. 输出：加减后数字日期  -------------
# ## ex.
# addnum = f"-1 * ({f_backmapid('loginbitmap', 3)}) +1"  # 附加\t数
# x = f_idateaday(f_idate2ts, f_tsaday, f_ts2idate, "'day'", addnum )
# print(x)

# ------------- 定义函数：根据sql代码找select的字段数组  -------------
def f_sql2lcol(sql, starrepcol=''):
    x = re.search( 'select(.*?)from', sql, re.M|re.I|re.S)
    y = x.group(1)
    if re.search('\*', y):
        y = re.sub('(a\d\.){0,1}\*', starrepcol , y )
    z = re.split('\n,', y)
    lcolall = []
    for i in z:
        x = re.sub('\W+$', '', i)
        # print(x)
        y = re.split('\W', x)
        # print(y[-1])
        # 分出a1.xxx后的xxx
        y = re.split('\.', y[-1])
        # 不添加为空的元素
        if y[-1] != '':
            lcolall.append(y[-1])
    # print(lcolall)
    return lcolall


# ------------- 定义函数：  -------------
def f_crtchecktb(maxnum):
    z1 = ''
    crange = maxnum
    for x in range(crange):
        y = ', c' + str(x + 2) + ' varchar\n'
        z1 = z1 + y 

    sql2 = """
DROP table if EXISTS test.yzd_tmp_check ;
CREATE table test.yzd_tmp_check 
(
c1 VARCHAR
""" \
    + z1 + ');\n'
    return sql2    

# x = f_crtchecktb(99)
# print(x)

# ------------- 定义函数：输出结果到检查表  -------------
def f_check(sql, cmttb, tb, itnum1, starrepcol=''):
    lnum = [x for x in range(itnum1,1000)]
    itnum = iter(lnum)
    # print(starrepcol)
    # 这里可能不能用starrepcol=''
    lcolall = f_sql2lcol(sql, starrepcol)
    # print(lcolall)

    # print(len(lcolall))

    # 把字段转成 castasvarchar格式, 以及不转varchar的两种换行加逗号字符串
    castasvarchar = ''
    strcolall = ''
    for i in lcolall:
        if re.search('_arr$', i):
            # array类型无法转varchar, 改用其他类型转换
            x = ', array_join(' + i + ", '、')\n"
        else:
            x = ', cast(' + i + " as varchar)\n"
        y = ", '" + i + "'\n"
        castasvarchar = castasvarchar + x
        strcolall = strcolall + y

    # print(z5)

    # print(len(lcolall))

    # 定义函数, 根据select字段数输出需要insertinto的字段数
    def f_t_2(maxnum): 
        insertcolnum = ''
        for x in range(1, maxnum):
            y = ', c' + str(x + 1) + '\n'
            insertcolnum = insertcolnum + y 
            # print(insertcolnum)
        return insertcolnum

    insertcolnum = f_t_2( len(lcolall) + 1 )


    # print(insertcolnum)

    sql2 = "\ninsert into test.yzd_tmp_check (c1) select " + f"""'{"%03d" % next(itnum)}'""" + ";\n"\
        + "insert into test.yzd_tmp_check (c1, c2) select " + f"""'{"%03d" % next(itnum)}'""" + ", '" + cmttb + "';\n"\
        + "insert into test.yzd_tmp_check (c1, c2) select " + f"""'{"%03d" % next(itnum)}'""" + ", '" + tb + "';\n"\
        + "insert into test.yzd_tmp_check (c1) select " + f"""'{"%03d" % next(itnum)}'""" + ";\n"\
        + "insert into test.yzd_tmp_check (\n c1\n" + insertcolnum + ')\n' \
        + "(select " + f"""'{"%03d" % next(itnum)}'""" + " \n" + strcolall + ") \nunion all\n" \
        + "(select " + f"""'{"%03d" % next(itnum)}'""" + " \n" + castasvarchar \
        + "from " + tb \
        + "\nlimit 20 );\n" \
        + "insert into test.yzd_tmp_check (c1) select " + f"""'{"%03d" % next(itnum)}'""" + ";\n"

    selectcolnum = 2
    insertinto_0 = "insert into test.yzd_tmp_check (\n c1\n"
    z5 = 'select \n'
    z6 = ', cast(count(1) as varchar) as num \n'
    z2 = ", 'num'\n"
    if 'openid' in lcolall:
        z6 = z6 + ', cast(count(distinct openid) as varchar) as openid_num\n'
        z2 = z2 + ", 'openid_num'\n"
        selectcolnum =selectcolnum + 1

    if 'uid' in lcolall:
        z6 = z6 + ', cast(count(distinct uid) as varchar) as uid_num\n'
        z2 = z2 + ", 'uid_num'\n"
        selectcolnum = selectcolnum + 1

    if {'openid', 'samp'} < set(lcolall):
        z6 = z6 + ', cast(count(distinct if(samp=1, openid, null)) as varchar) as openid_s_num\n'
        z2 = z2 + ", 'openid_s_num'\n"
        selectcolnum = selectcolnum + 1

    if {'uid', 'samp'} < set(lcolall):
        z6 = z6 + ', cast(count(distinct if(samp=1, uid, null)) as varchar) as uid_s_num\n'
        z2 = z2 + ", 'openid_num'\n"
        selectcolnum = selectcolnum + 1

    insertinto = insertinto_0 +  f_t_2(selectcolnum) + ')\n' 
    selectfromunion = z5 + f"""'{"%03d" % next(itnum)}'""" \
        + z2 + 'union all\n' + z5 \
        + f"""'{"%03d" % next(itnum)}'""" + z6 + 'from '  + tb + '\n'

    z9 = ''
    z9 = z9 + insertinto + selectfromunion + ';\n' \
        + "insert into test.yzd_tmp_check (c1) select "\
        + f"""'{"%03d" % next(itnum)}'""" + ";\n"

    sql2 = sql2 + z9
    z9 = ''

    groupby = ''
    l1 = ['gameid', 'idate' ]
    l2 = ['idate']
    l3 = ['gameid']

    def f_t_1(list, groupby, selectfromunion, z5, z9, piciid):
        insertinto = insertinto_0 + f_t_2(selectcolnum + len(list)) + ')\n' 
        groupby = groupby + 'group by ' + piciid + ', ' + ', '.join(l1)  + ' \norder by ' + ', '.join(l1) + '\n;'
        selectgroupvarchar = piciid + ' as piciid'
        for i in l1:
            selectgroupvarchar = selectgroupvarchar  + ', cast(' + i + ' as varchar)\n'
        selectfromunion = z5 + selectgroupvarchar + z6 + 'from '  + tb + '\n'
        z9 = z9 + insertinto + selectfromunion + groupby
        return z9
    
    tmpnum = f"""'{"%03d" % next(itnum)}'"""

    if set(l1) < set(lcolall):
        z9 = f_t_1(l1, groupby, selectfromunion, z5, z9, tmpnum)
    elif set(l2) < set(lcolall):
        z9 = f_t_1(l2, groupby, selectfromunion, z5, z9, tmpnum)
    elif set(l3) < set(lcolall):
        z9 = f_t_1(l2, groupby, selectfromunion, z5, z9, tmpnum)


    sql2 = sql2 + z9
    z9 = ''
    return (sql2,  next(itnum))


# ------------- 定义函数：输出临时表名  -------------
# 临时表变量名规则：tb1、tb2、……、tbb1、tbb2……、tbc1、……
def f_tb(tbmk, tkid = ''):
    topmk = 'test.tmp_yzd_'
    tblist = []
    for i in range(1, 99):
        x = topmk + '_' + tkid + tbmk + '_' + str(i)
        tblist.append(x)
    y = iter(tblist)
    return y

# x = f_tb('a')
# print(next(x))
# print(next(x))


# ------------- 定义函数：输出建表或insertinto或union语句  -------------
def f_crttb(type, tb, crttype='table'):
    crt = f"""drop table if exists {tb};\ndrop view if exists {tb};\
        \ncreate {crttype} {tb} as \n"""
    insertintotb = f"insert into {tb} \n"
    unionall = 'union all' + '\n'
    if type == 'crt':
        sqlcrt = crt
    elif type == 'insert':
        sqlcrt = insertintotb
    elif type == 'union':
        sqlcrt = unionall
    return sqlcrt

# x = f_crttb('union', 'tb3', crttype='table')
# print(x)


# ------------- 定义函数：取分隔符最后N个,并合并输出  -------------
def f_splitconcat(inx, splitmk, dirtype , tknum, concat=None, a=None):
    x = re.split(splitmk, inx)
    list = []
    if dirtype == 'left':
        for i in range(tknum):
            list.append(x[i])
    elif dirtype == 'right':
        for i in range(-1 * tknum, 0):
            list.append(x[i])
    if concat is None:
        outx = splitmk.join(list)
    else:
        outx = concat.join(list)
    if a is not None:
        outx = re.sub('^a', '', outx)
    return outx

# inx = 'test.tmp_yzd__a_3'
# x = f_splitconcat(inx, '_', 'right', 2, '', '')
# print(x)


# ------------- 定义函数：输入数组与mk, 输出指定分隔符string  -------------
def f_mklist2str(mk, list, split):
    list2 = []
    for i in list:
        list2.append(mk + i)
    outx = split.join(list2)
    return outx

# list = ['xx', 'yy', 'zz']
# x = f_mklist2str('a2.', list, '\n, ')
# print(x)


# ------------- 定义函数：输出select 到from前的语句  -------------
# 面对带逗号的语句, 会出错, 比如： , count(if(x = 1, 1, null)) as zzz
def f_sel2frm(selkey='', selall='', selpart='', seltg=''):
    sel = 'select \n'
    lst2 = []
    for l in [selkey, selall, selpart, seltg]:
        pattern = r'''
            \\s*             # 匹配0或多个空白字符
            ,               # 匹配英文逗号
            (?=             # 向前查找
                (?:         # 以下是一个非捕获组
                    [^()]*  # 匹配0或多个非括号字符
                    (?:     # 以下是一个非捕获组
                        \\(
                        [^()]*  # 匹配0或多个非括号字符
                        \\)
                    )?      # 该非捕获组出现0次或1次
                )*          # 该非捕获组出现0或多次
                [^()]*      # 匹配0或多个非括号字符
                $           # 匹配行末
            )
            '''
        lst1 = re.split(pattern, l, flags=re.X)
        for i in lst1:
            i = i.strip()
            if i not in lst2 and i != '':
                lst2.append(i)
    x = '\n, '.join(lst2)
    return sel + x


selkey = ' xx \n, yy, \n dd as aa, count(distinct aaa) as aaa, count(distinct if(a = 1, 1, null)) as bbb'
selpart = ' , \n yy, zz'
x = f_sel2frm(selkey,  selpart)
print(x)


# ------------- 定义函数：输入空格, 逗号, 换行分隔字符, 输出List  -------------
def f_strsplit2lst(str):
    x = re.split('(?:,| |\n)+', str)
    return x 

# a = """xxx, ddd,  hhhabababuuu ffff  bbbb yyy
# zzz iii
# kkk"""

# a = ''
# x = f_strsplit2lst(a)
# print(x)


# ------------- 定义函数：判断输入是否为空, 空则输出空, 否则输出物  -------------
def f_ifnone(inx, outx):
    if inx == '' or inx is None or inx == [] or inx == ['']:
        return ''
    else:
        return outx


# ------------- 定义函数：输出join on语句  -------------
def f_jnn(jid1, jlist1, jid2, jlist2, idmk = 'a'):
    jlist12 = []
    if jlist1 != '' and jlist1 != [''] and jlist1 is not None :
        for i in range(len(jlist1)):
            x = idmk + str(jid1) + '.' + jlist1[i] + ' = ' \
            + idmk + str(jid2) + '.' + jlist2[i]
            jlist12.append(x)
    return '\nand '.join(jlist12)

# x = f_jnn(1, ['x', 'y', 'z'], 2 , ['xx', 'yy', 'zz'])

# x = f_jnn(1, ['x', 'y', 'z'], 2 , ['xx', 'yy', 'zz'])
# print(x)


# ------------- 定义函数：输出join语句  -------------
def f_iljoin(frmtb \
             , jntype1 = '', jntb1 = '', jnon1 = '' \
             , jntype2 = '', jntb2 = '', jnon2 = '' \
             , jntype3 = '', jntb3 = '', jnon3 = '' \
             , jntype4 = '', jntb4 = '', jnon4 = '' \
             , jntype5 = '', jntb5 = '', jnon5 = '' \
             , jntype6 = '', jntb6 = '', jnon6 = '' ):
    frm = '\nfrom '
    tbid, jntbid1, jntbid2, jntbid3, jntbid4, jntbid5 , jntbid6= \
    'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'
    # ## join1
    jntype1 = jntype1 # join1类型, 如 'inner' 或 'left'
    jntb1 = jntb1 # join1的表, 如 tb 1 或 dbmk + vwname1 
    jnon1 = jnon1 # join1后的on语句, 如 a1.x = a2.x 或 函数 f.f_x(xx)
    # ## join2
    jntype2 = jntype2 # join2类型, 如 'inner' 或 'left'
    jntb2 = jntb2 # join2的表, 如 tb 1 或 dbmk + vwname1 
    jnon2 = jnon2 # join2后的on语句, 如 a1.x = a3.x 或 函数 f.f_x(xx)
    # ## join3
    jntype3 = jntype3 # join3类型, 如 'inner' 或 'left'
    jntb3 = jntb3 # join3的表, 如 tb 1 或 dbmk + vwname1 
    jnon3 = jnon3 # join3后的on语句, 如 a1.x = a4.x 或 函数 f.f_x(xx)
    # ## join4
    jntype4 = jntype4 # join4类型, 如 'inner' 或 'left'
    jntb4 = jntb4 # join4的表, 如 tb 1 或 dbmk + vwname1 
    jnon4 = jnon4# join4后的on语句, 如 a1.x = a5.x 或 函数 f.f_x(xx)
    # ## join5
    jntype5 = jntype5 # join5类型, 如 'inner' 或 'left'
    jntb5 = jntb5 # join5的表, 如 tb 1 或 dbmk + vwname1 
    jnon5 = jnon5 # join5后的on语句, 如 a1.x = a6.x 或 函数 f.f_x(xx)   
    # ## join6
    jntype6 = jntype6 # join5类型, 如 'inner' 或 'left'
    jntb6 = jntb6 # join5的表, 如 tb 1 或 dbmk + vwname1 
    jnon6 = jnon6 # join5后的on语句, 如 a1.x = a6.x 或 函数 f.f_x(xx)  
    ###
    sqljn1 =  jntype1 + ' join ' + jntb1 + ' ' + jntbid1 + '\n' \
        + 'on\n' + jnon1 + '\n' 
    sqljn2 = jntype2 + ' join ' + jntb2 + ' ' + jntbid2 + '\n' \
        + 'on\n' + jnon2 + '\n' 
    sqljn3 = jntype3 + ' join ' + jntb3 + ' ' + jntbid3 + '\n' \
        + 'on\n' + jnon3 + '\n' 
    sqljn4 = jntype4 + ' join ' + jntb4 + ' ' + jntbid4 + '\n' \
        + 'on\n' + jnon4 + '\n' 
    sqljn5 = jntype5 + ' join ' + jntb5 + ' ' + jntbid5 + '\n' \
        + 'on\n' + jnon5 + '\n' 
    sqljn = f_ifnone(jnon1, sqljn1) + f_ifnone(jnon2, sqljn2) \
        + f_ifnone(jnon3, sqljn3) + f_ifnone(jnon4, sqljn4) \
        + f_ifnone(jnon5, sqljn5)
    ###
    sqlfrm = frm + frmtb + ' ' + tbid + '\n' 
    return sqlfrm , sqljn

# x = f_iljoin('inner', 'tb2', 'a1.x = a2.x')
# x = f_iljoin('', '', '')
# x = f_iljoin('tb1', 'inner', 'tb2', f_jnn(1,['x', 'y'], 2, ['xx', 'yy']))

# print(x[0])
# print(x[1])


# ------------- 定义函数：输出sql where语句  -------------
def f_sqlwhr(sqlwhr=''):
    if sqlwhr != '':
        sqlwhr = 'where ' + sqlwhr + '\n'
    return sqlwhr

# sqlwhr = f"""
# a = b and c = d
# """

# x = f_sqlwhr(sqlwhr)
# print(x)


# ------------- 定义函数：输出sql groupby语句  -------------
def f_sqlgrp(sqlgrp=''):
    if sqlgrp != '':
        sqlgrp = 'group by ' + sqlgrp + '\n'
    return sqlgrp


# ------------- 定义函数：输出sql having语句  -------------
def f_sqlhav(sqlhav=''):
    if sqlhav != '':
        sqlhav = 'having ' + sqlhav + '\n'
    return sqlhav


# ------------- 定义函数：输出sql orderby语句  -------------
def f_sqlord(sqlord=''):
    if sqlord != '':
        sqlord = 'order by ' + sqlord + '\n'
    return sqlord


# ------------- 定义函数：输出sql limit语句  -------------
def f_sqllmt(sqllmt=''):
    if sqllmt != '':
        sqllmt = 'limit ' + sqllmt + '\n'
    return sqllmt



# ------------- 定义函数：输出完整多个sql语句  -------------
def f_outallsql(sql, tb, cmttb, selkey, selall, selpart, seltg \
                , jnon1id1,jnon1c1, jnon1id2, jnon1c2 \
                , jnon2id1,jnon2c1, jnon2id2, jnon2c2 \
                , jnon3id1,jnon3c1, jnon3id2, jnon3c2 \
                , jnon4id1,jnon4c1, jnon4id2, jnon4c2 \
                , jnon5id1,jnon5c1, jnon5id2, jnon5c2 \
                , jnon6id1,jnon6c1, jnon6id2, jnon6c2 \
                , frmtb, jntype1, jntb1, jntype2, jntb2 \
                , jntype3, jntb3, jntype4, jntb4 \
                , jntype5, jntb5, jntype6, jntb6 \
                , sqlcrt, sqlend \
                , sqlwhr='', sqlgrp='', sqlhav='', sqlord='', sqllmt=''
                ):
    sqlcmt = '-- ' + f_splitconcat(tb, '_', 'right', 2, '', '')\
        + '、 ' + cmttb + '\n'
    sqlsel = 'select \n' + selkey + selall + selpart + seltg
    # for i in range(1, 6):
    #     for m in ['c1', 'c2']:
    #         x = 'jnon' + str(i) + m
    #         x1 = x + ' = f_strsplit2lst(' + x + ')'
    #         exec(x1) # exec放函数里, 好像不执行

    jnon1 = f_jnn(jnon1id1,jnon1c1, jnon1id2, jnon1c2) 
    jnon2 = f_jnn(jnon2id1,jnon2c1, jnon2id2, jnon2c2)
    jnon3 = f_jnn(jnon3id1,jnon3c1, jnon3id2, jnon3c2)
    jnon4 = f_jnn(jnon4id1,jnon4c1, jnon4id2, jnon4c2)
    jnon5 = f_jnn(jnon5id1,jnon5c1, jnon5id2, jnon5c2)
    jnon6 = f_jnn(jnon6id1,jnon6c1, jnon6id2, jnon6c2)
    return_iljoin = f_iljoin(frmtb, jntype1, jntb1, jnon1 \
                            , jntype2, jntb2, jnon2 \
                                , jntype3, jntb3, jnon3 \
                                , jntype4, jntb4, jnon4 \
                                , jntype5, jntb5, jnon5 \
                                , jntype6, jntb6, jnon6 )
    sqlfrm = return_iljoin[0]
    sqljn = return_iljoin[1]

    sqlwhr, sqlgrp, sqlhav, sqlord, sqllmt = f_sqlwhr(sqlwhr) \
        , f_sqlgrp(sqlgrp), f_sqlhav(sqlhav) \
        , f_sqlord(sqlord), f_sqllmt(sqllmt)

    # print('-'*30 + sqlhav)

    sqlnew = sqlcmt + sqlcrt \
            + '(\n' \
            + sqlsel + sqlfrm \
            + sqljn \
            + sqlwhr + sqlgrp + sqlhav + sqlord + sqllmt \
            + ')' \
            + sqlend \
            + '\n' + '\n'
    sql = sql + sqlnew
    return sqlnew, sql

            