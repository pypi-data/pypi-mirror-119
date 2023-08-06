CREATE TABLE IF NOT EXISTS "Container"(
    "Name" TEXT PRIMARY KEY,
    "Hosted" TEXT NOT NULL UNIQUE,
    "Version" VARCHAR(20) NOT NULL,
    "Readme" TEXT DEFAULT ""
);

CREATE TABLE IF NOT EXISTS "Sql"(
    "Hash" INT PRIMARY KEY,
    "SQL" TEXT NOT NULL,
    "EMPTY" BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE TABLE IF NOT EXISTS "Settings"(
    "Name" TEXT PRIMARY KEY,
    "Auto" BOOL DEFAULT TRUE,
    "Checked" TEXT,
    "Updated" TEXT,
    FOREIGN KEY(Name) REFERENCES Container(Name) ON DELETE CASCADE
);


INSERT OR IGNORE INTO "Container"(
    "Name", "Hosted", "Version") VALUES (
    "Rash", "https://github.com/RahulARanger/Rash/tree/master/Rash", "0.0.4"
);

INSERT OR IGNORE INTO Settings(Name) VALUES ("Rash");

INSERT OR IGNORE INTO "Sql"(
'Hash', 'SQL') VALUES(
0, "SELECT SQL, Empty FROM Sql WHERE Hash = ?"
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
1, "SELECT Name FROM Container;", TRUE
); -- for selecting all entities except markdown in Container


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
2, "SELECT Hosted, Version FROM Container WHERE Name = ?;"
); -- searches in container through Name column


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
3, "SELECT Hosted FROM Container WHERE Name = ?;"
); -- used in search bar

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
4, "SELECT Version FROM Container WHERE Name = ?;"
); -- used for checking updates

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
5, "SELECT Name, Hosted, Version FROM Container;", TRUE
); -- while activating extension

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
6, "DELETE FROM Container WHERE Name = ?;", TRUE
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
7, "SELECT Readme FROM Container WHERE Name = ?;"
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES(
8, "UPDATE Container SET Version = ? WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES(
9, "UPDATE Container SET Readme = ? WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES(
10, "INSERT INTO Container(Name, Hosted, Version, Readme) VALUES(?, ?, ?, ?);"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES(
11, "SELECT Name FROM Container WHERE Hosted = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES(
12, "SELECT Auto FROM Settings WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "Sql") VALUES(
13, "UPDATE Settings SET Auto = ? WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "Sql") VALUES(
14, "UPDATE Settings SET Updated = datetime('now') WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "Sql") VALUES(
15, "SELECT Updated FROM Settings WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "Sql") VALUES(
16, "SELECT Checked FROM Settings WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "Sql") VALUES(
17, "UPDATE Settings SET Updated = datetime('now') WHERE Name = ?;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "Sql") VALUES(
18, "DELETE FROM Container WHERE Name = ?;"
);
