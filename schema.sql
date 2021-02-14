
-- delete the urls table if it alredy exists to avoid the possibility of another table named urls existing
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    -- id to get the original url from hash string 
    -- original_url is the original long url to redirect users 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
);
