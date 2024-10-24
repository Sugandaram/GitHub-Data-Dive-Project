create database githubrepositorys;

use githubrepositorys;

CREATE TABLE repository_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Repository_Name VARCHAR(255) NOT NULL,
    Owner VARCHAR(255) NOT NULL,
    Description TEXT,
    URL VARCHAR(255),
    Programming_Language VARCHAR(100),
    Creation_Date DATETIME,
    Last_Updated_Date DATETIME,
    Number_of_Stars INT,
    Number_of_Forks INT,
    Number_of_Open_Issues INT,
    License_Type VARCHAR(100)
);

describe repository_data;

select * from repository_data;


