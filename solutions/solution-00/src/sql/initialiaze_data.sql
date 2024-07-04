-- src/sql/initial_data.sql

-- Insert initial data into countries
INSERT INTO countries (id, name, code) VALUES
('1', 'France', 'FR'),
('2', 'Germany', 'DE');

-- Insert initial data into cities
INSERT INTO cities (id, name, country_id) VALUES
('1', 'Paris', '1'),
('2', 'Berlin', '2');

-- Insert initial data into users
INSERT INTO users (id, email, first_name, last_name, password_hash, is_admin) VALUES
('1', 'admin@example.com', 'Admin', 'User', 'hashed_password', TRUE),
('2', 'user@example.com', 'Regular', 'User', 'hashed_password', FALSE);

-- Insert initial data into places
INSERT INTO places (id, name, description, user_id) VALUES
('1', 'Eiffel Tower', 'A famous tower in Paris', '1');

-- Insert initial data into reviews
INSERT INTO reviews (id, place_id, user_id, comment, rating) VALUES
('1', '1', '2', 'Amazing place!', 5);

-- Insert initial data into amenities
INSERT INTO amenities (id, name) VALUES
('1', 'Free WiFi'),
('2', 'Swimming Pool');
