
drop schema if exists base_tjm_ok cascade;
create schema base_tjm_ok;
alter schema base_tjm_ok owner to postgres;

create table base_tjm_ok.base_tjm_ok(
    fsection text NOT NULL,
    fonctionel text,
    f_prop text,
    f_axe text,
    f_sens text,
    f_pr_d text,
    f_dist_d text,
    ecartd text,
    f_pr_f text,
    f_dist_f text,
    ecartf text,
    usaneg text,
    poste text,
    troncon text,
    lieu_rue text,
    type_tra text,
    sensor text,
    classif text,
    lpseps text,
    permanent text,
    c_ehbdo text,
    boucon text,
    ccd text,
    ccf text,
    f_long text,
    f_surf text,
    nom_rue text,
    Dir1 text,
    Dir2 text,
    geometry geometry(LINESTRING, 2056)
);





