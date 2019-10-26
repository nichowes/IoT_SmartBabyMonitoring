-- IoT Smart Baby Monitoring SQL Create Schema Code

CREATE TABLE BABY_ANALYSIS (
    id int NOT NULL,
    babyName varchar(255) NOT NULL,
    babyAge int NOT NULL,
    babyHeight int NOT NULL,
    babyWeight int NOT NULL,
    averageNumberOfWakeupsPerDay int NOT NULL,
    averageWakeupTimesPerDay varchar(255) NOT NULL,
    averageNumberOfFeedsPerDay int NOT NULL,
    averageFeedTimesPerDay varchar(255) NOT NULL,
    favouriteDayTimeCalmDownMethod int NOT NULL,
    favouriteNightTimeCalmDownMethod int NOT NULL,
    preferredTemperature int NOT NULL,
    CONSTRAINT BABY_ANALYSIS_pk PRIMARY KEY (id)
) COMMENT 'All information relating to the baby analysis.';

CREATE TABLE BABY_CALM_METHODS (
    id int NOT NULL,
    name varchar(255) NOT NULL,
    type varchar(255) NOT NULL,
    description varchar(255) NOT NULL,
    priority int NOT NULL,
    CONSTRAINT BABY_CALM_METHODS_pk PRIMARY KEY (id)
) COMMENT 'All the methods the system uses to ';

CREATE TABLE GENERAL_DATA_AND_SETTINGS (
    id int NOT NULL,
    userName varchar(255) NOT NULL,
    babyName varchar(255) NOT NULL,
    waitTimeAfterTryingCalmMethods int NOT NULL,
    CONSTRAINT GENERAL_DATA_AND_SETTINGS_pk PRIMARY KEY (id)
) COMMENT 'All general information relating to the system and its users.';

CREATE TABLE SENSOR_DATA (
    id int NOT NULL,
    timestamp timestamp NOT NULL,
    temperature_sensor_Temperature int NOT NULL,
    temperature_sensor_Humidity int NOT NULL,
    CONSTRAINT SENSOR_DATA_pk PRIMARY KEY (id)
);

-- Foreign Keys
-- Reference: BABY_ANALYSIS_BABY_CALM_METHODS (table: BABY_ANALYSIS)
ALTER TABLE BABY_ANALYSIS ADD CONSTRAINT BABY_ANALYSIS_BABY_CALM_METHODS FOREIGN KEY BABY_ANALYSIS_BABY_CALM_METHODS (favouriteDayTimeCalmDownMethod)
    REFERENCES BABY_CALM_METHODS (id);

-- Reference: favouriteNightTimeCalmDownMethod (table: BABY_ANALYSIS)
ALTER TABLE BABY_ANALYSIS ADD CONSTRAINT favouriteNightTimeCalmDownMethod FOREIGN KEY favouriteNightTimeCalmDownMethod (favouriteNightTimeCalmDownMethod)
    REFERENCES BABY_CALM_METHODS (id);
