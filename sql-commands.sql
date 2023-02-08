CREATE OR ALTER TABLE guests (id serial primary key, 
                    first_name varchar(255) NOT NULL CONSTRAINT proper_letters CHECK (first_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'),
                    last_name varchar(255) NOT NULL CONSTRAINT proper_letters CHECK (first_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'),
                    age int4 NOT NULL CONSTRAINT proper_age CHECK (age ~ '[1-125]'),
                    tel_number varchar(13) UNIQUE NOT NULL CONSTRAINT proper_tel CHECK (tel_number ~ '^[0-9]{11}$'),
                    email varchar(100) UNIQUE NOT NULL CONSTRAINT proper_email CHECK (email ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'));

CREATE OR ALTER TABLE rooms (id serial primary key,
                    number int4 UNIQUE NOT NULL,
                    description text,
                    capacity int4 NOT NULL CONSTRAINT proper_number CHECK (capacity ~ '[1-10]'),
                    price_per_day int4 NOT NULL);

CREATE OR ALTER TABLE room_reservations (id serial primary key,
                                guest_id int4 references guests(id) NOT NULL,
                                room_id int4 references rooms(id) NOT NULL,
                                start_date timestamp NOT NULL,
                                end_date timestamp NOT NULL,
                                num_of_people int4 NOT NULL CONSTRAINT proper_number CHECK (num_of_people ~ '[1-10]'));

CREATE OR ALTER TABLE eq_categories (id serial primary key,
                            name varchar(100) UNIQUE NOT NULL,
                            description text);

CREATE OR ALTER TABLE equipment (id serial primary key,
                        cat_id int4 references eq_categories(id) NOT NULL,
                        name varchar(100) NOT NULL,
                        description text,
                        cost_per_hour int4 NOT NULL);

CREATE OR ALTER TABLE eq_reservations (id serial primary key,
                              equipment_id int4 references equipment(id) NOT NULL,
                              guest_id int4 references guests(id) NOT NULL,
                              start_date timestamp NOT NULL,
                              end_date timestamp NOT NULL);

CREATE OR ALTER TABLE employees (id serial primary key,
                        first_name varchar(255) NOT NULL CONSTRAINT proper_letters CHECK (first_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'),
                        last_name varchar(255) NOT NULL CONSTRAINT proper_letters CHECK (first_name ~ '^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'),
                        tel_number varchar(13) UNIQUE NOT NULL CONSTRAINT proper_tel CHECK (tel_number ~ '^[0-9]{11}$'),
                        email varchar(100) UNIQUE NOT NULL CONSTRAINT proper_email CHECK (email ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
                        position_id int references positions(id) NOT NULL);

CREATE OR ALTER TABLE positions (id serial primary key,
                        name varchar(100) UNIQUE NOT NULL,
                        description text,
                        salary int4 NOT NULL);

CREATE OR ALTER TABLE tasks (id serial primary key,
                    employee_id int4 references employees(id) NOT NULL,
                    room_id int4 references rooms(id) NOT NULL,
                    name varchar(100) NOT NULL,
                    description text);

CREATE OR ALTER TABLE users (login varchar(255) UNIQUE NOT NULL,
                    password varchar(255) NOT NULL,
                    guest_id int4 references guests(id),
                    employee_id int4 references employees(id));



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