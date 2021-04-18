import math
import copy
import sys
import time

class Graph:

    def __init__(self, nume_fisier):

        f = open(nume_fisier,"r")
        textFisier = f.read()
        listaInfoFisier = textFisier.split("\n")
    
        for i in range(len(listaInfoFisier)):
            txt = listaInfoFisier[i].split("=")

            if(txt[0] == 'N'):
                self.__class__.N = int(txt[1])
                self.vectM = [int(x) for x in listaInfoFisier[i+1].split(' ')]
                self.vectM.sort()
                self.vectC = [int(x) for x in listaInfoFisier[i+2].split(' ')]
                self.vectC.sort()
                i = i + 2

            elif(txt[0] == 'M'):
                self.__class__.M = int(txt[1])

            elif(txt[0] == "GMAX"):
                self.__class__.GMAX = int(txt[1])

            elif(txt[0] == "MalInitial"):
                self.__class__.malInitial = txt[1]

            elif(txt[0] == "MalFinal"):
                self.__class__.malFinal = txt[1]

        self.__class__.Misionari = copy.deepcopy(self.vectM)
        self.__class__.Canibali = copy.deepcopy(self.vectC)
        self.start = (self.vectM, self.vectC, 1, [], []) # informatia nodului de start aka *nodInfo*
        self.scopuri = [([], [], 0, self.__class__.Misionari, self.__class__.Canibali),([], [], 1, self.__class__.Misionari, self.__class__.Canibali)]

    def testeaza_scop(self, nodCurent):

        return nodCurent.info in self.scopuri

    def afis(self):

        print("N = ", self.__class__.N)
        print("M = ", self.__class__.M)
        print("vectM = ", self.vectM)
        print("vectC = ", self.vectC)
        print("GMAX = ", self.__class__.GMAX)
        print("malInit = ", self.__class__.malInitial)
        print("malFin = ", self.__class__.malFinal)

    def genereazaSuccesori(self, nodCurent, tip_euristica = "euristica banala"):

        def test_conditie(mis, can):

            return mis==0 or mis>=can

        def testConditieBarca(misionari, canibali):

            if(len(misionari) > 0):
                if(len(misionari) < len(canibali)):
                    return False
            if(sum(misionari) + sum(canibali) > self.__class__.GMAX):
                return False
            return True

        def calculeazaVectori(l1, l2):

            return list(set(l1) - set(l2))
            

        listaSuccesori = []
        #nodCurent.info va contine un triplet (vectMisInitial, vectCanInitial, barca, vectMisOpus, vectCanOpus)
        barca = nodCurent.info[2]
        
        if barca == 1: #pe mal initial
            misMalCurent = len(nodCurent.info[0])
            canMalCurent = len(nodCurent.info[1])
            canMalOpus = Graph.N - canMalCurent
            misMalOpus = Graph.N - misMalCurent
        else:
            misMalOpus = len(nodCurent.info[0])
            canMalOpus = len(nodCurent.info[1])
            canMalCurent = Graph.N - canMalOpus                 
            misMalCurent = Graph.N - misMalOpus                 
        maxMisionariBarca = min(Graph.M, misMalCurent)

        for misBarca in range(maxMisionariBarca + 1):

            if misBarca == 0:
                maxCanibaliBarca = min(Graph.M, canMalCurent)
                minCanibaliBarca = 1
            else:
                maxCanibaliBarca = min(Graph.M - misBarca, canMalCurent, misBarca)
                minCanibaliBarca = 0

            for canBarca in range(minCanibaliBarca, maxCanibaliBarca+1):
                #consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca
                canMalCurentNou = canMalCurent-canBarca
                misMalCurentNou = misMalCurent-misBarca
                canMalOpusNou = canMalOpus+canBarca
                misMalOpusNou = misMalOpus+misBarca

                if not test_conditie(misMalCurentNou,canMalCurentNou ):
                    continue

                if not test_conditie(misMalOpusNou,canMalOpusNou ):
                    continue
                
                if not testConditieBarca(nodCurent.info[0][0:misBarca], nodCurent.info[1][0:canBarca]):
                    continue

                if barca == 1: #testul este pentru barca nodului curent (parinte) deci inainte de mutare
                    misionariAici = nodCurent.info[0][misBarca:]
                    canibaliAici = nodCurent.info[1][canBarca:]
                    misionariOpus = nodCurent.info[3] + nodCurent.info[0][0:misBarca]
                    misionariOpus.sort()
                    canibaliOpus = nodCurent.info[4] + nodCurent.info[1][0:canBarca]
                    canibaliOpus.sort()
                    infoNodNou = (misionariAici, canibaliAici, 0, misionariOpus, canibaliOpus)

                else:                        
                    misionariAici = nodCurent.info[3][misBarca:]
                    canibaliAici = nodCurent.info[4][canBarca:]
                    misionariOpus = nodCurent.info[0] + nodCurent.info[3][0:misBarca]
                    misionariOpus.sort()
                    canibaliOpus = nodCurent.info[1] + nodCurent.info[4][0:canBarca]
                    canibaliOpus.sort()
                    infoNodNou = (misionariOpus, canibaliOpus, 1, misionariAici, canibaliAici)

                if not nodCurent.contineInDrum(infoNodNou):
                    costSuccesor = sum(nodCurent.info[0][0:misBarca]) + sum(nodCurent.info[1][0:canBarca])
                    listaSuccesori.append(NodParcurgere(infoNodNou,nodCurent,cost = nodCurent.g + costSuccesor, h = nodCurent.gr.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori            

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):

        if tip_euristica=="euristica banala":

            if infoNod not in self.scopuri:
                return 1

            return 0  

        elif tip_euristica == "euristica admisibila":
            #calculez cati oameni mai am de mutat si impart la nr de locuri in barca
            #totalOameniDeMutat=infoNod[0]+infoNod[1]
            return 2*math.ceil((len(infoNod[0])+len(infoNod[1]))/self.M) + (1-infoNod[2]) - 1 
            #(1-infoNod[2]) vine de la faptul ca daca barca e pe malul final trebuie sa mai faca o trecere spre malul initial #
            # ca sa ii ia pe oameni, pe cand daca e deja pe malul initial, nu se mai aduna acel 1
    
    def __repr__(self):

        sir=""

        for (k,v) in self.__dict__.items() :
            sir+="{} = {}\n".format(k,v)

        return(sir)



class NodParcurgere:
    gr = None
    def __init__(self, info, parinte, cost=0, h=0):

        self.info=info
        self.parinte=parinte #parintele din arborele de parcurgere
        self.g=cost #consider cost=1 pentru o mutare
        self.h=h
        self.f=self.g+self.h


    def getDrum(self):

        list = [self]
        #
        # print(list)
        nod = self

        while nod.parinte is not None:
            list.insert(0, nod.parinte)
            nod = nod.parinte

        return list

    def afisDrum(self, afisCost=False, afisLung=False): #returneaza si lungimea drumului

        l = self.getDrum()

        for index, nod in enumerate(l):

            if nod.parinte is not None:

                if nod.parinte.info[2]==1:
                    mbarca1=self.__class__.gr.malInitial
                    mbarca2=self.__class__.gr.malFinal
                else:
                    mbarca1=self.__class__.gr.malFinal
                    mbarca2=self.__class__.gr.malInitial
                    f.write("\nIndexul starii (nodului): ")
                    f.write(str(int(index/2)))
                    f.write("\nMisionari pe mal curent:")
                    f.write(str(len(nod.info[3])))
                    f.write("\nGreutati:")
                    f.write(str(nod.info[3]))
                    f.write("\nCanibali pe mal curent: ")
                    f.write(str(len(nod.info[4])))
                    f.write("\nGreutati: ")
                    f.write(str(nod.info[4]))
                    f.write("\nMisionari pe mal opus:")
                    f.write(str(len(nod.info[0])))
                    f.write("\nGreutati:")
                    f.write(str(nod.info[0]))
                    f.write("\nCanibali pe mal opus: ")
                    f.write(str(len(nod.info[1])))
                    f.write("\nGreutati: ")
                    f.write(str(nod.info[1]))
                    f.write("\nBarca s-a deplasat de la malul %s la malul %s cu %d oameni."%(mbarca1,mbarca2, abs(len(nod.info[0])+len(nod.info[1])-len(nod.parinte.info[0])-len(nod.parinte.info[1]))))
                f.write("\n")
                f.write(str(nod))

        if afisCost:
            f.write("Cost: ")
            f.write(str(self.g))
            f.write("\n")

        if afisCost:
            f.write("Lungimea drumului: ")
            f.write(str(len(l)))
            f.write("\n")

        f.write("Timp: ")
        f.write(str(time.time()-start))
        f.write("\n")

        return len(l)
        
    def contineInDrum(self, infoNodNou):

        nodDrum=self

        while nodDrum is not None:

            if(infoNodNou == nodDrum.info):
                return True

            nodDrum = nodDrum.parinte

        return False
            
    def __repr__(self):

        sir=""          
        sir+=str(self.info)

        return(sir)

    def __str__(self):

        return str(self.info)+"\n"


def a_star(gr, nrSolutiiCautate, tip_euristica):

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    #                    info, parinte, g = 0, h = 0
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    
    while len(c)>0:
        nodCurent=c.pop(0)
        
        if gr.testeaza_scop(nodCurent):
            f.write("\nSolutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            f.write("\n----------------\n")
            #input()
            nrSolutiiCautate-=1

            if nrSolutiiCautate==0:
                return

            if time.time() - start > Time:  # verificam daca am depasit timpul de executie
                f.write("Out of time\n")
                return

        lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica) 

        for s in lSuccesori:
            i=0
            gasit_loc=False

            for i in range(len(c)):
                    #diferenta fata de UCS e ca ordonez dupa f

                    if c[i].f>=s.f :
                            gasit_loc=True
                            break

            if gasit_loc:
                    c.insert(i,s)
            else:
                    c.append(s)

def uniform_cost(gr, nrSolutiiCautate=1):

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(gr.start, None, 0)]
    
    while len(c)>0:
        #print("Coada actuala: " + str(c))
        #input()
        nodCurent=c.pop(0)
        
        if gr.testeaza_scop(nodCurent):
            f.write("\nSolutie: \n")
            nodCurent.afisDrum()
            f.write("\n----------------\n")
            nrSolutiiCautate-=1

            if nrSolutiiCautate==0:
                return

        lSuccesori=gr.genereazaSuccesori(nodCurent) 

        for s in lSuccesori:
            i=0
            gasit_loc=False

            for i in range(len(c)):

                #ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g>s.g :
                    gasit_loc=True
                    break

            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)



def a_star_optimizat(gr):

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    
    #l_open contine nodurile candidate pentru expandare

    #l_closed contine nodurile expandate
    l_closed=[]

    while len(l_open)>0:
        #print("Coada actuala: " + str(l_open))
        #input()
        nodCurent=l_open.pop(0)
        l_closed.append(nodCurent)

        if gr.testeaza_scop(nodCurent):
            f.write("\nSolutie: \n")
            nodCurent.afisDrum()
            f.write("\n----------------\n")
            return

        lSuccesori=gr.genereazaSuccesori(nodCurent) 

        for s in lSuccesori:
            gasitC=False

            for nodC in l_open:

                if s.info==nodC.info:
                    gasitC=True

                    if s.f>=nodC.f:

                        try:
                            lSuccesori.remove(s)
                        except:
                            pass

                    else:#s.f<nodC.f
                        l_open.remove(nodC)

            if not gasitC:

                for nodC in l_closed:

                    if s.info==nodC.info:

                        if s.f>=nodC.f:

                            try:
                                lSuccesori.remove(s)
                            except:
                                pass

                        else:#s.f<nodC.f
                            l_closed.remove(nodC)

        for s in lSuccesori:
            i=0
            gasit_loc=False

            for i in range(len(l_open)):
                #diferenta fata de UCS e ca ordonez crescator dupa f
                #daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f>s.f or (l_open[i].f==s.f and l_open[i].g<=s.g) :
                    gasit_loc=True
                    break

            if gasit_loc:
                l_open.insert(i,s)
            else:
                l_open.append(s)

def ida_star(gr):
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    
    while len(c)>0:
        nodCurent=c.pop(0)
        
        if gr.testeaza_scop(nodCurent):
            f.write("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            f.write("\n----------------\n")
            # input()
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return

        lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica) 

        for s in lSuccesori:
            i=0
            gasit_loc=False

            for i in range(len(c)):
                    #diferenta fata de UCS e ca ordonez dupa f
                    if c[i].f>=s.f :
                            gasit_loc=True
                            break

            if gasit_loc:
                    c.insert(i,s)
            else:
                    c.append(s)


start=time.time()

input_path = sys.argv[1]
output_path = sys.argv[2]+"\\"+"output_"+input_path.split("\\")[-1]
f = open(output_path, "w")
gr=Graph(sys.argv[1])    

gr.afis()
NodParcurgere.gr=gr
f.write("\n\n##################\nSolutii obtinute cu A*:")
nrSolutiiCautate = int(sys.argv[3])
Time = int(sys.argv[4])

a_star(gr, nrSolutiiCautate, tip_euristica="euristica banala")

f.write("\n\n##################\nSolutii obtinute cu UCS:")
uniform_cost(gr,nrSolutiiCautate=4)


f.write("\n\n##################\nSolutii obtinute cu A* optimizat:")
a_star_optimizat(gr)
f.close()
