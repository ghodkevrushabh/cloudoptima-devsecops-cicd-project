--
-- PostgreSQL database dump
--

\restrict t8x25ldQ5RnMKCQQDmgwEyN4xNNsv1YSjH6CpTbRNAbpGUfEsOR8nGnbXchTf6e

-- Dumped from database version 15.18
-- Dumped by pg_dump version 15.18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: environment_request; Type: TABLE; Schema: public; Owner: cloudoptima_admin
--

CREATE TABLE public.environment_request (
    id integer NOT NULL,
    app_name character varying(50) NOT NULL,
    environment character varying(20) NOT NULL,
    port integer NOT NULL,
    instance_size character varying(20) NOT NULL,
    status character varying(20)
);


ALTER TABLE public.environment_request OWNER TO cloudoptima_admin;

--
-- Name: environment_request_id_seq; Type: SEQUENCE; Schema: public; Owner: cloudoptima_admin
--

CREATE SEQUENCE public.environment_request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.environment_request_id_seq OWNER TO cloudoptima_admin;

--
-- Name: environment_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cloudoptima_admin
--

ALTER SEQUENCE public.environment_request_id_seq OWNED BY public.environment_request.id;


--
-- Name: environment_request id; Type: DEFAULT; Schema: public; Owner: cloudoptima_admin
--

ALTER TABLE ONLY public.environment_request ALTER COLUMN id SET DEFAULT nextval('public.environment_request_id_seq'::regclass);


--
-- Data for Name: environment_request; Type: TABLE DATA; Schema: public; Owner: cloudoptima_admin
--

COPY public.environment_request (id, app_name, environment, port, instance_size, status) FROM stdin;
1	demo-payment-api	dev	8080	t3.micro	Generated
2	demo-payment-api	dev	8080	t3.micro	Generated
3	demo-payment-api	dev	8080	t3.micro	Generated
4	demo-payment-api	dev	8080	t3.micro	Generated
5	demo-payment-api-2	dev	8080	t3.micro	Generated
6	demo-payment-api-2	dev	80	t3.micro	GitPushFailed
\.


--
-- Name: environment_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cloudoptima_admin
--

SELECT pg_catalog.setval('public.environment_request_id_seq', 6, true);


--
-- Name: environment_request environment_request_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudoptima_admin
--

ALTER TABLE ONLY public.environment_request
    ADD CONSTRAINT environment_request_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict t8x25ldQ5RnMKCQQDmgwEyN4xNNsv1YSjH6CpTbRNAbpGUfEsOR8nGnbXchTf6e

