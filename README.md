# Ankidodawacz

Prosty i otwarty na konfigurację program do tworzenia monojęzycznych kart do Anki.<br>
Pozyskuje informacje z American Heritage Dictionary, Farlex Dictionary of Idioms i WordNet 3.1.<br>
Pozwala na szybki wybór definicji, części mowy, etymologii, synonimów oraz audio.

Celem programu jest ułatwienie i uprzyjemnienie żmudnego i zniechęcającego procesu dodawania kart, który konwencjonalnie odbywa się
za pomocą powtarzalnych ruchów myszką i przekopiowywania informacji do edytora kart.<br>Z Ankidodawaczem ten proces odbywa
się w stu procentach za pomocą klawiatury.

## Instalacja:

[link do pobrania v0.9.0-1.zip](https://github.com/gryzus24/anki-dodawacz/archive/refs/tags/v0.9.0-1.zip)
:-
[link do pobrania v0.9.0-1.tar.gz](https://github.com/gryzus24/anki-dodawacz/archive/refs/tags/v0.9.0-1.tar.gz)

### Windows:
Pobieramy .zip i rozpakowujemy.
##### Po rozpakowaniu folderu:

Aby uruchomić program potrzebujemy Pythona 3.7 lub nowszego.<br>
Pythona pobieramy z oficjalnej strony: https://www.python.org/downloads/<br>
Przy instalacji zaznaczamy "Add python to PATH"

##### Po zainstalowaniu Pythona:<br>

Otwieramy terminal (cmd na windowsie) i pobieramy wymagane biblioteki wpisując:<br>
`pip install BeautifulSoup4 colorama pyyaml requests lxml cchardet`<br>
(cchardet jest opcjonalny, ale przyspiesza wyświetlanie słowników)

Następnie wpisujemy:<br>
`cd <ścieżka do folderu z programem>`<br>
  np. `cd Pobrane`
  
Gdy jesteśmy w folderze z programem, aby uruchomić Ankidodawacza wpisujemy:<br>
`python ankidodawacz.py` lub `python3 ankidodawacz.py`<br>

Na Windowsie kliknięcie w ikonkę też powinno otworzyć program, jednak przy wystąpieniu jakiegokolwiek nieoczekiwanego błędu, okno zamknie się natychmiastowo.

### Linux:
Na Linuxie odpowiednia wersja Pythona powinna być już zainstalowana.

  Pobieramy archiwum tar.gz i rozpakowujemy
  
  Możemy użyć komendy:<br>
  `tar -xvf <pobrany tar.gz> -C <ścieżka gdzie chcemy rozpakować>`

  Instalujemy wymagane biblioteki:<br>
    `pip install BeautifulSoup4 colorama pyyaml requests lxml cchardet`

  Otwieramy za pomocą Pythona:<br>
    `python ankidodawacz.py` lub `python3 ankidodawacz.py`
    
## Konfiguracja i działanie programu

Cykl dodawanie jest bardzo prosty. Wyszukujemy słowo i przechodzimy przez różne pola: przykładowego zdania, definicji,
części mowy, etymologii i synonimów. Po przejściu przez wszystkie pola program zapisuje nasz wybór w dokumencie
tekstowym "karty.txt",<br>
który od razu jest gotowy do zaimportowania do Anki.

![image](https://user-images.githubusercontent.com/82805891/130697928-8901f8c8-a0ee-45d1-85ba-7e672de6680a.png)
  
Audio domyślnie zapisywane jest w folderze "Karty_audio" w folderze z programem.<br>
Możemy zmienić ścieżkę zapisu audio, jak i wszystkie domyślne ustawienia używając komend.

Najlepiej dodać ścieżkę do folderu "collection.media", aby audio było automatycznie odtwarzane w Anki bez potrzeby
ręcznego przenoszenia zawartości "Karty_audio".<br>
  Aby to zrobić możemy ręcznie wpisać ścieżkę używając komendy `-ap [ścieżka]`<br>
  albo wpisać `-ap auto`, aby program wyszukał ścieżkę do "collection.media" automatycznie

Customizacja wyglądu w części zależna jest od naszego emulatora terminala. Na Windowsie 10,
aby zmienić czcionkę, przeźroczystość czy wielkość okna należy kliknąć górny pasek -> właściwości. Tutaj możemy
dostosować wygląd okna do naszych preferencji.
  
![image](https://user-images.githubusercontent.com/82805891/116147106-999c3080-a6df-11eb-85ec-40de05b43a90.png)

Mamy możliwość bogatej konfiguracji z poziomu programu.  
  
![image](https://user-images.githubusercontent.com/82805891/130698280-a41c0200-aac2-49cd-b14e-eb3bf583925f.png)

## Konfiguracja Anki i AnkiConnect

Program interfejsuje z Anki za pomocą AnkiConnect.<br>
Używanie AnkiConnect przynosi wiele korzyści, takich jak:
  - bezpośrednie dodawanie kart do Anki bez potrzeby importowania pliku "karty.txt"
  - bezpośrednie dodawanie customowych notatek
  - dodawanie tagów (etykiet) do kart
  - dodatkowe opcje sprawdzania duplikatów

#### Instalacja AnkiConnect:
- Otwieramy Anki
- Wchodzimy w "Narzędzia" -> "Dodatki"
- Klikamy "Pobierz dodatki..."
- Kopiujemy kod dodatku z https://ankiweb.net/shared/info/2055492159 i restartujemy Anki

Teraz możemy przejść do Ankidodawacza i wpisać `-ankiconnect on`<br>
Zanim jednak będziemy mogli dodawać karty, musimy sprecyzować do jakiej talii mają one trafiać.<br>
  Aby to zrobić, wpisujemy `-deck [nazwa talii]`

Teraz została nam do ustawienia tylko notatka.<br>
### Konfiguracja notatek:
  Notatkę ustawiamy wpisując `-note [nazwa notatki]`
  
Program spróbuje automatycznie wykryć jakie informacje trafiają w poszczególne pola.<br>
Jeżeli jednak coś pójdzie nie tak to musimy zmienić nazwy pól naszej notatki w Anki tak, aby były zrozumiałe dla dodawacza. 
Obsługiwane pola to:
- Definicja
- Synonimy
- Przykłady
- Słowo
- Przykładowe zdanie
- Części mowy
- Etymologia
- Audio
- Nagranie

### Dodawanie przykładowych notatek:
  
Jeżeli nie chcesz używać swojej własnej notatki to możesz skorzystać z mojej przykładowej.<br>
  Aby dodać przykładową notatkę wpisujemy `--add-note gryzus-std`

Notatka posiada tryb jasny oraz ciemny.

![image](https://user-images.githubusercontent.com/82805891/122020987-c8b45180-cdb4-11eb-9c1f-20fbfb44d0d4.png)
  
Link do notatki "gryzus-std" w formie tekstowej: https://pastebin.com/9ZfWMpNu

## Importowanie ręczne

Aby zaimportować karty do Anki, na górnym pasku klikamy w "Plik" i "Importuj..." lub "Ctrl+Shift+I".

- Nawigujemy do folderu z Ankidodawaczem i wybieramy plik "karty.txt".
- Wybieramy nasz typ notatki i talię
- Klikamy w "Pola oddzielone o" i wpisujemy "\t"
- Wybieramy "Ignoruj linie, których pierwsze pole pasuje do istniejącej notatki"
- I na końcu ważne, aby zaznaczyć "Zezwól na HTML w polach"
- Jeżeli nie sprecyzowaliśmy ścieżki zapisu audio w Ankidodawaczu, musimy przenieść zawartość folderu "Karty_audio" do
  folderu "collection.media", aby audio było odtwarzane podczas powtarzania
  
![image](https://user-images.githubusercontent.com/82805891/130698679-70fe0803-c98d-405e-82fe-d540675d0d65.png)

Gdy raz ustawimy opcje importowania w Anki, nie musimy się przejmować ich ponownym ustawianiem. Ścieżka importu też
powinna zostać zapisana.

Po dodaniu kart możemy usunąć zawartość pliku "karty.txt", jednak gdy zostawimy go, importowanie nie powinno zostać
skompromitowane dzięki opcji "Ignoruj linie, których pierwsze pole pasuje do istniejącej notatki". Warto o tym pamiętać.

## Konfiguracja nagrywania
Ankidodawacz jest także prostym interfejsem do programu _ffmpeg_.<br>
Możemy:
- nagrywać audio bezpośrednio z naszego komputera lub mikrofonu
- ustawiać jakość nagrywania

Aktualnie obsługiwane systemy operacyjne i konfiguracja audio:<br>
  - Linux:    pulseaudio (z alsą)<br>
  - Windows:  dshow

Oficjalna strona ffmpeg: https://www.ffmpeg.org/download.html

Aby nagrywać audio musimy przenieść program _ffmpeg_ do folderu z programem
  lub dodać jego ścieżkę do $PATH.
Następnie wybieramy urządzenie audio za pomocą którego chcemy nagrywać audio
  wpisując `-device` lub `--audio-device`

Jeżeli nie widzimy interesującego nas urządzenia na Windowsie:
  - Włączamy "Miks stereo" w ustawieniach dźwięku
  - Zaznaczamy "nasłuchuj tego urządzenia"
  - Zezwalamy aplikacjom na wykorzystywanie mikrofonu

Na Linuxie jest dosyć duża szansa, że _ffmpeg_ jest zainstalowany i jest dostępny w $PATH.<br>
Więc jedyne co musimy zrobić to:<br>
  - Wpisujemy `-rec` w Ankidodawaczu
  - podczas nagrywania wchodzimy w mikser dźwięku pulseaudio -> Nagrywanie
  - zmieniamy urządzenie monitorujące dla Lavf na urządzenie wybrane przy konfiguracji za pomocą `-device` lub `--audio-device`

## Kod

Jestem początkujący, jeżeli chodzi o programowanie. Jest to mój pierwszy projekt i jakość kodu z pewnością pozostawia wiele do życzenia.

Jestem otwarty na sugestie i krytykę. Mam nadzieję, że narzędzie okaże się pomocne.

Użyte biblioteki: BeautifulSoup4, requests, colorama, pyyaml, lxml
