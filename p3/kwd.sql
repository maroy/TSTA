CREATE TABLE keywords(idx_id,created,content);
CREATE INDEX idx_keywords_idx_id ON keywords(idx_id);
CREATE INDEX idx_keywords_created_id ON keywords(created);
