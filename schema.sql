-- user database
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    date_birth TEXT NOT NULL,
    password TEXT NOT NULL  
);


-- admin database
DROP TABLE IF EXISTS admin;

CREATE TABLE admin
(
    admin_id PRIMARY KEY,
    admin_password TEXT NOT NULL
);

INSERT INTO admin (admin_id, admin_password)
VALUES
    ('Shopkeeper', 'pbkdf2:sha256:260000$DXmvxgsB3CKucsyH$c65725235763b8fba5ff1482ee816d5dc011b6f7162134476f395f4b971657bb');




-- kit database
DROP TABLE IF EXISTS kit_all;

CREATE TABLE kit_all
(
    kit_id INTEGER PRIMARY key AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL,
    image_name TEXT NOT NULL
);

INSERT INTO kit_all (name, price, description, image_name)
VALUES
    ('Ucc Jersey', 55, '1-1 replica of the game day jersey', 'jersey.jpg'),
    ('Hoodie', 55, 'Casual, comfortable zip hoodie with zip pockets', 'hoodie.png'),
    ('Warm-up Jersey', 20, 'A light jersey for pre-game or training', 'tshirt.jpg'),
    ('Sleevles gym top', 12.99, 'No sleeves, great for gym sessions', 'vest.jpg'),
    ('Pants', 24.99, 'Casual, comfortable pants with zip pockets', 'pants.jpg'),
    ('Tactic Shorts', 15.50, 'A light, comfortable leisure shorts with zip pockets', 'shorts.jpg' );

-- customer checkout database
DROP TABLE IF EXISTS details;

CREATE TABLE details
(
    address TEXT PRIMARY key,
    card_name TEXT NOT NULL,
    number TEXT NOT NULL,
    expiry TEXT NOT NULL,
    cvc TEXT NOT NULL
);


-- CREATE TABLE dboImages

-- (

--       [ImageID] [int] IDENTITY(1,1) NOT NULL,

--       [ImageName] [varchar](40) NOT NULL,

--       [OriginalFormat] [nvarchar](5) NOT NULL, 

--       [ImageFile] [varbinary](max) NOT NULL

--  );  

-- INSERT INTO dboImages

-- (

--        ImageName

--       ,OriginalFormat

--       ,ImageFile

-- )

-- SELECT

--       'Sample Image'

--       ,'jpg'

--       ,ImageFile

-- FROM OPENROWSET(BULK N'C:\Users\peter\Desktop\HTML\WD2\ucc_rugby\static\tshirt_shop.jpg', SINGLE_BLOB) AS ImageSource(ImageFile);