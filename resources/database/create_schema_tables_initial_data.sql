
CREATE SCHEMA crypto;


ALTER SCHEMA crypto OWNER TO postgres;


CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


CREATE TABLE crypto.asset (
    name text NOT NULL,
    asset_id text NOT NULL,
    symbol text NOT NULL
);


ALTER TABLE crypto.asset OWNER TO postgres;



CREATE TABLE crypto.asset_price (
    asset_price_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    price_usd double precision NOT NULL,
    "time" bigint NOT NULL,
    asset_id text NOT NULL
);


ALTER TABLE crypto.asset_price OWNER TO postgres;



ALTER TABLE ONLY crypto.asset
    ADD CONSTRAINT asset_pk PRIMARY KEY (asset_id);



ALTER TABLE ONLY crypto.asset_price
    ADD CONSTRAINT asset_price_pkey PRIMARY KEY (asset_price_id);



CREATE INDEX index_asset_id_time ON crypto.asset_price USING btree (asset_id, "time");



ALTER TABLE ONLY crypto.asset_price
    ADD CONSTRAINT asset_price_asset_asset_id_fk FOREIGN KEY (asset_id) REFERENCES crypto.asset(asset_id);



