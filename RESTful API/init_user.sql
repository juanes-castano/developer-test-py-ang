-- init_user.sql
-- Crea el usuario 'miusuario' con la contraseña 'miclave' si no existe
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'miusuario'
   ) THEN
      CREATE ROLE miusuario WITH LOGIN PASSWORD 'miclave' CREATEDB;
   ELSE
      RAISE NOTICE 'El usuario ya existe.';
   END IF;
END
$$;
