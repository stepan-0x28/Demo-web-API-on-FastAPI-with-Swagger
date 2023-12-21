CREATE TABLE roles (
    id          serial4 NOT NULL,
    key         varchar NOT NULL,
    name        varchar NOT NULL,
    description varchar NOT NULL,
    CONSTRAINT roles_pk PRIMARY KEY (id),
    CONSTRAINT roles_un UNIQUE (key)
);

CREATE TABLE statuses (
    id          serial4 NOT NULL,
    key         varchar NOT NULL,
    name        varchar NOT NULL,
    description varchar NOT NULL,
    CONSTRAINT statuses_pk PRIMARY KEY (id),
    CONSTRAINT statuses_un UNIQUE (key)
);

CREATE TABLE users (
    id         serial4 NOT NULL,
    username   varchar NOT NULL,
    password   varchar NOT NULL,
    role_id    int4    NOT NULL,
    first_name varchar NOT NULL,
    last_name  varchar NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_un UNIQUE (username),
    CONSTRAINT users_fk FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE orders (
    id          serial4 NOT NULL,
    customer_id int4    NOT NULL,
    executor_id int4    NOT NULL,
    name        varchar NOT NULL,
    description varchar NOT NULL,
    status_id   int4    NOT NULL,
    is_deleted  bool    NOT NULL DEFAULT false,
    CONSTRAINT orders_pk PRIMARY KEY (id),
    CONSTRAINT orders_fk FOREIGN KEY (customer_id) REFERENCES users (id),
    CONSTRAINT orders_fk_1 FOREIGN KEY (executor_id) REFERENCES users (id),
    CONSTRAINT orders_fk_2 FOREIGN KEY (status_id) REFERENCES statuses (id)
);


INSERT INTO roles (key, name, description)
VALUES ('customer', 'Customer', 'Creates orders'),
       ('executor', 'Executor', 'Fulfills orders');

INSERT INTO statuses (key, name, description)
VALUES ('new', 'New', 'The customer created an order'),
       ('in_progress', 'In progress', 'The customer began work on the order'),
       ('completed', 'Completed', 'The customer has completed work on the order');

INSERT INTO users (username, password, role_id, first_name, last_name)
VALUES ('kevin645', 'kevin645pass', 2, 'Kevin', 'Morgan'),
       ('james4214', 'james4214pass', 2, 'James', 'Anderson'),
       ('fred4444', 'fred4444pass', 1, 'Fred', 'Russell'),
       ('thomas9213', 'thomas9213pass', 1, 'Thomas', 'Sparks'),
       ('josh8882', 'josh8882pass', 1, 'Josh', 'Torres');

INSERT INTO orders(customer_id, executor_id, name, description, status_id, is_deleted)
VALUES (3, 1, 'Website', 'Create a website using the Django framework for an insurance company', 1, false),
       (3, 2, 'Mobile app', 'Create a mobile application for Android for a pizzeria', 1, false),
       (4, 2, 'Service', 'Data processing service for a meteorological company', 2, false);