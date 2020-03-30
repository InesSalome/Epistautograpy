PRAGMA encoding = 'UTF-8';

INSERT INTO DESTINATAIRE(type_destinataire,titre_destinataire, identite_destinataire,date_naissance,date_deces) 
VALUES ("noblesse","Princesse de Viane","Madeleine de France","1443-12-01","1495-01-21"),
("noblesse","Reine de Navarre ","Catherine de Navarre","1468-04-18","1517-02-12"),
("noblesse","Duc de Milan","Jean Galéas Sforza","1469-06-20","1494-10-22"),
("institution",NULL,"États de Béarn",NULL,NULL),
("institution",NULL,"Chambre des Comptes de Paris",NULL,NULL),
("institution",NULL,"Anciennes Ligues de la Haute-Allemagne",NULL,NULL),
("institution",NULL,"Parlement de Paris",NULL,NULL);

INSERT INTO INSTITUTION_CONSERVATION(nom_institution_conservation,latitude_institution_conservation,longitude_institution_conservation)
VALUES ("Archives départementales des Pyrénées-Atlantiques",43.3,-0.3667),
("Archives d'État de Milan", 45.4654219,9.1859243),
("Archives nationales",48.866667,2.333333),
("Archives d'État du canton de Zurich",47.4535,8.561);

INSERT INTO LETTRE(date_envoie_lettre,lieu_ecriture_lettre,objet_lettre,contresignataire_lettre,langue_lettre,pronom_personnel_employe_lettre,cote_lettre,statut_lettre, institution_id)
VALUES ("1483-09-09","Amboise","Invitation à consentir au mariage de la reine Catherine de Navarre avec Jean, fils aîné d'Alain, sire d'Albret.","Mesme","Français","Je","E 543","Copie",1),
("1483-09-09","Amboise","Invitation à consentir au mariage de la reine Catherine de Navarre avec Jean, fils aîné d'Alain, sire d'Albret.","Mesme","Français","Je","E 543","Copie",1),
("1483-09-21","Amboise","Réponse à la dernière lettre écrite par le duc au roi Louis XI, promesse à s'employer à la pacification de l'Italie.","Charbonier","Latin","Nous","Potenze estere, corrispondenze diplomatiche","Orig.",2),
("1483-09-08","Amboise","Invitation à consentir au mariage de la reine Catherine de Navarre avec Jean, fils aîné d'Alain, sire d'Albret.","non mentionné","Français","Nous","E 543", "Orig.",1),
("1488-02-05","Poissy","Ordre de mettre incontinent à exécution les lettres portant donation au maréchal de Gié de la terre et seigneurie de Fronsac, en échange de la terre de Fontenay-le-Comte, qui est réunie au domaine royal.","Robineau","Français","Nous","reg. MM 759, p.790","Copie",3),
("1486-10-05","Compiègne","Sauf-conduit a été accordé aux Suisses de l'armée du duc d'Autriche qui se sont rendus aux Français, et un secours de deux francs a été attribué à chacun d'eux. Idée que si ces hommes avaient préféré le service de la France à celui de l'Autriche, ils n'eussent pas été réduits à une telle extrémité.","Damont","Latin","Nous","Lettres des rois de France","Orig.",4),
("1487-10-08","Laval","Surséance de trois mois en faveur de Navarrot d'Anglade, seigneur de Colombiers, présentement occupé à la guerre en Basse-Bretagne.","Robineau","Français","Nous","X1a, 9319, fol.13","Orig.",3);

INSERT INTO IMAGE_NUMERISEE(url_image_numerisee,reference_bibliographique_image_numerisee, lettre_id)
VALUES ("https://archive.org/details/lettresdecharle06chargoog/page/n19/mode/","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.6.",1),
("https://archive.org/details/lettresdecharle06chargoog/page/n21/mode/","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.8.",2),
("https://archive.org/details/lettresdecharle06chargoog/page/n25/mode/","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.12.",3),
("https://archive.org/details/lettresdecharle06chargoog/page/n17/mode/","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.4.",4),
("https://archive.org/details/lettresdecharle06chargoog/page/n293/mode/","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.283.",5),
("https://archive.org/details/lettresdecharle07chargoog/page/n151/mode/2up","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.137.",6),
("https://archive.org/details/lettresdecharle07chargoog/page/n245/mode/2up","Lettres de Charles VIII, roi de France, vol.1, Librairie Renouard, H. Laurens, 1898, p.231.",7);

INSERT INTO CORRESPONDANCE(destinataire_id, lettre_id)
VALUES (1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7);