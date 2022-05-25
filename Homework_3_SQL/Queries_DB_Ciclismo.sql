DECLARE cod_ciclista as CHAR(5);
SET cod_ciclista = 'C0001';
DECLARE cod_tappa as CHAR(5);
SET cod_tappa = 'T0001';

SELECT Nome, Cognome, NomeS, CodTappa, Edizione, Posizione
FROM CICLISTA C, CLASSIFICA_INDIVIDUALE CI, SQUADRA S
WHERE C.CodC = CI.CodC AND C.CodS = S.CodS
AND C.CodC = cod_ciclista AND CI.CodTappa = cod_tappa
ORDER BY Edizione;
