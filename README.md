Projekt zaliczniowy dla przedmiotu **Infrastruktura systemowa**
Weronika Tlałka (380373) i Przemysław Bukowski (386126)


## Opis

W ramach projektu stworzsyliśmy prostą aplikację, połączoną z bazą danych PostgreSQL. 
Aplikacja ma za zadanie wyświetlać id, autora, tytuł i ISBN ksiązek, które znajdują się w bazie danych.
Ksiązki mozna do bazy dodawać, edytować je oraz usuwać. 


## Docker-compose

### Kontenery 

Utworzono 2 kontenery:

- kontener bazy danych: **database**:
    - nadano mu nazwę *database*, 
    - wykorzystano obraz bazy *postgres*, 
    - zdefiniowano zmienne środowiskowe dostępu do bazy danych *booksdb*, 
    - ustawiono port nasłuchwiania na standardowy dla bazy PostgreSQL - 5432, 
    - uzyto ''' volumes: ''' aby wprowadzane dane były trwałe (a nie znikały po zbiciu kontenera).

- kontener aplikacji: **booksapp** (najpierw zbudowano kontener, wypchnięto własny obraz na serwer *DockerHub*, a następnie uzyto tego obrazu):
    - nadano kontenerowi nazwę *booksapp*,
    - uzyto wlasnego obrazu (*infrastruktura-systemowa*) utworzonego z *Dockerfile*,
    - ustawiono port na 5001 (aostał on wybrany ze względu na to, ze port 5000, standardowo uzywany dla tego typu aplikacji, był juz zajęty przez inny proces)
    - zdefiniowano środowisko uwzględniając aplikację FLASK,
    - ustawiono *restart* na *always* w razie gdyby baza danych nie wstała pierwsza po uruchomieniu,
    - dodano zaleznosc tego kontenera, od kontenera bazy danych.


### Uruchomienie
Aby uruchomić aplikację, nalezy otworzyć kartę terminala/konsoli w folderze, w którym znajduje się aplikacja.
Następnie nalezy uzyć następującego polecenia:

''' docker-compose up '''

W ten sposób kontener z serwisami aplikacji (app) i bazy danych (db) zostanie uruchomiony.
Nie trzeba uzywać ''' docker-compose build ''' poniewaz oba kontenery korzystają z gotowych obrazów 
(gdyby zamiast "image: ..." w kontenerze app uzyć "build: ." wówczas nalezałoby najpierw uzyc instrukcji *docker-compose build*).

### Sprawdzenie
Aplikację będzie mozna wyświetlić w przeglądarce pod następującym adresem:

- *http://localhost:5001/books* dla wyświetlenia listy ksiązek
- *http://localhost:5001/books/id* (gdzie *id* nalezy zastąpić dowolnym id ksiązki) dla wyswietlenia i edycji pojedynczej pozycji

### Modyfikacja ksiązek

Zawartość w bazie mozna modyfikować na kilka sposobów. Jednym z nich jest zalogowanie się do bazy danych wewnątrz kontenera za pomocą poleceń:

''' docker exec -it [id kontenera] bash '''
''' psql -U postgres '''

Inny sposób to skorzystanie z polecenia ***cURL*** aby wysłać dane za pomocą protokołu HTTP na serwer.

#### Dodanie ksiązki

''' curl -X POST -H "Content-Type: application/json" -d '{"title": "Buszujacy w zbozu", "author": "J.D. Salinger", "isbn": "0316769487"}' http://localhost:5001/books '''

#### Usunięcie ksiązki 

''' curl -X DELETE http://localhost:5001/books/1 '''

#### Aktualizacja ksiązki 

''' curl -X PUT -H "Content-Type: application/json" -d '{"title": "Wielki Gatsby", "author": "F. Scott Fitzgerald", "isbn": "0743273567"}' http://localhost:5000/books/1 '''


## Kubernetes (k8s)

### Utworzono

- Deployment (baza danych) - wdrozenie
- Deployment (aplikacja) - wdrozenie
- Service (baza danych) - sposob dostepu z zewnatrz klastra
- Service (aplikacja) - sposob dostepu z zewnatrz klastra
- ConfigMap - zbiór zmiennych środowiskowych 
- PersistentVolumeClaim - zdefiniowane ządanie do wolumenu przechowującego dane

Wszystkie zasoby umieszczono w jednym pliku jako, ze jest to zalecana praktyka.

### Uruchomienie 

Aby uruchomić aplikację, nalezy w oknie terminala skorzystać z komendy:

''' kubectl apply -f k8s.yml '''

### Sprawdzanie statusu podów i serwisów

Mozna sprawdzić aktualne statusy podów i serwisów za pomoca komend w terminalu:

''' kubectl get pods '''
''' kubectl get services '''
