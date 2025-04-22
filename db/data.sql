-- Insert physician data
INSERT INTO physician (physician_name) VALUES
('Dr. Sarah Johnson'),
('Dr. Michael Chen'),
('Dr. Emily Wilson'),
('Dr. Robert Garcia'),
('Dr. Jennifer Lee');

-- Insert patient data
INSERT INTO patient (id, patient_name, date_of_birth, gender) VALUES
('1', 'Emma Thompson', '1985-03-15', 'female'),
('2', 'Olivia Martinez', '1978-07-22', 'female'),
('3', 'Sophia Rodriguez', '1992-11-05', 'female'),
('4', 'James Wilson', '1982-09-18', 'male'),
('5', 'Ava Anderson', '1995-04-30', 'female'),
('6', 'Isabella Brown', '1988-12-14', 'female'),
('7', 'Mia Garcia', '1975-06-27', 'female'),
('8', 'William Taylor', '1990-02-09', 'male'),
('9', 'Benjamin Davis', '1983-08-23', 'male'),
('10', 'Lucas Miller', '1972-05-11', 'male'),
('11', 'Alexander Moore', '1998-10-03', 'male'),
('12', 'Henry White', '1987-01-26', 'male'),
('13', 'Daniel Jackson', '1993-07-19', 'male'),
('14', 'Samuel Harris', '1980-04-08', 'male'),
('15', 'Charlotte Clark', '1979-09-21', 'female'),
('16', 'Ethan Lewis', '1991-03-04', 'male'),
('17', 'Matthew Walker', '1986-11-17', 'male'),
('20', 'Amelia Hall', '1984-08-12', 'female');

-- Insert scan data
INSERT INTO scan (patient_id, scan_datetime, consent_given, image_path, referring_physician_id) VALUES
('1', '2023-01-10 09:15:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/1_F_anger5.jpg', 1),
('2', '2023-01-11 10:30:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/2_F_happiness2.jpg', 2),
('3', '2023-01-12 11:45:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/3_F_g1.png', 3),
('4', '2023-01-13 13:00:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/4_M_aug_0_18.jpg', 4),
('5', '2023-01-14 14:15:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/5_F_paralysis.png', 1),
('6', '2023-01-15 15:30:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/6_F_anger22.jpg', 2),
('7', '2023-01-16 16:45:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/7_F_happiness3.jpg', 3),
('8', '2023-01-17 09:00:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/8_M_g2.png', 4),
('9', '2023-01-18 10:15:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/9_M_anger36.jpg', 1),
('10', '2023-01-19 11:30:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/10_M_paralysis.png', 2),
('11', '2023-01-20 12:45:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/11_M_anger37.jpg', 3),
('12', '2023-01-21 14:00:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/12_M_happiness9.jpg', 4),
('13', '2023-01-22 15:15:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/13_M_aug_0_427.jpg', 1),
('14', '2023-01-23 16:30:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/14_M_happiness34.jpg', 2),
('15', '2023-01-24 09:45:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/15_F_paralysis.png', 3),
('16', '2023-01-25 11:00:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/16_M_anger56.jpg', 4),
('17', '2023-01-26 12:15:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/17_M_g3.png', 1),
('20', '2023-01-27 13:30:00', TRUE, 'C:/shared/anjali/facial_paralysis/streamer/input/20_F_paralysis.png', 2);