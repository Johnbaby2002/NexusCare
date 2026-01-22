-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2026 at 12:59 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ehr_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL,
  `doctorid` int(11) NOT NULL,
  `patientid` int(11) NOT NULL,
  `appt_date` date NOT NULL,
  `appt_time` varchar(5) DEFAULT NULL,
  `status` enum('Scheduled','Visited','Cancelled') NOT NULL DEFAULT 'Scheduled',
  `diagnosis` varchar(255) DEFAULT NULL,
  `report` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `doctorid`, `patientid`, `appt_date`, `appt_time`, `status`, `diagnosis`, `report`, `created_at`, `updated_at`) VALUES
(1, 1, 2, '2026-01-17', '11:45', 'Scheduled', NULL, NULL, '2026-01-18 16:12:11', NULL),
(2, 1, 4, '2025-01-08', NULL, 'Scheduled', NULL, NULL, '2026-01-18 16:12:11', NULL),
<<<<<<< HEAD
(4, 1, 7, '2026-01-20', '08:45', 'Scheduled', NULL, NULL, '2026-01-18 23:22:27', NULL),
(5, 1, 8, '2026-01-21', '12:00', 'Scheduled', NULL, NULL, '2026-01-19 16:41:11', NULL);
=======
(4, 1, 7, '2026-01-20', '08:45', 'Scheduled', NULL, NULL, '2026-01-18 23:22:27', NULL);
>>>>>>> f84a6bd (changes to dashboard,base.html)

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `doctor_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`doctor_id`, `name`, `email`, `password_hash`, `created_at`) VALUES
(1, 'John Baby Nayathodan', 'johnnayathodan@gmail.com', '$2b$12$sUIUrxvQxsYaaxnJkj6JV.bFvoZmVwDeUILlFLvZchGa0KQ1nmvmG', '2026-01-14 16:00:40');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `patientid` int(11) NOT NULL,
  `doctorid` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `dateofbirth` date NOT NULL,
  `weight` decimal(5,1) DEFAULT NULL,
  `height` decimal(5,1) DEFAULT NULL,
  `visit_date` date DEFAULT NULL,
  `smoker` tinyint(1) NOT NULL DEFAULT 0,
  `allergies` text DEFAULT NULL,
  `radiology_image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `symptoms` text DEFAULT NULL,
  `visited` tinyint(1) NOT NULL DEFAULT 0,
  `visit_time` varchar(5) DEFAULT NULL,
  `diagnosis` text DEFAULT NULL,
  `soap_subjective` text DEFAULT NULL,
  `soap_objective` text DEFAULT NULL,
  `soap_assessment` text DEFAULT NULL,
  `soap_plan` text DEFAULT NULL,
  `is_revisit` tinyint(4) DEFAULT 0,
<<<<<<< HEAD
  `revisit_from` int(11) DEFAULT NULL
=======
  `revisit_from` int(11) DEFAULT NULL,
  `billing_amount` decimal(10,2) DEFAULT NULL,
  `billing_status` varchar(30) DEFAULT NULL,
  `billing_notes` text DEFAULT NULL
>>>>>>> f84a6bd (changes to dashboard,base.html)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

<<<<<<< HEAD
INSERT INTO `patients` (`patientid`, `doctorid`, `name`, `gender`, `dateofbirth`, `weight`, `height`, `visit_date`, `smoker`, `allergies`, `radiology_image`, `created_at`, `updated_at`, `symptoms`, `visited`, `visit_time`, `diagnosis`, `soap_subjective`, `soap_objective`, `soap_assessment`, `soap_plan`, `is_revisit`, `revisit_from`) VALUES
(2, 1, 'John Baby Nayathodan', 'Male', '2004-01-06', 100.0, 181.0, '2026-01-17', 1, 'Peanuts, Pollen', 'doc1_20260114202514_WhatsApp_Image_2026-01-06_at_12.31.57_5.jpeg', '2026-01-14 19:25:14', '2026-01-19 20:03:00', '', 1, '11:45', NULL, NULL, NULL, NULL, NULL, 0, NULL),
(4, 1, 'John Nayathodan', 'Male', '2004-01-05', 68.0, 181.0, '2025-01-08', 1, 'None', NULL, '2026-01-14 20:33:30', '2026-01-19 20:03:00', 'ear pain', 1, '08:00', NULL, NULL, NULL, NULL, NULL, 0, NULL),
(5, 1, 'robert will', 'Male', '2005-01-13', 49.4, 173.0, '2026-01-22', 1, 'Peanuts', NULL, '2026-01-18 19:13:02', NULL, 'Sore throat', 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
(6, 1, 'John Baby Nayathodan', 'Male', '2006-01-05', 88.0, 188.0, '2026-01-20', 1, 'None', NULL, '2026-01-18 22:30:58', '2026-01-18 22:51:44', 'Dizziness', 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
(7, 1, 'John Baby Nayathodan', 'Male', '2003-01-07', 177.0, NULL, NULL, 0, 'Dust, Latex, Pollen', NULL, '2026-01-18 23:22:27', NULL, 'Headache', 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
(8, 1, 'John Baby Nayathodan', 'Male', '2002-02-05', 90.0, NULL, NULL, 0, 'Dust, Latex, Pollen', NULL, '2026-01-19 16:41:11', NULL, 'Nausea', 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
(9, 1, 'Tobias', 'Male', '2003-01-17', 98.0, 176.0, '2026-01-26', 1, 'Peanuts, Dust', NULL, '2026-01-19 18:45:40', '2026-01-19 20:56:45', 'Nausea , Rashes', 0, NULL, '', '', '', '', '', 1, 9),
(10, 1, 'Tobias', 'Male', '2007-01-10', 99.0, 176.0, '2026-01-15', 1, 'Gluten', NULL, '2026-01-19 22:00:56', '2026-01-19 22:00:56', 'Dizziness', 1, '11:45', '', '', '', '', '', 0, NULL),
(11, 1, 'Tobias', 'Male', '2007-01-10', 99.0, 176.0, '2026-01-26', 1, 'Gluten', NULL, '2026-01-19 22:01:22', NULL, 'Dizziness', 0, NULL, NULL, NULL, NULL, NULL, NULL, 1, 10),
(12, 1, 'Tobias', 'Male', '2003-01-08', 78.0, 177.0, '2026-01-19', 1, 'Peanuts, Gluten', NULL, '2026-01-20 10:39:10', '2026-01-20 10:39:10', 'Dizziness', 1, '11:15', '', '', '', '', '', 0, NULL),
(13, 1, 'robert will', 'Male', '1997-01-12', 88.0, 178.0, '2026-01-20', 1, 'Peanuts, Latex', NULL, '2026-01-20 10:44:21', NULL, 'Nausea', 0, '16:30', '', '', '', '', '', 0, NULL);
=======
INSERT INTO `patients` (`patientid`, `doctorid`, `name`, `gender`, `dateofbirth`, `weight`, `height`, `visit_date`, `smoker`, `allergies`, `radiology_image`, `created_at`, `updated_at`, `symptoms`, `visited`, `visit_time`, `diagnosis`, `soap_subjective`, `soap_objective`, `soap_assessment`, `soap_plan`, `is_revisit`, `revisit_from`, `billing_amount`, `billing_status`, `billing_notes`) VALUES
(2, 1, 'John Baby Nayathodan', 'Male', '2004-01-06', 100.0, 181.0, '2026-01-17', 1, 'Peanuts, Pollen', 'doc1_20260114202514_WhatsApp_Image_2026-01-06_at_12.31.57_5.jpeg', '2026-01-14 19:25:14', '2026-01-19 20:03:00', '', 1, '11:45', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL),
(4, 1, 'John Nayathodan', 'Male', '2004-01-05', 68.0, 181.0, '2025-01-08', 1, 'None', NULL, '2026-01-14 20:33:30', '2026-01-19 20:03:00', 'ear pain', 1, '08:00', NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL),
(5, 1, 'robert will', 'Male', '2005-01-13', 49.4, 173.0, '2026-01-22', 1, 'Peanuts', NULL, '2026-01-18 19:13:02', NULL, 'Sore throat', 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL),
(6, 1, 'John Baby Nayathodan', 'Male', '2006-01-05', 88.0, 188.0, '2026-01-20', 1, 'None', NULL, '2026-01-18 22:30:58', '2026-01-21 11:59:40', 'Dizziness', 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL),
(7, 1, 'John Baby Nayathodan', 'Male', '2003-01-07', 177.0, NULL, NULL, 0, 'Dust, Latex, Pollen', NULL, '2026-01-18 23:22:27', NULL, 'Headache', 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL),
(9, 1, 'Tobias', 'Male', '2003-01-17', 98.0, 176.0, '2026-01-26', 1, 'Peanuts, Dust', NULL, '2026-01-19 18:45:40', '2026-01-19 20:56:45', 'Nausea , Rashes', 0, NULL, '', '', '', '', '', 1, 9, NULL, NULL, NULL),
(10, 1, 'Tobias', 'Male', '2007-01-10', 99.0, 176.0, '2026-01-15', 1, 'Gluten', NULL, '2026-01-19 22:00:56', '2026-01-19 22:00:56', 'Dizziness', 1, '11:45', '', '', '', '', '', 0, NULL, NULL, NULL, NULL),
(11, 1, 'Tobias', 'Male', '2007-01-10', 99.0, 176.0, '2026-01-26', 1, 'Gluten', NULL, '2026-01-19 22:01:22', NULL, 'Dizziness', 0, NULL, NULL, NULL, NULL, NULL, NULL, 1, 10, NULL, NULL, NULL),
(12, 1, 'Tobias', 'Male', '2003-01-08', 78.0, 177.0, '2026-01-19', 1, 'Peanuts, Gluten', NULL, '2026-01-20 10:39:10', '2026-01-20 10:39:10', 'Dizziness', 1, '11:15', '', '', '', '', '', 0, NULL, NULL, NULL, NULL),
(13, 1, 'robert will', 'Male', '1997-01-12', 88.0, 178.0, '2026-01-20', 1, 'Peanuts, Latex', NULL, '2026-01-20 10:44:21', '2026-01-21 11:59:40', 'Nausea', 1, '16:30', '', '', '', '', '', 0, NULL, NULL, NULL, NULL),
(14, 1, 'John Baby Nayathodan', 'Male', '2006-01-05', 88.0, 188.0, '2026-01-28', 1, 'None', NULL, '2026-01-21 11:59:56', NULL, 'Dizziness', 0, NULL, NULL, NULL, NULL, NULL, NULL, 1, 6, NULL, NULL, NULL),
(15, 1, 'John Baby Nayathodan', 'Male', '2003-01-01', 88.0, 187.0, '2026-01-20', 1, 'Peanuts, Dust', NULL, '2026-01-21 12:06:28', '2026-01-21 12:06:28', 'Shortness of breath', 1, '12:00', '', '', '', '', '', 0, NULL, NULL, NULL, NULL),
(18, 1, 'John Baby Nayathodan', 'Male', '2003-01-01', 88.0, 187.0, '2026-01-29', 1, 'Peanuts, Dust', NULL, '2026-01-22 08:19:56', NULL, 'Shortness of breath', 0, NULL, NULL, NULL, NULL, NULL, NULL, 1, 15, NULL, NULL, NULL),
(19, 1, 'Tom smith', 'Male', '2013-01-03', 99.0, 187.0, '2026-01-22', 1, 'Peanuts, Dust, Latex', 'doc1_p19_20260122094842_Screenshot_2024-01-31_102700.png', '2026-01-22 08:21:01', '2026-01-22 08:48:42', 'Chest pain', 0, '16:00', '', '', '', '', '', 0, NULL, NULL, NULL, NULL),
(21, 1, 'Tobias', 'Male', '2026-01-01', 88.0, 167.0, '2026-01-22', 0, 'Peanuts', 'doc1_p21_20260122115328_bd64cf28-498e-44df-be77-3e74cd079783-featured-49f3a3c3ecd5bdb5a10037c1b80de2ff.jpg', '2026-01-22 10:53:05', '2026-01-22 10:53:28', '', 0, '12:15', '', NULL, NULL, NULL, NULL, 0, NULL, 99.00, 'Pending', NULL),
(22, 1, 'Joyel Raju', 'Male', '2002-01-01', 88.0, 178.0, '2026-01-22', 1, 'Peanuts', 'doc1_20260122123459_bd64cf28-498e-44df-be77-3e74cd079783-featured-49f3a3c3ecd5bdb5a10037c1b80de2ff.jpg', '2026-01-22 11:34:59', '2026-01-22 11:36:43', 'Chest pain', 0, '10:15', '', NULL, NULL, NULL, NULL, 0, NULL, 899.00, 'Insurance', NULL),
(23, 1, 'John Baby Nayathodan', 'Male', '2003-01-01', 88.0, 187.0, '2026-01-29', 1, 'Peanuts, Dust', NULL, '2026-01-22 11:35:29', NULL, 'Shortness of breath', 0, NULL, NULL, NULL, NULL, NULL, NULL, 1, 15, NULL, NULL, NULL);
>>>>>>> f84a6bd (changes to dashboard,base.html)

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD KEY `idx_appt_doctor_date` (`doctorid`,`appt_date`,`appt_time`),
  ADD KEY `idx_appt_patient` (`patientid`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`doctor_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`patientid`),
  ADD KEY `idx_patients_doctorid` (`doctorid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `doctor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
<<<<<<< HEAD
  MODIFY `patientid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
=======
  MODIFY `patientid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
>>>>>>> f84a6bd (changes to dashboard,base.html)

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `fk_appt_doctor` FOREIGN KEY (`doctorid`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_appt_patient` FOREIGN KEY (`patientid`) REFERENCES `patients` (`patientid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `fk_patients_doctor` FOREIGN KEY (`doctorid`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
