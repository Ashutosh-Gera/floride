DELIMITER $$
CREATE TRIGGER driver_rating_insert
AFTER INSERT ON booking
FOR EACH ROW 
BEGIN 
    IF NEW.review_id IS NOT NULL THEN
        UPDATE driver
        SET driver.rating = (
            SELECT avg(star_review) FROM booking JOIN review ON booking.review_id = review.review_id WHERE booking.driver_id = driver.driver_id
        )
        WHERE driver.driver_id = NEW.driver_id;
    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER driver_rating_update
AFTER UPDATE ON booking
FOR EACH ROW 
BEGIN 
    IF NEW.review_id IS NOT NULL THEN
        UPDATE driver
        SET driver.rating = (
            SELECT avg(star_review) FROM booking JOIN review ON booking.review_id = review.review_id WHERE booking.driver_id = driver.driver_id
        )
        WHERE driver.driver_id = NEW.driver_id;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER driver_rating_delete
AFTER DELETE ON booking
FOR EACH ROW 
BEGIN 
    IF OLD.review_id IS NOT NULL THEN
        UPDATE driver
        SET driver.rating = (
            SELECT avg(star_review) FROM booking JOIN review ON booking.review_id = review.review_id WHERE booking.driver_id = driver.driver_id
        )
        WHERE driver.driver_id = OLD.driver_id;
    END IF;
END$$
DELIMITER ;

--trigger to delete an entry in car table when a driver is deleted

DELIMITER $$
CREATE TRIGGER car_delete
AFTER DELETE ON driver
FOR EACH ROW 
BEGIN 
    DELETE FROM car WHERE car.car_id = OLD.car_id;
END$$
DELIMITER ;

