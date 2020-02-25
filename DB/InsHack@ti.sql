drop table if exists users;
drop table if exists teams;
drop table if exists challenges;
drop table if exists patches;
drop table if exists exploits;
drop table if exists flags;

create table users (
  id integer primary key autoincrement,
  name text unique not null,
  username text unique not null,
  password text not null
);

create table teams (
  id integer primary key autoincrement,
  name text unique not null,
  ip text unique not null,
  enabled boolean default 1
);

create table challenges (
  id integer primary key autoincrement,
  name text not null,
  port integer not null
);

create table patches (
  id integer primary key autoincrement,
  name text,
  version text not null,
  description text not null,
  path text unique not null,
  timestamp datetime not null default current_timestamp,

  user_id integer not null,
  challenge_id integer not null
);

create table exploits (
  id integer primary key autoincrement,
  version text not null,
  command text not null,
  path text unique not null,
  timestamp datetime not null default current_timestamp,
  enabled boolean not null default 1,

  user_id integer not null,
  challenge_id integer not null
);

create table flags (
  id integer primary key autoincrement,
  flag text not null,
  submitted boolean not null default 0,
  status text not null default 'NOT SUBMITTED',
  timestamp datetime not null default current_timestamp,

  exploit_id integer not null,
  team_id integer not null
);

insert into users ( name, username, password ) values ( 'Samuele', 'D3xter98', 'pbkdf2:sha256:150000$u3jbdFAX$577e026d6efa8761b5a7646baf98098552ff4cb9a339c14fc84a3f8aa6d5240e' );
insert into users ( name, username, password ) values ( 'Massimo', 'Damax', 'pbkdf2:sha256:150000$vqiYUsvL$678b1d341838e8d49d31ebbae82d3d0209bf12fb8bbb0dff0bc0ab3453c98788' );
insert into users ( name, username, password ) values ( 'Kevin', 'kevincela', 'pbkdf2:sha256:150000$hjQmTJIN$58d3b98b59ebe393f30cb5376b175c216f594407cfdba7259792b534848b7e5e' );
insert into users ( name, username, password ) values ( 'Began', 'Dyrem', 'pbkdf2:sha256:150000$ojdqjuqG$9080328d1f7f1869120cdacd11c90bbabe1f75b1a56e7e8abfa3e333482069a5' );
