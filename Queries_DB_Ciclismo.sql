DECLARE cod_ciclista as SMALLINT;
SET cod_ciclista = 1;
DECLARE cod_tappa as SMALLINT;
SET cod_tappa = 1;

SELECT Nome, Cognome, NomeS, CodT, Edizione, Posizione
FROM CICLISTA C, CLASSIFICA_INDIVIDUALE CI, SQUADRA S
WHERE C.CodC = CI.CodC AND C.CodS = S.CodS
AND C.CodC = cod_ciclista AND CI.CodT = cod_tappa
ORDER BY Edizione;
