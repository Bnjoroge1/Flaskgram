
BEGIN;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('63b8ae348991');
CREATE TABLE comment (
	id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	content TEXT NOT NULL, 
	post_id INTEGER NOT NULL, 
	CONSTRAINT pk_comment PRIMARY KEY (id), 
	CONSTRAINT fk_comment_post_id_user FOREIGN KEY(post_id) REFERENCES user (id)
);
CREATE TABLE connection (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	provider_id VARCHAR(255), 
	provider_user_id VARCHAR(255), 
	access_token VARCHAR(255), 
	secret VARCHAR(255), 
	display_name VARCHAR(255), 
	profile_url VARCHAR(512), 
	image_url VARCHAR(512), 
	rank INTEGER, 
	CONSTRAINT pk_connection PRIMARY KEY (id), 
	CONSTRAINT fk_connection_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE followers (
	follower_id INTEGER, 
	followed_id INTEGER, 
	CONSTRAINT fk_followers_followed_id_user FOREIGN KEY(followed_id) REFERENCES user (id), 
	CONSTRAINT fk_followers_follower_id_user FOREIGN KEY(follower_id) REFERENCES user (id)
);
INSERT INTO followers VALUES(5,4);
INSERT INTO followers VALUES(7,4);
INSERT INTO followers VALUES(7,5);
INSERT INTO followers VALUES(5,7);
INSERT INTO followers VALUES(5,7);
INSERT INTO followers VALUES(8,7);
INSERT INTO followers VALUES(8,7);
INSERT INTO followers VALUES(8,7);
INSERT INTO followers VALUES(9,8);
INSERT INTO followers VALUES(5,8);
INSERT INTO followers VALUES(5,8);
INSERT INTO followers VALUES(10,5);
INSERT INTO followers VALUES(10,9);
INSERT INTO followers VALUES(10,7);
INSERT INTO followers VALUES(10,8);
INSERT INTO followers VALUES(11,10);
INSERT INTO followers VALUES(12,11);
INSERT INTO followers VALUES(12,8);
INSERT INTO followers VALUES(12,10);
INSERT INTO followers VALUES(12,9);
INSERT INTO followers VALUES(5,9);
INSERT INTO followers VALUES(5,12);
INSERT INTO followers VALUES(5,10);
INSERT INTO followers VALUES(15,9);
INSERT INTO followers VALUES(15,10);
INSERT INTO followers VALUES(15,12);
INSERT INTO followers VALUES(15,5);
INSERT INTO followers VALUES(19,9);
INSERT INTO followers VALUES(19,15);
INSERT INTO followers VALUES(15,19);
INSERT INTO followers VALUES(20,15);
INSERT INTO followers VALUES(21,15);
INSERT INTO followers VALUES(21,20);
CREATE TABLE post (
	id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	content TEXT NOT NULL, 
	user_id INTEGER NOT NULL, 
	post_image VARCHAR(20), 
	CONSTRAINT pk_post PRIMARY KEY (id), 
	CONSTRAINT fk_post_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO post VALUES(1,'r=','2020-08-16 10:54:12.083878','tesrere',4,'default.png');
INSERT INTO post VALUES(2,'rerere','2020-08-18 09:17:10.671906','rererer',7,'default.png');
INSERT INTO post VALUES(3,'rerere','2020-08-18 09:17:33.402635','rererer',7,'default.png');
INSERT INTO post VALUES(4,'second post','2020-08-18 09:33:00.515468',replace(replace('love it\r\n','\r',char(13)),'\n',char(10)),7,'default.png');
INSERT INTO post VALUES(5,'dog','2020-08-18 10:05:52.110365','sfdf',8,'default.png');
INSERT INTO post VALUES(6,'fjk','2020-08-18 10:08:05.382278','jkjk',8,'default.png');
INSERT INTO post VALUES(7,'brujghgh','2020-08-18 10:09:08.452978','hghghg',8,'default.png');
INSERT INTO post VALUES(8,'Computer Science','2020-08-18 10:12:30.124088','m,jkjjlklk',8,'default.png');
INSERT INTO post VALUES(9,'ghjjhyy','2020-08-18 10:13:09.922278','uyuyufu',8,'default.png');
INSERT INTO post VALUES(10,'ferererer','2020-08-19 13:08:28.188940','rerfeerere',8,NULL);
INSERT INTO post VALUES(11,'ferererer','2020-08-19 13:12:03.782973','rerfeerere',8,NULL);
INSERT INTO post VALUES(12,'ferererer','2020-08-19 13:14:27.556917','rerfeerere',8,NULL);
INSERT INTO post VALUES(13,'frtrrtrt','2020-08-19 13:20:51.604306','rtrtrrryr',8,NULL);
INSERT INTO post VALUES(14,'try','2020-08-19 14:20:40.009317','ytytyt',8,NULL);
INSERT INTO post VALUES(15,'rerer','2020-08-19 14:26:21.047817','revertrbrb',8,NULL);
INSERT INTO post VALUES(16,'feere','2020-08-19 14:41:09.786747','rferer',8,NULL);
INSERT INTO post VALUES(17,'fererevf','2020-08-19 14:55:25.242224',replace(replace('regrggrt\r\n\r\n','\r',char(13)),'\n',char(10)),8,'c7165501f46fdcc7.jpeg');
INSERT INTO post VALUES(18,'RERER','2020-08-20 14:21:23.679856','VGTHTYTY',10,'57447aca0356e72b.jpeg');
INSERT INTO post VALUES(19,'testing notif','2020-08-21 12:20:24.726545','jfdrtrt',11,'2206096165570e32.png');
INSERT INTO post VALUES(20,'testing notif','2020-08-21 12:21:30.768792','jfdrtrt',11,'e2f4c7742af29f01.png');
INSERT INTO post VALUES(21,'testing notif2332','2020-08-21 12:21:44.370913',replace(replace('jfdrtrt324343\r\n','\r',char(13)),'\n',char(10)),11,'3eea16ed40f93170.png');
INSERT INTO post VALUES(22,'testing notif2332trrt45','2020-08-21 12:22:32.407720',replace(replace('jfdrtrt324343\r\n54545454','\r',char(13)),'\n',char(10)),11,'a68de17d701e278b.png');
INSERT INTO post VALUES(23,'try56u6utjtjtjty','2020-08-21 12:30:15.489061','ghgjjgjgjg',11,'eae66072167ed710.jpeg');
INSERT INTO post VALUES(24,'try56u6utjtjtjtyuiuu','2020-08-21 12:33:10.570074','jhuhuighgjjgjgjg',11,'460be731572cfb65.jpeg');
INSERT INTO post VALUES(25,'yiuyuyuyiyi','2020-08-21 12:45:22.585159','uyuyuiyiyiyi',11,'fe4031cbf086bff6.jpeg');
INSERT INTO post VALUES(26,'tytytyyiuyuyuyiyi','2020-08-21 12:51:34.088491','uyuyuiyiyiyiytytyty',11,'e2b82ef6adbccd4b.jpeg');
INSERT INTO post VALUES(27,'tytytyyiuyuyuyiyi','2020-08-21 12:52:39.172116','uyuyuiyiyiyiytytyty',11,'0c6f19fb5b19d488.jpeg');
INSERT INTO post VALUES(28,'testing email','2020-08-21 17:41:36.890604','testing email',9,'5b599a7a22e72693.jpeg');
INSERT INTO post VALUES(29,'testing email','2020-08-21 17:43:49.041457','testing email',9,'4f7ef673d278f5b1.jpeg');
INSERT INTO post VALUES(30,'testing email','2020-08-21 17:44:13.858121','testing email',9,'c3741a98a0ef8b7d.jpeg');
INSERT INTO post VALUES(31,'testing email','2020-08-21 17:44:39.839344','testing email',9,'7d14c6ada52e5634.jpeg');
INSERT INTO post VALUES(32,'testing email','2020-08-21 17:50:38.683893','testing email',9,'d8fc78d9d98085fc.jpeg');
INSERT INTO post VALUES(33,'testing email','2020-08-21 17:50:48.669881','testing email',9,'b48d4d62470a113c.jpeg');
INSERT INTO post VALUES(34,'testing email','2020-08-21 17:56:33.795907','testing email',9,'c001c6065a38963d.jpeg');
INSERT INTO post VALUES(35,'testing email','2020-08-21 18:01:16.195747','testing email',9,'0f6a6c47d6235192.jpeg');
INSERT INTO post VALUES(36,'testing email','2020-08-21 18:02:29.699030','testing email',9,'de13ef6f196fc476.jpeg');
INSERT INTO post VALUES(37,'testing emailerere','2020-08-21 18:54:57.701411','testing emailrererer',9,'d1a4eac89062f832.jpeg');
INSERT INTO post VALUES(38,'testing emailerere','2020-08-21 18:58:13.888507','testing emailrererer',9,'96a3afe76f1f7425.jpeg');
INSERT INTO post VALUES(39,'testing emailerere','2020-08-21 18:58:37.101368','testing emailrererer',9,'eb60d187badf7281.jpeg');
INSERT INTO post VALUES(40,'testing emailerere','2020-08-21 18:58:59.736419','testing emailrererer',9,'30e45fc6da4078e5.jpeg');
INSERT INTO post VALUES(41,'testing emailerere','2020-08-21 18:59:32.573153','testing emailrererer',9,'0c89a8fe2a3a4a62.jpeg');
INSERT INTO post VALUES(42,'testing emailerere','2020-08-21 18:59:46.152693','testing emailrererer',9,'d8537c2e431fe197.jpeg');
INSERT INTO post VALUES(43,'testing emailerere','2020-08-21 18:59:51.805800','testing emailrererer',9,'0f51193068c97c72.jpeg');
INSERT INTO post VALUES(44,'testing emailerere','2020-08-21 19:01:47.236519','testing emailrererer',9,'82783fbb6fa12c73.jpeg');
INSERT INTO post VALUES(45,'testing emailerere','2020-08-21 19:04:30.726796','testing emailrererer',9,'88de83c92a7429ff.jpeg');
INSERT INTO post VALUES(46,'rererer','2020-08-21 19:06:12.842542','gytuyuyiy',9,'aa9dc95451fd1a3a.gif');
INSERT INTO post VALUES(47,'rererec','2020-08-21 19:12:58.269563','ceceeveere',9,'be22ed2ef89edd92.png');
INSERT INTO post VALUES(48,'fdgfryr','2020-08-24 16:32:09.112435','dfdfdf',15,'871dd34a744cd233.png');
INSERT INTO post VALUES(49,'kk','2020-08-26 11:28:30.641452','kkkk',21,'e5f79522d6de952b.png');
INSERT INTO post VALUES(50,'kk','2020-08-26 11:28:37.635648','kkkk',21,'3114ea46b5eba0b9.png');
INSERT INTO post VALUES(51,'iioio','2020-08-26 12:40:18.239231','huii',15,'bfabadafa0b24a6d.png');
INSERT INTO post VALUES(52,'FDFDFD','2020-08-26 12:41:59.003573','FDFDFDF',15,'3a3b1029e98dc4d6.png');
INSERT INTO post VALUES(53,'FDFDFD','2020-08-26 12:44:38.217337','FDFDFDF',15,'d1880abadd66323f.png');
INSERT INTO post VALUES(54,'FDFDFD','2020-08-26 12:47:06.384813','FDFDFDF',15,'c2f23c9c020a6e3c.png');
INSERT INTO post VALUES(55,'FDFDFD','2020-08-26 12:53:21.600356','FDFDFDF',15,'7f7a159f420c6fce.png');
CREATE TABLE post_like (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	post_id INTEGER, 
	CONSTRAINT pk_post_like PRIMARY KEY (id), 
	CONSTRAINT fk_post_like_post_id_post FOREIGN KEY(post_id) REFERENCES post (id), 
	CONSTRAINT fk_post_like_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE facebook_user (
	social_id INTEGER NOT NULL, 
	username VARCHAR(20), 
	CONSTRAINT pk_facebook_user PRIMARY KEY (social_id), 
	CONSTRAINT uq_facebook_user_username UNIQUE (username)
);
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR(64), 
	"default" BOOLEAN, 
	permissions INTEGER, 
	CONSTRAINT pk_roles PRIMARY KEY (id), 
	CONSTRAINT uq_roles_name UNIQUE (name), 
	CONSTRAINT ck_roles_default CHECK ("default" IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "user" (
	id INTEGER NOT NULL, 
	username VARCHAR(20), 
	email VARCHAR(120), 
	image_file VARCHAR(20), 
	password VARCHAR(60), 
	bio VARCHAR(140), 
	last_seen DATETIME, 
	registered_on DATETIME, 
	admin BOOLEAN, 
	confirmed BOOLEAN, 
	confirmed_on DATETIME, 
	social VARCHAR(64), 
	role_id INTEGER, 
	receive_notifs BOOLEAN, 
	phone_number INTEGER, 
	CONSTRAINT pk_user PRIMARY KEY (id), 
	CHECK (admin IN (0, 1)), 
	CHECK (confirmed IN (0, 1)), 
	CHECK (receive_notifs IN (0, 1)), 
	CONSTRAINT fk_user_role_id_roles FOREIGN KEY(role_id) REFERENCES roles (id), 
	CONSTRAINT uq_user_social UNIQUE (social), 
	CONSTRAINT uq_user_phone_number UNIQUE (phone_number)
);
INSERT INTO user VALUES(1,'Randomdork','randomdork@gmail.com','default.png','$2a$12$/Mo.oG8XhDjlgmhjfk1OYe533ofeEJJR4F1fPhajJjjn7Azij9xuG','Hey there I am using this blog!','2020-08-15 19:18:30.717092',NULL,0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(2,NULL,NULL,'default.png',NULL,'Hey there I am using this blog!','2020-08-16 10:28:14.883220',NULL,0,0,NULL,'facebook$963819807422700',NULL,NULL,NULL);
INSERT INTO user VALUES(3,'test2','test2@GMAIL.COM','default.png','$2a$12$gN7y/b60dMl4VrdpENTOj.MC9Bsu9/36ZTvccoNf5jSpuWPQZQv.C','Hey there I am using this blog!','2020-08-16 10:33:12.221295',NULL,0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(4,'test2a','test2a@gmail.com','default.png','$2a$12$G7BlGEFGZz/8ryImu05XRu8j355VKucVBcQUAMcbKorFbLG3ghFO2','Hey there I am using this blog!','2020-08-16 10:34:34.895268',NULL,0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(5,'Bill','randomdorkbill@gmail.com','default.png','$2a$12$bztFexd6I2uIXqpashp88eBKeOUSoPadPnR7y3LZSCHZvGMJos3Sa','Hey there I am using this blog!','2020-08-16 12:00:20.402091',NULL,0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(6,'rerrererer','rererer@gmail.com','default.png','$2a$12$nAJhnF2XNT/NmZLRk96diuoAAashli7SJz0iTvEYP2MUzS9XVwTZa','Hey there I am using this blog!','2020-08-17 16:14:19.392969',NULL,0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(7,'test','test@st.com','f7cb2edbdc534091.jpeg','$2a$12$VVENAmfWWZQw1ral6ixw5.KqDXo9qSeMg96p1fejyvpBVVLTGW1OC','Hey there I am using this blog!','2020-08-18 07:21:16.088972',NULL,0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(8,'testregister','testregiste@gmairl.coM','default.png','$2a$12$7R4qEAlZWAJ1tJkdbaKxCeZbdEOBAJCknQwrHvP6qUd2HFuc9SR36','Hey there I am using this blog!','2020-08-18 10:01:13.747794','2020-08-18 13:01:13.743209',0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(9,'createaccount','createaccount12@gmail.com','7e367f2ed7e1ffd1.jpeg','$2a$12$yuYSd4Rm2jd3tBejXOfdPuptqXFu51ivGpTtL0OAQxIYyHGBbFOfK','Hey there I am using this blog!','2020-08-20 09:13:07.482279','2020-08-20 12:13:07.474968',0,0,NULL,NULL,NULL,1,NULL);
INSERT INTO user VALUES(10,'adminuser','testflask673@gmail.com','default.png','$2a$12$2rLmOq50cx7/OQ5oGSKICeFU39OFKIcSEfBxM811WK6ZUcAKL/Tzi','Hey there I am using this blog!','2020-08-20 09:56:56.825422','2020-08-20 12:56:56.815981',0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(11,'Matt','matt@gmail.com','default.png','$2a$12$jgX69Lk9aTr6mmqBEbVdkOHmIryHFiVSkrCqvPGCQw45P/65mbrRu','Hey there I am using this blog!','2020-08-21 09:31:41.983322','2020-08-21 12:31:41.975687',0,0,NULL,NULL,NULL,NULL,NULL);
INSERT INTO user VALUES(12,'teatmatt','testmatt@gmail.com','default.png','$2a$12$9MQTwK4Py5kSdofWpxeQ8.89uFgWrekhb.nS9SJZ1dgznJ/Yd6gMK','Hey there I am using this blog!','2020-08-21 13:39:29.439116','2020-08-21 16:39:29.431835',0,0,NULL,NULL,NULL,1,NULL);
INSERT INTO user VALUES(13,'testlocalhost','testlocalhsot@gmail.com','default.png','$2a$12$lVmBPoQuv1yfhlklYZK/T.3Bni8Ti7cwlPK4bmek3Oae2w4RYsiN6','Hey there I am using this blog!','2020-08-22 09:12:48.771188','2020-08-22 12:12:48.762055',0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(14,'tesingadmin','testingadmin@gmail.com','default.png','$2a$12$F/OuPlSYQEPSE8KZSPKWEuX7vJjVtAGZskKlw.SIAW41m1xQm0Kmq','Hey there I am using this blog!','2020-08-23 19:38:08.062226','2020-08-23 22:38:08.051854',0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(15,'williamsriunge','williamsriunge@gmail.com','default.png',NULL,'Hey there I am using this blog!','2020-08-24 10:24:13.747244',NULL,0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(16,'williamsriunge@gmail.com',NULL,'default.png',NULL,'Hey there I am using this blog!','2020-08-24 13:04:58.767774',NULL,0,0,NULL,'google$williamsriunge',NULL,0,NULL);
INSERT INTO user VALUES(17,'randomdorkynig',NULL,'default.png',NULL,'Hey there I am using this blog!','2020-08-24 13:42:17.101886',NULL,0,0,NULL,'twitter$randomdorkynig',NULL,0,NULL);
INSERT INTO user VALUES(18,'testingflaskapp763','testingflaskapp763@gmail.com','https://lh4.googleusercontent.com/-uy2ROABVA-A/AAAAAAAAAAI/AAAAAAAAAAA/AMZuuckXlaH1m07kA0JtJYFJswW_JIjU5g/photo.jpg',NULL,'Hey there I am using this blog!','2020-08-24 14:08:52.330803',NULL,0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(19,'testingcreate','testingcreateaccount@gmail.com','default.png','$2a$12$XYNKW9Rxwxv/fCVVpTZdx.1P8LXAwyNni08tm2UdMmwmGTm3qgHhK','Hey there I am using this blog!','2020-08-24 16:01:19.927520','2020-08-24 19:01:19.924905',0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(20,'text','text@gmail.com','default.png','$2a$12$EUGV.JTJghsLmQikC8LLW.hzwCIdcei7X9kJWGfpD.fr0Gp0/VwGa','Hey there I am using this blog!','2020-08-25 11:48:40.057320','2020-08-25 14:48:40.053319',0,0,NULL,NULL,NULL,0,NULL);
INSERT INTO user VALUES(21,'TESTINFAWS','testingaws@gmail.com','f86d8afffe25d50f.png','$2a$12$/v77mIhlyEtsph9HOYskCOJa/Dg2WT/J6.3qC4vvIOJszt1SJTMJq','Hey there I am using this blog!','2020-08-25 19:30:37.252598','2020-08-25 22:30:37.248872',0,0,NULL,NULL,NULL,0,NULL);
CREATE INDEX ix_post_date_posted ON post (date_posted);
CREATE INDEX ix_roles_default ON roles ("default");
CREATE UNIQUE INDEX ix_user_username ON user (username);
CREATE UNIQUE INDEX ix_user_email ON user (email);
COMMIT;
