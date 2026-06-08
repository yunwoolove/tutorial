create database memories;
use memories;
CREATE DATABASE memories;
USE memories;

-- 1. 유저 테이블 (이름 글자수 제한 완화, 비밀번호 암호화 대비 글자수 확장)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL -- 비밀번호 해시 암호화를 위해 늘려야 합니다.
);

-- 2. 카테고리 테이블
CREATE TABLE category (
    cate_id INT AUTO_INCREMENT PRIMARY KEY,
    cate_name VARCHAR(50) NOT NULL -- 혹시 모를 긴 카테고리명 대비
);

-- 3. 리뷰 테이블 (정규화: 중복되는 score 제거, rating 하나로 통합)
CREATE TABLE review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL, -- 제목 글자수 확장
    cate_id INT NOT NULL,
    picture VARCHAR(255), -- 이미지 URL 구조 대비 확장
    link VARCHAR(255),    -- 웹 링크 주소 대비 확장
    writing TEXT NOT NULL, -- VARCHAR(100)은 너무 짧아서 글이 안 써짐 -> TEXT 타입으로 변경
    rating DECIMAL(2, 1) UNSIGNED NOT NULL CHECK (rating BETWEEN 0.0 AND 5.0), -- 평점 단일화
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 데이터 입력 시 자동으로 시간 저장되게 설정
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (cate_id) REFERENCES category(cate_id) ON DELETE CASCADE
);

-- 4. 댓글 테이블
CREATE TABLE comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    review_id INT NOT NULL,
    comment VARCHAR(255) NOT NULL, -- 댓글 100자 제한 완화
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 댓글 쓴 시간 추가
    FOREIGN KEY (review_id) REFERENCES review(review_id) ON DELETE CASCADE
);
INSERT INTO category (cate_name)
VALUES 
    ('영화'),
    ('드라마'),
    ('노래');
