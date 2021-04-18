# AI-KR-tema1
Se va implementa o problema asemanatoare cu a canibalilor si misionarilor, indeplinind urmatoare conditii:
In continuare avem N misionari si N canibali si o barca cu M locuri. In oricare dintre locatii (maluri/barca) trebuie respectata conditia: fie nu am misionari, fie am misionari dar atunci trebuie sa fie in numar mai mare sau egal decat canibalii.
Barca poate duce doar o anumită capacitate GMAX, dată în fișierul de intrare.
Fiecare canibal si misionar va avea o greutate proprie (mentionata in fisierul de intrare). Greutatea celor urcati in barca nu trebuie sa depaseasca greutatea maxima pe care o poate duce barca.
Costul unei mutări e dat de suma greutăților oamenilor din barcă.

Solutiile vor reprezenta secventele de mutari. Afisarea se va face scriind la fiecare moment de timp starea curenta (cati canibali, misionari sunt pe malul de vest, cati canibali, misionari sunt pe malul de est), dar si cati se deplaseaza cu barca intre momentele de timp consecutive (se va preciza si de la care mal pornesc barcile si catre care se duc).

Fișierul de input va conține toți parametrii problemei în formatul: "nume parametru=valoare". Sub parametrul N vor fi 2 randuri cu cate N valori (greutatile misionarilor si, respectiv, canibalilor)

Solutiile vor reprezenta secventele de mutari. Afisarea în fișierul de output se va face scriind la fiecare moment de timp:

indicele stării (nodului) în drum
informații despre starea curenta (cati canibali, misionari si ce greutăți au, pe primul mal, cati canibali, misionari si ce greutați au, pe al doilea mal)
Se va afișa între stări de la care mal pornesc bărcile si către care se duc și detaliat ce conțin
Între două soluții se va afișa un separator, de exemplu "----------------------------------"
