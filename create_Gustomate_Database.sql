-- 기존 데이터베이스 삭제
DROP DATABASE IF EXISTS gustomate;

-- 데이터베이스 생성
CREATE DATABASE gustomate;
USE gustomate;

-- users 테이블 생성
CREATE TABLE `users` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(100) DEFAULT NULL,
    `useremail` varchar(100) DEFAULT NULL,
    `password` varchar(100) DEFAULT NULL,
    `profile_image` varchar(100) DEFAULT NULL,
    `location` varchar(100) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- admin 테이블 생성
CREATE TABLE `admins` (
    `admin_id` int(11) NOT NULL AUTO_INCREMENT,
    `adminname` varchar(100) DEFAULT NULL,
    `adminemail` varchar(100) DEFAULT NULL,
    `adminpassword` varchar(100) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- user_preferences 테이블 생성
CREATE TABLE `user_preferences` (
    `user_preferences_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) DEFAULT NULL,
    `spiciness_preference` int(11) DEFAULT NULL,
    `cooking_skill` varchar(100) DEFAULT NULL,
    `fridge_public` boolean DEFAULT NULL,
    `notification_enabled` boolean DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`user_preferences_id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- chats 테이블 생성
CREATE TABLE `chats` (
    `chat_id` int(11) NOT NULL AUTO_INCREMENT,
    `user1_id` int(11) NOT NULL,
    `user2_id` int(11) NOT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`chat_id`),
    FOREIGN KEY (`user1_id`) REFERENCES users(`user_id`),
    FOREIGN KEY (`user2_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- recipes 테이블 생성
CREATE TABLE `recipes` (
    `recipe_id` int(11) NOT NULL AUTO_INCREMENT,
    `recipe_name` varchar(100) DEFAULT NULL,
    `image` varchar(100) DEFAULT NULL,
    `method_classification` varchar(100) DEFAULT NULL,
    `country_classification` varchar(100) DEFAULT NULL,
    `theme_classification` varchar(100) DEFAULT NULL,
    `difficulty_classification` varchar(100) DEFAULT NULL,
    `calorie` INT(11) DEFAULT NULL,
    `view` INT(11) DEFAULT NULL,
    `quantity` INT(11) DEFAULT NULL,
    `main_ingredients` TEXT DEFAULT NULL,
    `sub_ingredients` TEXT DEFAULT NULL,
    `seasonings` TEXT DEFAULT NULL,
    `recipe` TEXT DEFAULT NULL,
    `cooking_time` INT DEFAULT NULL,
    `spiciness` INT(11) DEFAULT NULL,
    PRIMARY KEY (`recipe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- recipe_reviews 테이블 생성
CREATE TABLE `recipe_reviews` (
    `review_id` int(11) NOT NULL AUTO_INCREMENT,
    `recipe_id` int(11) DEFAULT NULL,
    `user_id` int(11) DEFAULT NULL,
    `review_header` varchar(100) DEFAULT NULL,
    `review_text` text DEFAULT NULL,
    `rating` int(11) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`review_id`),
    FOREIGN KEY (`recipe_id`) REFERENCES recipes(`recipe_id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- market 테이블 생성
CREATE TABLE `market` (
    `market_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) DEFAULT NULL,
    `ingredient_id` varchar(100) DEFAULT NULL,
    `market_image` varchar(100) DEFAULT NULL,
    `market_description` TEXT DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`market_id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
    FOREIGN KEY (`ingredient_id`) REFERENCES ingredients(`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- friends 테이블 생성
CREATE TABLE `friends` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `friend_id` int(11) NOT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
    FOREIGN KEY (`friend_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- token_blacklist 테이블 생성
CREATE TABLE `token_blacklist` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `jti` varchar(255) NOT NULL,
    `exp` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- 테스트 유저 생성
INSERT INTO users (username, useremail, password, profile_image, location, created_at, updated_at)
VALUES 
('testuser1', 'testuser1@example.com', 'password123', 'profile_image_url', 'Seoul', NOW(), NOW()),
('testuser2', 'testuser2@example.com', 'password123', 'profile_image_url', 'Seoul', NOW(), NOW()),
('testuser3', 'testuser3@example.com', 'password123', 'profile_image_url', 'Seoul', NOW(), NOW());

-- 관리자 생성
INSERT INTO admins (adminname, adminemail, adminpassword, created_at, updated_at)
VALUES ('admin', 'admin@example.com', 'adminpassword123', NOW(), NOW());

-- 예시 친구 관계 데이터 삽입
INSERT INTO friends (user_id, friend_id, created_at, updated_at)
VALUES
(1, 2, NOW(), NOW()),
(1, 3, NOW(), NOW()),
(2, 3, NOW(), NOW());