-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 02, 2023 at 04:21 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appkesmental`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `category` varchar(100) NOT NULL,
  `link` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `content`, `category`, `link`) VALUES
(3, 'Mengenal Pentingnya Kesehatan Mental pada Remaja', 'Pengertian Kesehatan Mental\r\n\r\nKesehatan mental merupakan kondisi dimana individu memiliki kesejahteraan yang tampak dari dirinya yang mampu menyadari potensinya sendiri, memiliki kemampuan untuk mengatasi tekanan hidup normal pada berbagai situasi dalam kehidupan, mampu bekerja secara produktif dan menghasilkan, serta mampu memberikan kontribusi kepada komunitasnya.\r\n\r\nGejala Gangguan Mental\r\n\r\nBerikut adalah beberapa gejala atau tanda penyakit mental yang mungkin terjadi pada anak :\r\n\r\n1. Perubahan perilaku\r\n\r\nIni merupakan tanda munculnya penyakit mental pada anak yang tergolong mudah Anda sadari melalui aktivitas sehari-hari baik di rumah maupun di sekolah. Ketika anak menjadi lebih sering bertengkar, cenderung kasar, hingga berkata kasar yang menyakitkan orang lain padahal sebelumnya tidak, Anda perlu curiga. Tak hanya itu saja, Anda juga mungkin melihat perubahan perilaku anak seperti menjadi lebih mudah marah dan merasa frustasi.\r\n\r\n2. Perubahan mood\r\n\r\nTanda penyakit mental lainnya adalah mood atau suasana hati anak yang berubah secara tiba-tiba. Kondisi ini bisa berlangsung sebentar hingga dalam jangka waktu yang tidak menentu.\r\n\r\nTentunya, hal ini bisa mengakibatkan masalah pada hubungan dengan keluarga serta teman sebaya. Ini merupakan gejala umum dari depresi, ADHD, hingga kelainan bipolar.\r\n\r\n3. Kesulitan berkonsentrasi\r\n\r\nAnak-anak yang menderita gangguan mental cenderung sulit fokus atau memperhatikan dalam waktu yang lama. Selain itu, mereka juga memiliki kesulitan untuk duduk diam dan membaca. Tanda penyakit mental yang satu ini dapat menyebabkan menurunnya performa di sekolah juga perkembangan otaknya.\r\n\r\n4. Penurunan berat badan\r\n\r\nTahukah Anda bahwa gangguan mental juga dapat memengaruhi kondisi fisik anak? Tak hanya karena penyakit fisik, berat badan yang menurun drastis juga bisa menjadi tanda penyakit mental anak. Gangguan makan, stres, hingga depresi dapat menjadi penyebab anak kehilangan nafsu makan, mual, dan muntah yang berkelanjutan.\r\n\r\n5. Menyakiti diri sendiri\r\n\r\nPerhatikan saat anak sering mengalami kekhawatiran serta rasa takut berlebih. Perasaan ini dapat berujung pada keinginannya untuk menyakiti diri sendiri.\r\n\r\nBiasanya, ini menjadi akumulasi dari perasaan stres serta menyalahkan diri sendiri karena gangguan mental juga mengakibatkan anak sulit mengelola emosi. Ini juga menjadi tanda gangguan mental pada anak yang perlu Anda cermati karena tidak menutup kemungkinan berujung pada percobaan bunuh diri.\r\n\r\n6. Muncul berbagai masalah kesehatan\r\n\r\nPenyakit atau gangguan mental juga dapat ditandai dengan masalah pada kesehatannya, misal anak mengalami sakit kepala dan sakit perut yang berkelanjutan.\r\n\r\n7. Perasaan yang intens\r\n\r\nAnak-anak kadang menghadapi perasaan takut yang berlebihan tanpa alasan. Tanda gangguan mental pada anak ini seperti menangis, berteriak atau mual disertai dengan perasaan sangat intens. Perasaan ini pun dapat menyebabkan efek seperti kesulitan bernapas, jantung berdebar atau bernapas dengan cepat, yang dapat mengganggu aktivitas sehari-hari.', 'Kesehatan Mental', 'https://yankes.kemkes.go.id/img/bg-img/gambarartikel_1658394236_551030.png'),
(4, 'Apa Saja Penyebab Gangguan Kesehatan Mental?', 'Ada beberapa kondisi yang bisa menjadi penyebab seseorang mengalami gangguan kesehatan jiwa, antara lain: \r\n\r\n    Cedera pada kepala.\r\n    Faktor genetik atau terdapat riwayat pengidap gangguan kesehatan jiwa dalam keluarga.\r\n    Kekerasan dalam rumah tangga atau bentuk pelecehan lainnya.\r\n    Adanya riwayat kekerasan saat kanak-kanak.\r\n    Memiliki kelainan senyawa kimia otak atau gangguan pada otak.\r\n    Mengalami diskriminasi dan stigma.\r\n    Kehilangan atau kematian seseorang yang sangat dekat.\r\n    Mengalami kerugian sosial, seperti masalah kemiskinan atau utang.\r\n    Merawat anggota keluarga atau teman yang sakit kronis.\r\n    Pengangguran, kehilangan pekerjaan, atau tunawisma.\r\n    Pengaruh zat racun, alkohol, atau obat-obatan yang dapat merusak otak.\r\n    Stres berat yang terjadi dalam waktu yang lama.\r\n    Terisolasi secara sosial atau merasa kesepian.\r\n    Tinggal pada lingkungan perumahan yang buruk.\r\n    Mengalami trauma yang signifikan, seperti pertempuran militer, kecelakaan serius, atau tindakan kriminal lainnya.', 'Kesehatan Mental', 'https://fikes.almaata.ac.id/wp-content/uploads/2020/02/unnamed.jpg'),
(8, 'Pengertian Kesehatan Mental', 'Kesehatan jiwa atau sebutan lainnya kesehatan mental adalah kesehatan yang berkaitan dengan kondisi emosi, kejiwaan, dan psikis seseorang.\r\n\r\nPerlu kamu ketahui bahwa peristiwa dalam hidup yang berdampak besar pada kepribadian dan perilaku seseorang bisa berpengaruh pada kesehatan mentalnya.\r\n\r\nMisalnya, pelecehan saat usia dini, stres berat dalam jangka waktu lama tanpa adanya penanganan, dan mengalami kekerasan dalam rumah tangga.\r\n\r\nBerbagai kondisi tersebut bisa membuat kondisi kejiwaan seseorang terganggu, sehingga muncul gejala gangguan kesehatan jiwa. \r\n\r\nAkan tetapi, masalah kesehatan mental bisa mengubah cara seseorang dalam mengatasi stres, berhubungan dengan orang lain, membuat pilihan, dan memicu hasrat untuk menyakiti diri sendiri.\r\n\r\nBeberapa jenis gangguan mental yang umum terjadi antara lain depresi, gangguan bipolar, kecemasan, gangguan stres pasca trauma (PTSD), gangguan obsesif kompulsif (OCD), dan psikosis.\r\n\r\nSelain itu, ada beberapa penyakit mental hanya terjadi pada jenis pengidap tertentu, seperti postpartum depression hanya menyerang ibu setelah melahirkan.', 'Kesehatan Mental', 'https://d1vbn70lmn1nqe.cloudfront.net/prod/wp-content/uploads/2021/06/09064223/Kesehatan-Mental-1.jp');

-- --------------------------------------------------------

--
-- Table structure for table `long_texts`
--

CREATE TABLE `long_texts` (
  `id` int(11) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `long_texts`
--

INSERT INTO `long_texts` (`id`, `text`) VALUES
(4, 'hey kamu '),
(8, 'Assalamu\'alaikum '),
(9, 'haiii'),
(10, 'hay'),
(11, 'kgxkhxkhcmb mhxlhzlhzlgzkgzkgzkgxkhhhckgzkg,mv????gxkhckhc'),
(12, 'Tahu ga sih kalau aku sebenarnya pengen eee tapi malu bangey');

-- --------------------------------------------------------

--
-- Table structure for table `mp3_files`
--

CREATE TABLE `mp3_files` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `data` longblob DEFAULT NULL,
  `title` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mp3_files`
--

INSERT INTO `mp3_files` (`id`, `name`, `data`, `title`) VALUES
(1, 'y2mate.com - Musik Relaksasi Lagu Pengantar Tidur 30 Menit.mp3', NULL, 'Musik Pertama'),
(2, 'Indonesia merupakan .mp3', NULL, 'Bakso Ikan');

-- --------------------------------------------------------

--
-- Table structure for table `transcriptions`
--

CREATE TABLE `transcriptions` (
  `id` int(11) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transcriptions`
--

INSERT INTO `transcriptions` (`id`, `text`) VALUES
(1, 'Tuliskan 6 contoh'),
(2, 'tadi didengar sistem informasi upload di iPhone');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `updatedAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama`, `email`, `password`, `is_verified`, `createdAt`, `updatedAt`) VALUES
(11, 'isa', 'baninazarr12@gmail.com', 'pbkdf2:sha256:600000$LCB49npcxc51Xwmi$402a562a2b9de5e5a40eeac770fe087a92667b5606a598841fdfce041df8b477', 1, '2023-05-03 14:49:38', '2023-05-03 14:49:38'),
(12, 'IrfanTS', 'irfants1710@gmail.com', 'pbkdf2:sha256:600000$klvdXHWtnqO7E20q$7e27909279ffc8388d60c029318b3c7b38dde97e1398e9b6856770188841217b', 1, '2023-08-06 14:30:41', '2023-08-06 14:30:41');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `long_texts`
--
ALTER TABLE `long_texts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mp3_files`
--
ALTER TABLE `mp3_files`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transcriptions`
--
ALTER TABLE `transcriptions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `long_texts`
--
ALTER TABLE `long_texts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `mp3_files`
--
ALTER TABLE `mp3_files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `transcriptions`
--
ALTER TABLE `transcriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
