#Page pour créer des transactions sécurisées
from warnings import warn

LETTRES_PAR_PAGE = 2
SECRET_KEY = "JE SUIS UN SECRET !"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
