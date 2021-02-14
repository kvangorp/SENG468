CREATE DATABASE ariesdb;
USE ariesdb;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS stock_acct;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS triggers;

CREATE TABLE users (   
	id VARCHAR(20) NOT NULL,
	balance FLOAT NOT NULL 
) engine=ColumnStore;

CREATE TABLE stock_acct (
	userID VARCHAR(20),
	stock_symbol VARCHAR(3) NOT NULL,
	amount INT NOT NULL
) engine=ColumnStore;

CREATE TABLE transactions (
	transaction_number BIGINT NOT NULL COMMENT 'autoincrement=1',
	transaction_time DATETIME NOT NULL,
	userID VARCHAR(20) NOT NULL,
	stock_symbol VARCHAR(3) NOT NULL,
	amount FLOAT NOT NULL,
	price FLOAT NOT NULL,
	type VARCHAR(3) NOT NULL,
	crypto_key VARCHAR(20) NOT NULL
) engine=ColumnStore;

CREATE TABLE triggers (
	userID VARCHAR(20) NOT NULL,
	stock_symbol VARCHAR(3) NOT NULL,
	trigger_type VARCHAR(5) NOT NULL,
	trigger_amount FLOAT NOT NULL,
	transaction_amount FLOAT NOT NULL,
    transaction_number INT
) engine=ColumnStore;
