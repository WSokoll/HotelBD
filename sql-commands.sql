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

CREATE TABLE rooms (id serial primary key,
                    number int4 UNIQUE NOT NULL,
                    description text,
                    capacity int4 NOT NULL,
                    price_per_day int4 NOT NULL,
                    CHECK (capacity BETWEEN 1 AND 10));

CREATE TABLE room_reservations (
                    id serial primary key,
                    start_date timestamp NOT NULL,
                    end_date timestamp NOT NULL,
                    num_of_people int4 NOT NULL,
                    guest_id int4 NOT NULL,
                    room_id int4 NOT NULL,
                    CHECK (num_of_people BETWEEN 1 AND 10),
                    FOREIGN KEY (guest_id) REFERENCES guests (id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (room_id) REFERENCES rooms (id) ON UPDATE CASCADE ON DELETE RESTRICT
);


CREATE TABLE eq_categories (id serial primary key,
                            name varchar(100) UNIQUE NOT NULL,
                            description text);

CREATE TABLE equipment (id serial primary key,
                        cat_id int4 NOT NULL,
                        name varchar(100) NOT NULL,
                        description text,
                        cost_per_hour int4 NOT NULL,
                        FOREIGN KEY (cat_id) REFERENCES eq_categories(id) ON UPDATE CASCADE ON DELETE RESTRICT);

CREATE TABLE eq_reservations (id serial primary key,
                              equipment_id int4 NOT NULL,
                              guest_id int4 NOT NULL,
                              start_date timestamp NOT NULL,
                              end_date timestamp NOT NULL,
                              FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                              FOREIGN KEY (guest_id) REFERENCES guests(id) ON UPDATE CASCADE ON DELETE RESTRICT);

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

CREATE TABLE positions (id serial primary key,
                        name varchar(100) UNIQUE NOT NULL,
                        description text,
                        salary int4 NOT NULL);

CREATE TABLE tasks (id serial primary key,
                    employee_id int4 NOT NULL,
                    room_id int4 NOT NULL,
                    name varchar(100) NOT NULL,
                    description text,
                    FOREIGN KEY (employee_id) REFERENCES employees(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (room_id) REFERENCES rooms(id) ON UPDATE CASCADE ON DELETE RESTRICT);

CREATE TABLE users (login varchar(255) UNIQUE NOT NULL,
                    password varchar(255) NOT NULL,
                    guest_id int4,
                    employee_id int4,
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
    tmp_s_date date;
    tmp_e_date date;
begin
    IF NEW.room_id IN (select room_id from room_reservations) THEN
        tmp_s_date = (select start_date from room_reservations where room_id=NEW.room_id);
        tmp_e_date = (select end_date from room_reservations where room_id=NEW.room_id);
        IF NEW.end_date > tmp_s_date AND NEW.start_date < tmp_e_date THEN
            raise notice '' Pokoj jest juz zarezerwowany w wybranym terminie '';
            return NULL;
        END IF;
    END IF;
    IF NEW.num_of_people > (select capacity from rooms where id = NEW.room_id) THEN
        raise notice '' Za duza ilosc osob na ten pokoj '';
        return NULL;
    END IF;
    return NEW;
end;
' language 'plpgsql';

CREATE TRIGGER check_room_t BEFORE INSERT ON room_reservations FOR EACH ROW EXECUTE PROCEDURE check_room();