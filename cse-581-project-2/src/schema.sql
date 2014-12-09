CREATE TABLE source_db
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL
)
GO
CREATE UNIQUE INDEX idx_source_db ON source_db(name)
GO
CREATE TABLE keywords
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_db_id INT NOT NULL,
    created VARCHAR(20) NOT NULL,
    content VARCHAR(200) NOT NULL
)
GO
CREATE INDEX idx_keywords_source_db ON keywords(source_db_id)
GO
CREATE INDEX idx_keywords_created ON keywords(created)
GO