--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: category; Type: TABLE; Schema: public; Owner: rafael.castro
--

CREATE TABLE category (
    category_id integer NOT NULL,
    title character varying(255) NOT NULL
);


ALTER TABLE category OWNER TO "rafael.castro";

--
-- Name: category_category_id_seq; Type: SEQUENCE; Schema: public; Owner: rafael.castro
--

CREATE SEQUENCE category_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE category_category_id_seq OWNER TO "rafael.castro";

--
-- Name: category_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rafael.castro
--

ALTER SEQUENCE category_category_id_seq OWNED BY category.category_id;


--
-- Name: category_page; Type: TABLE; Schema: public; Owner: rafael.castro
--

CREATE TABLE category_page (
    category_id integer,
    page_id integer
);


ALTER TABLE category_page OWNER TO "rafael.castro";

--
-- Name: links; Type: TABLE; Schema: public; Owner: rafael.castro
--

CREATE TABLE links (
    page_id integer,
    linked_page_id integer,
    sort_position integer NOT NULL
);


ALTER TABLE links OWNER TO "rafael.castro";

--
-- Name: page; Type: TABLE; Schema: public; Owner: rafael.castro
--

CREATE TABLE page (
    page_id integer NOT NULL,
    title character varying(255) NOT NULL,
    modified timestamp without time zone NOT NULL
);


ALTER TABLE page OWNER TO "rafael.castro";

--
-- Name: page_page_id_seq; Type: SEQUENCE; Schema: public; Owner: rafael.castro
--

CREATE SEQUENCE page_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE page_page_id_seq OWNER TO "rafael.castro";

--
-- Name: page_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rafael.castro
--

ALTER SEQUENCE page_page_id_seq OWNED BY page.page_id;


--
-- Name: category category_id; Type: DEFAULT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY category ALTER COLUMN category_id SET DEFAULT nextval('category_category_id_seq'::regclass);


--
-- Name: page page_id; Type: DEFAULT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY page ALTER COLUMN page_id SET DEFAULT nextval('page_page_id_seq'::regclass);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (category_id);


--
-- Name: page page_pkey; Type: CONSTRAINT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY page
    ADD CONSTRAINT page_pkey PRIMARY KEY (page_id);


--
-- Name: category_page category_page_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY category_page
    ADD CONSTRAINT category_page_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(category_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: category_page category_page_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY category_page
    ADD CONSTRAINT category_page_page_id_fkey FOREIGN KEY (page_id) REFERENCES page(page_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: links links_linked_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY links
    ADD CONSTRAINT links_linked_page_id_fkey FOREIGN KEY (linked_page_id) REFERENCES page(page_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: links links_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: rafael.castro
--

ALTER TABLE ONLY links
    ADD CONSTRAINT links_page_id_fkey FOREIGN KEY (page_id) REFERENCES page(page_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

