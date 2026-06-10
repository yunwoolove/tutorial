create database memories;
use memories;
CREATE DATABASE memories;
USE memories;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE category (
    cate_id INT AUTO_INCREMENT PRIMARY KEY,
    cate_name VARCHAR(50) NOT NULL 
);

-- 리뷰 테이블
CREATE TABLE review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    cate_id INT NOT NULL,
    picture VARCHAR(255), 
    link VARCHAR(255),    
    writing TEXT NOT NULL, 
    rating DECIMAL(2, 1) UNSIGNED NOT NULL CHECK (rating BETWEEN 0.0 AND 5.0), 
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (cate_id) REFERENCES category(cate_id) ON DELETE CASCADE
);

-- 4. 댓글 테이블
CREATE TABLE comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    review_id INT NOT NULL,
    comment VARCHAR(255) NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (review_id) REFERENCES review(review_id) ON DELETE CASCADE
);
INSERT INTO category (cate_name)
VALUES 
    ('영화'),
    ('드라마'),
    ('노래');
