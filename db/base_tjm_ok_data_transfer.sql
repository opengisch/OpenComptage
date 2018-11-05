
-- Transfer data from the table base_tjm_ok copy-pasted in QGIS to the real tables  

SET search_path = base_tjm_ok, comptages;

insert into section(id, name, owner, road, way, start_pr, end_pr, start_dist, end_dist, place_name, geometry) 
	select fsection, nom_rue,
	f_prop, f_axe, f_sens,
	to_number(f_pr_d, '999999999999999999.999'),
  	to_number(f_pr_f, '999999999999999999.999'), 
	to_number(f_dist_d, '999999999999999999.999'), 
	to_number(f_dist_f, '999999999999999999.999'), 
	lieu_rue,
	geometry from base_tjm_ok;
