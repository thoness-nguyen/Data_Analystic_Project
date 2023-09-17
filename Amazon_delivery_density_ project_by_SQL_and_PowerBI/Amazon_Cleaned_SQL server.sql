use LEARN_DA
go
select * from amazon_analyze
go

--------------------------------------------------------------------------------------------------------------------------------------
-- View info of the data frame
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'amazon_analyze';

-- view the top six rows of dataframe
select top 6* from amazon_analyze


--------------------------------------------------------------------------------------------------------------------------------------
-- Identified missing value
SELECT
  COLUMN_NAME,
  COUNT(*) AS TotalRows,
  COUNT(*) - COUNT('Delivery_person_Age') AS MissingCount,
-- hàm cast để chuyển kiểu dữ liệu SELECT CAST(column_name AS DECIMAL(10, 2)) FROM table_name;
  CAST((COUNT(*) - COUNT('Delivery_person_Age')) * 100.0 / COUNT(*) AS DECIMAL(5, 2)) AS MissingPercentage
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'amazon_analyze'
GROUP BY COLUMN_NAME

-- Handle missing values
update amazon_analyze set "Delivery_person_Ratings" =
(
	select top 1 Delivery_person_Ratings from amazon_analyze
	where "Delivery_person_Ratings" <> N'NaN' or
	"Delivery_person_Ratings" <> N'0' or
	"Delivery_person_Ratings" is not null
	group by Delivery_person_Ratings
	order by count(*) DESC
)
where "Delivery_person_Ratings" = 'NaN' or
"Delivery_person_Ratings" = N'0' or
"Delivery_person_Ratings" is null
go
update amazon_analyze set Delivery_person_Age =
(
	select top 1 Delivery_person_Age from amazon_analyze
	group by Delivery_person_Age
	order by count (*) DESC
)
	where "Delivery_person_Age" = N'NaN' or Delivery_person_Age = N'0' or Delivery_person_Age is null
go
update amazon_analyze set Type_of_vehicle = 
	(
	select top 1 Type_of_vehicle from amazon_analyze 
	where Type_of_vehicle is not null
	group by Type_of_vehicle
	order by count (*) DESC
	)
where Type_of_vehicle = N'0' or Type_of_vehicle is null or Type_of_vehicle = N'NaN'


--------------------------------------------------------------------------------------------------------------------------------------
-- Handle error time value
select * from amazon_analyze
where Time_Orderd is null or Time_Orderd = N'NaN' or Time_Orderd = N'0'
go
select * from amazon_analyze
where Time_Order_picked is null or Time_Order_picked = N'NaN' or Time_Order_picked = N'0'

update amazon_analyze set Time_Orderd = Null
where Time_Orderd = null or Time_Orderd = N'0' or Time_Orderd = N'NaN'
go
update amazon_analyze set Time_Orderd_picked = Null
where Time_Orderd_picked = null or Time_Orderd_picked = N'0' or Time_Orderd_picked = N'NaN'


-- Change type of time value
update amazon_analyze set Time_Orderd =
(
	select convert (nvarchar (50), cast ("Time_Orderd" as Time),108)
)
go
UPDATE amazon_analyze SET Time_Order_picked = 
(
    SELECT CONVERT(NVARCHAR(50), CAST("Time_Order_picked" AS TIME), 108)
    WHERE ISDATE("Time_Order_picked") = 1
)
-- ADD column Count_minute_order by minus of 2 columns
update amazon_analyze set Count_mintue_order = 
(select datediff (MINUTE, Time_Orderd_picked, Time_Orderd))


--------------------------------------------------------------------------------------------------------------------------------------
-- delete unused columns
alter table amazon_analyze drop column "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude","Restaurant_latitude"
go
alter table amazon_analyze drop column "Name"
go
alter table amazon_analyze drop column "Filled_Time_Orderd", "fill_time_picked"


--------------------------------------------------------------------------------------------------------------------------------------
-- Analyze


--1. Count the number of records and the number of records with missing data in the "Delivery_person_Age" column:
SELECT COUNT(Delivery_person_Age) FROM amazon_analyze
WHERE Delivery_person_Age IS NULL;


--2. Get the total number of orders by order type:
SELECT Type_of_order, COUNT(*) AS Total_count FROM amazon_analyze
GROUP BY Type_of_order;


--3. Get the total number of deliveries affected by weather (with weather information) and not affected by weather (without weather information):
-- Total deliveries by weather condition
SELECT Weather, COUNT(*) FROM amazon_analyze
GROUP BY Weather;

-- Total deliveries affected by storms or sandstorms
SELECT COUNT(Weather) AS Order_Amount FROM amazon_analyze
WHERE Weather IN ('Stormy', 'Sandstorms');

-- Total deliveries not affected by weather (sunny, cloudy, windy, foggy)
SELECT COUNT(Weather) AS Order_Amount FROM amazon_analyze
WHERE Weather IN ('Sunny', 'Cloudy', 'Windy', 'Fog');


--4. Retrieve information about delivery personnel (Delivery_person_Ratings) with the highest and lowest ratings:
SELECT * FROM amazon_analyze
WHERE Delivery_person_Ratings = (
    SELECT MIN(Delivery_person_Ratings) AS Rating_info_min FROM amazon_analyze
) 
OR Delivery_person_Ratings = (
    SELECT MAX(Delivery_person_Ratings) AS Rating_info_max FROM amazon_analyze
)
ORDER BY Delivery_person_Ratings;

