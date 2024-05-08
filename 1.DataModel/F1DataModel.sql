CREATE TABLE "circuits" (
  "circuitId" integer,
  "circuitRef" varchar,
  "name" varchar,
  "location" varchar,
  "country" varchar,
  "lat" integer,
  "lng" integer,
  "alt" integer,
  "url" varchar
);

CREATE TABLE "constructor_results" (
  "constructorResultdsId" integer,
  "raceId" integer,
  "constructorId" integer,
  "points" integer,
  "status" varchar
);

CREATE TABLE "constructor_standings" (
  "constructorStandingsId" integer,
  "raceId" integer,
  "constructorId" integer,
  "points" integer,
  "position" integer,
  "positionText" integer,
  "wins" integer
);

CREATE TABLE "constructors" (
  "constructorId" integer,
  "constructorRef" varchar,
  "name" varchar,
  "nationality" varchar,
  "url" varchar
);

CREATE TABLE "driver_standings" (
  "driverStandingsId" integer,
  "raceId" integer,
  "driverId" integer,
  "points" integer,
  "position" integer,
  "positionText" varchar,
  "win" integer
);

CREATE TABLE "drivers" (
  "driverId" integer,
  "driverRef" varchar,
  "number" varchar,
  "code" varchar,
  "forename" varchar,
  "surname" varchar,
  "dob" date,
  "nationality" varchar,
  "url" varchar
);

CREATE TABLE "lap_times" (
  "raceId" integer,
  "driverId" integer,
  "lap" integer,
  "position" integer,
  "time" time,
  "milliseconds" integer
);

CREATE TABLE "pit_stops" (
  "raceId" integer,
  "driverId" integer,
  "stop" integer,
  "lap" integer,
  "time" time,
  "duration" integer,
  "milliseconds" integer
);

CREATE TABLE "qualifying" (
  "qualifyId" integer,
  "raceId" integer,
  "driveId" integer,
  "constructorId" integer,
  "number" integer,
  "position" integer,
  "q1" time,
  "q2" time,
  "q3" time
);

CREATE TABLE "races" (
  "raceId" integer,
  "year" integer,
  "round" integer,
  "circuitId" varchar,
  "name" varchar,
  "date" date,
  "time" time,
  "url" varchar,
  "fp1_date" time,
  "fp1_time" time,
  "fp2_date" time,
  "fp2_time" time,
  "fp3_date" time,
  "fp3_time" time,
  "quali_date" time,
  "quali_time" time,
  "sprint_date" time,
  "sprint_time" time
);

CREATE TABLE "results" (
  "resultId" integer,
  "raceId" integer,
  "driverId" integer,
  "constructorId" integer,
  "number" integer,
  "grid" integer,
  "position" integer,
  "positionText" varchar,
  "positionOrder" integer,
  "points" integer,
  "laps" integer,
  "time" time,
  "milliseconds" integer,
  "fastestLap" time,
  "rank" integer,
  "fastestLapTime" time,
  "fastestLapSpeed" integer,
  "statusId" integer
);

CREATE TABLE "seasons" (
  "year" integer,
  "url" varchar
);

CREATE TABLE "sprints_results" (
  "resultId" integer,
  "raceId" integer,
  "driverId" integer,
  "constructorId" integer,
  "number" integer,
  "grid" integer,
  "position" integer,
  "positionText" varchar,
  "positionOrder" integer,
  "points" integer,
  "laps" integer,
  "time" time,
  "milliseconds" integer,
  "fastestLap" time,
  "fastestLapTime" time,
  "statusId" integer
);

CREATE TABLE "status" (
  "statusId" integer,
  "status" varchar
);
