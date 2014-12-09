CREATE TABLE nfl_tweets(idx_id,created,keywords);
CREATE INDEX idx_keywords_idx_id ON nfl_tweets(idx_id);
CREATE INDEX idx_keywords_created ON nfl_tweets(created);
