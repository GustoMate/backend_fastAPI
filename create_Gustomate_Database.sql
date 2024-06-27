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

-- cuisines 테이블 생성
CREATE TABLE `cuisines` (
    `cuisine_id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(100) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`cuisine_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- recipes 테이블 생성
CREATE TABLE `recipes` (
    `recipe_id` int(11) NOT NULL AUTO_INCREMENT,
    `recipe_name` varchar(100) DEFAULT NULL,
    `image` varchar(100) DEFAULT NULL,
    `difficulty` int(11) DEFAULT NULL,
    `steps` varchar(1000) DEFAULT NULL,
    `cuisine_id` int(11) DEFAULT NULL,
    `spiciness` int(11) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`recipe_id`),
    FOREIGN KEY (`cuisine_id`) REFERENCES cuisines(`cuisine_id`)
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


-- Ingredient 테이블 생성
CREATE TABLE IF NOT EXISTS ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    purchaseDate DATE NOT NULL,
    expiryDate DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


-- token_blacklist 테이블 생성
CREATE TABLE `token_blacklist` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `jti` varchar(255) NOT NULL,
    `exp` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


-- 테스트 유저 생성
INSERT INTO users (username, useremail, password, profile_image, location, created_at, updated_at) 
VALUES ('testuser', 'testuser@example.com', 'password123', 'profile_image_url', 'Seoul', NOW(), NOW());

-- 관리자 생성
INSERT INTO admins (adminname, adminemail, adminpassword, created_at, updated_at)
VALUES ('admin', 'admin@example.com', 'adminpassword123', NOW(), NOW());

-- 추가 예시 레시피 데이터 삽입
INSERT INTO cuisines (name, created_at, updated_at) 
VALUES 
('한식', NOW(), NOW()),
('일식', NOW(), NOW()),
('이탈리아식', NOW(), NOW());

-- 예시 레시피 데이터 삽입
INSERT INTO recipes (recipe_name, image, difficulty, steps, cuisine_id, spiciness, created_at, updated_at) 
VALUES 
('매운 김치 찌개', 'kimchi_stew.jpg', 3, '1. 냄비에 기름을 두르고 달군다.\n2. 김치를 넣고 볶는다.\n3. 물을 붓고 끓인다.\n4. 두부를 넣고 끓인다.', 1, 4, NOW(), NOW()),
('일본식 스시 롤', 'sushi_rolls.jpg', 2, '1. 스시밥을 준비한다.\n2. 김을 대나무 매트에 깐다.\n3. 밥을 펴고 속재료를 올린다.\n4. 김밥처럼 말아서 자른다.', 2, 1, NOW(), NOW()),
('이탈리아 스파게티 카르보나라', 'spaghetti_carbonara.jpg', 2, '1. 스파게티를 삶는다.\n2. 판체타를 볶는다.\n3. 계란과 치즈를 섞는다.\n4. 스파게티와 판체타, 계란 혼합물을 섞는다.', 3, 0, NOW(), NOW()),
('한식 불고기', 'korean_bbq_beef.jpg', 3, '1. 소고기를 양념에 재운다.\n2. 소고기를 구워준다.\n3. 상추쌈과 함께 제공한다.', 1, 3, NOW(), NOW()),
('일본식 라멘', 'ramen.jpg', 4, '1. 면을 삶는다.\n2. 육수를 준비한다.\n3. 면과 육수, 토핑을 함께 제공한다.', 2, 2, NOW(), NOW()),
('이탈리아 마르게리타 피자', 'margherita_pizza.jpg', 2, '1. 도우를 준비한다.\n2. 토마토 소스를 바른다.\n3. 모짜렐라와 바질을 올린다.\n4. 오븐에 구워준다.', 3, 0, NOW(), NOW());

-- 예시 레시피 리뷰 데이터 삽입
INSERT INTO recipe_reviews (recipe_id, user_id, review_header, review_text, rating, created_at, updated_at)
VALUES 
(1, 1, '매운 김치 찌개 최고!', '이 레시피로 만든 김치찌개는 정말 맛있었어요. 강추합니다!', 5, NOW(), NOW()),
(2, 1, '일본식 스시 롤', '스시 롤 만들기 정말 간단하고 맛있어요. 재료 준비만 잘 하면 쉽게 만들 수 있어요.', 4, NOW(), NOW()),
(3, 1, '스파게티 카르보나라', '카르보나라를 처음 만들어봤는데 이 레시피 덕분에 성공했어요! 가족들도 좋아했어요.', 5, NOW(), NOW()),
(1, 1, '매운 김치 찌개 아주 좋아요', '매운 음식을 좋아하는 사람들에게 딱입니다. 간편하게 만들 수 있어요.', 5, NOW(), NOW()),
(2, 1, '맛있는 스시 롤', '간단한 레시피로도 훌륭한 스시 롤을 만들 수 있네요. 재료만 신선하면 최고!', 4, NOW(), NOW()),
(3, 1, '카르보나라 레시피 강추', '집에서 쉽게 만들 수 있어서 좋았습니다. 다음에도 이 레시피로 만들 것 같아요.', 5, NOW(), NOW());


-- 예시 친구 관계 데이터 삽입
INSERT INTO friends (user_id, friend_id, created_at, updated_at)
VALUES 
(1, 2, NOW(), NOW()),
(1, 3, NOW(), NOW()),
(2, 3, NOW(), NOW());


INSERT INTO ingredients (user_id, name, quantity, purchaseDate, expiryDate)
VALUES
(0, potato, 3, 2024-01-01, 2024-01-01);
