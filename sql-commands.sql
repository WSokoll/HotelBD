DROP TABLE IF EXISTS guests CASCADE;
CREATE TABLE guests (id serial primary key,
                    first_name varchar(255) NOT NULL,
                    last_name varchar(255) NOT NULL,
                    age int4 NOT NULL,
                    tel_number varchar(13) UNIQUE NOT NULL,
                    email varchar(100) UNIQUE NOT NULL,
                    CHECK (first_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$' AND last_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'),
                    CHECK (age BETWEEN 1 AND 120),
                    CHECK (tel_number ~ '^[0-9]{11}$'),
                    CHECK (email ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'));

DROP TABLE IF EXISTS rooms CASCADE;
CREATE TABLE rooms (id serial primary key,
                    number int4 UNIQUE NOT NULL,
                    description text,
                    capacity int4 NOT NULL,
                    price_per_day int4 NOT NULL,
                    CHECK (capacity BETWEEN 1 AND 10));

DROP TABLE IF EXISTS room_reservations CASCADE;
CREATE TABLE room_reservations (
                    id serial primary key,
                    start_date timestamp NOT NULL,
                    end_date timestamp NOT NULL,
                    num_of_people int4 NOT NULL,
                    guest_id int4 NOT NULL,
                    room_id int4 NOT NULL,
                    CHECK (num_of_people BETWEEN 1 AND 10),
                    FOREIGN KEY (guest_id) REFERENCES guests (id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (room_id) REFERENCES rooms (id) ON UPDATE CASCADE ON DELETE RESTRICT);

DROP TABLE IF EXISTS eq_categories CASCADE;
CREATE TABLE eq_categories (id serial primary key,
                            name varchar(100) UNIQUE NOT NULL,
                            description text);

DROP TABLE IF EXISTS equipment CASCADE;
CREATE TABLE equipment (id serial primary key,
                        cat_id int4 NOT NULL,
                        name varchar(100) NOT NULL,
                        description text,
                        cost_per_hour int4 NOT NULL,
                        FOREIGN KEY (cat_id) REFERENCES eq_categories(id) ON UPDATE CASCADE ON DELETE RESTRICT);

DROP TABLE IF EXISTS eq_reservations CASCADE;
CREATE TABLE eq_reservations (id serial primary key,
                              equipment_id int4 NOT NULL,
                              guest_id int4 NOT NULL,
                              start_date timestamp NOT NULL,
                              end_date timestamp NOT NULL,
                              FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                              FOREIGN KEY (guest_id) REFERENCES guests(id) ON UPDATE CASCADE ON DELETE RESTRICT);

DROP TABLE IF EXISTS positions CASCADE;
CREATE TABLE positions (id serial primary key,
                        name varchar(100) UNIQUE NOT NULL,
                        description text,
                        salary int4 NOT NULL);

DROP TABLE IF EXISTS employees CASCADE;
CREATE TABLE employees (id serial primary key,
                        first_name varchar(255) NOT NULL,
                        last_name varchar(255) NOT NULL,
                        tel_number varchar(13) UNIQUE NOT NULL,
                        email varchar(100) UNIQUE NOT NULL,
                        position_id int NOT NULL,
                        CHECK (first_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$' AND last_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'),
                        CHECK (tel_number ~ '^[0-9]{11}$'),
                        CHECK (email ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
                        FOREIGN KEY (position_id) REFERENCES positions(id) ON UPDATE CASCADE ON DELETE RESTRICT);

DROP TABLE IF EXISTS tasks CASCADE;
CREATE TABLE tasks (id serial primary key,
                    employee_id int4 NOT NULL,
                    room_id int4 NOT NULL,
                    name varchar(100) NOT NULL,
                    description text,
                    FOREIGN KEY (employee_id) REFERENCES employees(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (room_id) REFERENCES rooms(id) ON UPDATE CASCADE ON DELETE RESTRICT);

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (login varchar(255) UNIQUE NOT NULL,
                    password varchar(255) NOT NULL,
                    guest_id int4,
                    employee_id int4,
                    id serial PRIMARY KEY,
                    is_active BOOLEAN NOT NULL,
                    FOREIGN KEY (guest_id) REFERENCES guests(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (employee_id) REFERENCES employees(id) ON UPDATE CASCADE ON DELETE RESTRICT);



CREATE OR REPLACE FUNCTION check_date() RETURNS trigger as '
declare
    curr_ts timestamp without time zone;
begin
    IF NEW.end_date <= NEW.start_date THEN
        raise notice '' Data zakonczenia rezerwacji jest wczesniejsza lub taka sama jak poczatek rezerwacji! '';
        return NULL;
    END IF; 
    curr_ts = ( SELECT LOCALTIMESTAMP(0) );
    IF NEW.start_date < curr_ts THEN
        raise notice '' Data poczatku rezerwacji jest z przeszlosci. '';
        return NULL;
    END IF;
    return NEW;
end;
' language 'plpgsql';

CREATE TRIGGER check_date_t BEFORE INSERT ON room_reservations FOR EACH ROW EXECUTE PROCEDURE check_date();


CREATE OR REPLACE FUNCTION check_room() RETURNS trigger as '
declare
    temprow RECORD;
    tmp_s_date date;
    tmp_e_date date;
begin
    IF NEW.room_id IN (select room_id from room_reservations) THEN
        FOR temprow IN SELECT * FROM room_reservations where room_id = NEW.room_id LOOP
            tmp_s_date = temprow.start_date;
            tmp_e_date = temprow.end_date;
            IF NEW.end_date > tmp_s_date AND NEW.start_date < tmp_e_date THEN
                raise notice '' Pokoj jest juz zarezerwowany w wybranym terminie '';
                return NULL;
            END IF;
        END LOOP;
    END IF;
    IF NEW.num_of_people > (select capacity from rooms where id = NEW.room_id) THEN
        raise notice '' Za duza ilosc osob na ten pokoj '';
        return NULL;
    END IF;
    return NEW;
end;
' language 'plpgsql';

CREATE TRIGGER check_room_t BEFORE INSERT ON room_reservations FOR EACH ROW EXECUTE PROCEDURE check_room();

CREATE OR REPLACE FUNCTION check_item() RETURNS trigger as '
declare
    temprow RECORD;
    tmp_s_date date;
    tmp_e_date date;
begin
    IF NEW.equipment_id IN (select equipment_id from eq_reservations) THEN
        FOR temprow IN SELECT * FROM eq_reservations where equipment_id = NEW.equipment_id LOOP
            tmp_s_date = temprow.start_date;
            tmp_e_date = temprow.end_date;
            IF NEW.end_date > tmp_s_date AND NEW.start_date < tmp_e_date THEN
                raise notice '' Ekwipunek jest juz zarezerwowany w wybranym terminie '';
                return NULL;
            END IF;
        END LOOP;
    END IF;
    return NEW;
end;
' language 'plpgsql';

CREATE TRIGGER check_item_t BEFORE INSERT ON eq_reservations FOR EACH ROW EXECUTE PROCEDURE check_item();

CREATE VIEW show_room_reservations AS 
select rr.id, rr.start_date as "Poczatek rezerwacji", 
rr.end_date as "Koniec rezerwacji", 
r.number as "Numer pokoju", 
g.first_name as "Imie", 
g.last_name as "Nazwisko", 
g.tel_number as "Numer telefonu", 
g.email from room_reservations rr, 
guests g, 
rooms r 
where rr.guest_id=g.id and r.id = rr.room_id;

CREATE VIEW show_eq_reservations AS 
select er.id, er.start_date as "Poczatek rezerwacji", 
er.end_date as "Koniec rezerwacji", 
e.name as "Nazwa sprzętu", 
g.first_name as "Imie", 
g.last_name as "Nazwisko", 
g.tel_number as "Numer telefonu", 
g.email from eq_reservations er, 
guests g, 
equipment e 
where er.guest_id=g.id and e.id = er.equipment_id;
