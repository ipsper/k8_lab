# För att få ut loggar eller debug-information från ett Docker-container-kommando som docker run, kan du använda följande metoder:

1. Visa loggar med docker logs
   Om du redan har startat en container med docker run, kan du se dess loggar med:

docker logs <container-id>
För att följa loggar i realtid, använd flaggan -f:

docker logs -f <container-id>

2. Visa loggar direkt i terminalen
   När du kör en container med docker run, visas dess standardutdata (stdout och stderr) i terminalen om du inte använder flaggan -d (detached mode). Exempel:

docker run --name my-container my-image
För att få debug-information kan du behöva aktivera verbose- eller debug-lägen i det program som körs inuti containern.

3. Kör Docker i debug-läge
   Om du vill få debug-information från Docker själv (daemonen), kan du köra Docker-demonen i debug-läge. Detta kräver att du ändrar demonens inställningar:

Lägg till flaggan --debug när du startar Docker-demonen:

dockerd --debug
Eller aktivera debug-läget i konfigurationsfilen /etc/docker/daemon.json:

json
￼Copy code
{
"debug": true
}
Starta om Docker-demonen efter ändringen:

systemctl restart docker

4. Visa debug-information vid körning
   Om du vill köra docker run med mer detaljerad information om själva körningen, kan du använda verbose-läget med docker-klienten:

DOCKER_CLI_DEBUG=1 docker run my-image

5. Få mer information om fel
   Om containern avslutas oväntat, kan du kontrollera dess utgångsstatus med:

docker inspect <container-id>
Särskilt delen under State kan ge insikter om varför containern slutade.

Behöver du hjälp med en specifik situation eller logg?

## Om containern inte startar alls, kan du felsöka problemet med följande steg:

1. Kör containern interaktivt
   Om containern kraschar direkt vid start, kan du testa att köra den interaktivt för att se vad som händer:

docker run -it <image-name> /bin/bash
Byt ut /bin/bash med en annan shell (t.ex. /bin/sh) om det inte finns något bash i bilden. Detta låter dig starta containern och inspektera filsystemet och loggar manuellt.

2. Inspektera loggar från containern
   Om containern hinner generera loggar innan den kraschar, kan du se dem med:

docker logs <container-id>
Om du kör docker run utan -d (detached mode), kommer loggarna att visas direkt i terminalen.

3. Få mer detaljer om felet med docker inspect
   Kör följande för att inspektera containerns tillstånd:

docker inspect <container-id>
Sök efter sektionen State, där du kan hitta information som ExitCode och eventuell Error. Exempel:

json
￼Copy code
"State": {
"Status": "exited",
"ExitCode": 1,
"Error": "",
"StartedAt": "2025-01-03T10:00:00Z",
"FinishedAt": "2025-01-03T10:00:05Z"
}
ExitCode 1 indikerar generellt ett applikationsfel.
Error kan ge mer specifik information.

4. Testa med --entrypoint för att kringgå entrypointen
   I vissa fall kan problemet ligga i en felaktig eller oåtkomlig entrypoint i bilden. Prova att åsidosätta entrypointen:

docker run --entrypoint /bin/sh -it <image-name>
Detta startar containern med ett skal istället för det fördefinierade kommandot, så att du kan inspektera miljön.

5. Byt ut kommandot som körs
   Om du misstänker att kommandot som körs i containern är orsaken, kan du testa att köra ett enklare kommando:

docker run <image-name> echo "Hello, World!"
Om detta fungerar, är det troligt att själva kommandot i din Dockerfile eller CMD är felkonfigurerat.

6. Kör med ökad verbosity
   Aktivera debug-information från Docker-klienten:

DOCKER_CLI_DEBUG=1 docker run <image-name>
Detta ger mer detaljerad information om vad som händer bakom kulisserna.

7. Kontrollera bilden
   Om bilden är trasig eller inkompatibel kan det orsaka problem. Kontrollera dess struktur:

Lista lager med:

docker history <image-name>
Bygg om bilden (om du har tillgång till Dockerfile):

docker build -t <image-name> . 8. Debugga med docker-compose
Om du använder docker-compose, kan du lägga till tty: true eller ändra kommandot i docker-compose.yml för att testa interaktivt:

services:
my-service:
image: my-image
command: /bin/bash
tty: true

Om problemet kvarstår, dela gärna detaljer som felmeddelanden, din Dockerfile eller vilka steg som leder till problemet!

Om problemet med containern är nätverksrelaterat, kan du felsöka och åtgärda detta genom följande steg:

1. Testa nätverksåtkomst i containern
   Kör en tillfällig container och testa om nätverket fungerar som förväntat:

docker run --rm alpine ping -c 4 8.8.8.8
Om detta fungerar, har containern åtkomst till internet.
Om det misslyckas, kan det finnas ett problem med Docker-nätverkskonfigurationen.

2. Inspektera nätverket
   Lista alla Docker-nätverk för att se vilka som är tillgängliga:

docker network ls
Inspektera ett specifikt nätverk för att se dess inställningar:

docker network inspect <network-name>
Vanligtvis använder Docker nätverket bridge som standard. Kontrollera att containern är ansluten till rätt nätverk.

3. Testa med ett annat nätverk
   Om nätverket bridge inte fungerar, kan du prova att köra containern med nätverket host (använder värdmaskinens nätverksstack):

docker run --network host <image-name>
Observera att host-nätverket inte är tillgängligt på Windows och macOS på samma sätt som på Linux.

4. Åtgärda DNS-problem
   Om containern inte kan lösa domännamn (t.ex. google.com), kan problemet ligga i Docker DNS-konfigurationen. Du kan specificera en DNS-server manuellt:

docker run --dns 8.8.8.8 <image-name>
Alternativt kan du lägga till följande i /etc/docker/daemon.json för att sätta en global DNS:

json
￼Copy code
{
"dns": ["8.8.8.8", "1.1.1.1"]
}
Starta om Docker-demonen efter ändringen:

systemctl restart docker

5. Kontrollera brandväggar
   En brandvägg på värdmaskinen kan blockera nätverkstrafiken för Docker. Kontrollera brandväggsreglerna och säkerställ att Docker tillåts:

På Linux:

sudo iptables -L -n
På Windows eller macOS: Kontrollera inställningarna i systemets brandvägg eller säkerhetsprogramvara.

6. Skapa ett eget nätverk
   Om det förvalda bridge-nätverket har problem, kan du skapa ett nytt nätverk och ansluta containern till det:

docker network create my-custom-network
docker run --network my-custom-network <image-name>

7. Testa med --net=none för isolering
   För att felsöka om problemet är nätverksberoende, kan du isolera containern helt:

docker run --net=none <image-name>
Detta bekräftar om nätverket påverkar uppstarten av containern.

8. Inspektera Docker-demonen
   Kontrollera om det finns några fel i Docker-demonens loggar relaterade till nätverk:

sudo journalctl -u docker
