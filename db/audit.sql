
alter system set log_connections=on;
alter system set log_disconnections=on;
alter system set log_statement='mod';
alter system set logging_collector=on;
alter system set log_hostname=on;

select pg_reload_conf();
