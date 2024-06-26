CREATE DATABASE gustomate;
use gustomate;
CREATE TABLE `users` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(100) DEFAULT NULL,
    `email` varchar(100) DEFAULT NULL,
    `password` varchar(100) DEFAULT NULL,
    `profile_image` varchar(100) DEFAULT NULL,
    `location` varchar(100) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`user_id`)
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

-- recipe 테이블 생성
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
    `review_header` varchar(100) DEFAULT NULL,
    `review_text` text DEFAULT NULL,
    `rating` int(11) DEFAULT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    PRIMARY KEY (`review_id`),
    FOREIGN KEY (`recipe_id`) REFERENCES recipes(`recipe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

