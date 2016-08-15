first_steps = dict(CentOS_6=[
    'yum update && yum install yum-utils -y',
    'yum install git -y'
])

lamp_cmd = dict(CentOS_6=['''yum -y install httpd'''
    , '''service httpd start'''
    , '''service httpd status'''
    , '''/sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT'''
    , '''/etc/rc.d/init.d/iptables save'''
    , '''yum -y install mysql-server'''
    , '''service mysqld start'''
    , '''mysqladmin -u root password "$DATABASE_PASS"'''
    ,
                    '''mysql -u root -p"$DATABASE_PASS" -e "UPDATE mysql.user SET Password=PASSWORD('$DATABASE_PASS') WHERE User='root'"'''
    ,
                    '''mysql -u root -p"$DATABASE_PASS" -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"'''
    , '''mysql -u root -p"$DATABASE_PASS" -e "DELETE FROM mysql.user WHERE User=''"'''
    , '''mysql -u root -p"$DATABASE_PASS" -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\_%'"'''
    , '''mysql -u root -p"$DATABASE_PASS" -e "FLUSH PRIVILEGES"'''
    , '''yum -y install php php-mysql'''
    , '''yum search php-'''
    , '''yum info NameOfTheModule'''
    , '''yum -y install php-mcrypt.x86_64'''
    , '''yum -y install php-mbstring.x86_64'''
    , '''chkconfig httpd on'''
    , '''chkconfig mysqld on'''
    , '''service httpd restart'''])
