drop table if exists emulate_data;

create table emulate_data(
  	id  INTEGER,
	ts	varchar(30),
    uid	varchar(30),
    orig_h	varchar(20),
  	orig_p	varchar(15),
  	resp_h	varchar(20),
  	resp_p	varchar(15),
  	proto	varchar(10),
  	service	varchar(15),
  	duration varchar(15),
  	orig_bytyes	varchar(15),
  	resp_bytes	varchar(15),
  	conn_state	varchar(10),
  	local_orig	varchar(15),
  	local_resp	varchar(15),
  	missed_bytes varchar(10),
  	history	varchar(15),
  	orig_pkts varchar(15),
  	orig_ip_bytes varchar(20),
   	resp_pkts varchar(15),
  	resp_ip_bytes varchar(20),
  	label varchar(50)
);