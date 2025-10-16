DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id varchar NOT NULL,
    email varchar NOT NULL,
    password varchar NOT NULL,
    created_at timestamp DEFAULT now(),
    is_active boolean NOT NULL DEFAULT true,
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX users_email_key ON public.users USING btree (email);

CREATE INDEX ix_users_id ON public.users USING btree (id);

CREATE TABLE posts (
    id varchar NOT NULL,
    owner_id varchar NOT NULL,
    title varchar NOT NULL,
    content varchar NOT NULL,
    published boolean DEFAULT true,
    rating integer,
    created_at timestamp DEFAULT now(),
    PRIMARY KEY (id),
    CONSTRAINT posts_owner_id_fkey FOREIGN key (owner_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX ix_posts_id ON public.posts USING btree (id);

CREATE TABLE votes (
    post_id varchar NOT NULL,
    user_id varchar NOT NULL,
    PRIMARY KEY (post_id, user_id),
    CONSTRAINT votes_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
    CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);