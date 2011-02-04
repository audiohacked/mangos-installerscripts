GRANT USAGE ON * . * TO 'mangos'@'localhost' IDENTIFIED BY 'mangos' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 ;
CREATE DATABASE `mangos` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES ON `mangos` . * TO 'mangos'@'localhost' WITH GRANT OPTION;