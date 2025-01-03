# container storage

## DockerHub är en populär plats för att lagra och hantera Docker-images. Det är en offentlig container registry som gör det enkelt att dela och distribuera images

## du kan använda GitHub som en alternativ plats för att lagra och hantera Docker-images genom att använda GitHub Container Registry (GHCR). GHCR är en container registry som är inbyggd i GitHub och fungerar på ett liknande sätt som DockerHub. Här är hur du kan använda det:

1. Skapa ett GitHub Personal Access Token
   Gå till Settings > Developer settings > Personal access tokens på GitHub.
   Generera ett token med tillstånd för write:packages och read:packages.
2. Logga in till GHCR från Docker CLI
   Kör följande kommando i terminalen och ange ditt GitHub-användarnamn och token:

echo <PAT> | docker login ghcr.io -u <username> --password-stdin 3. Bygga och tagga en image
Bygg och tagga din Docker-image för GHCR:

docker build -t ghcr.io/<username>/<image-name>:<tag> . 4. Push din image till GHCR
När bilden är byggd och taggad kan du pusha den till GitHub Container Registry:

docker push ghcr.io/<username>/<image-name>:<tag> 5. Dra ner en image från GHCR
För att använda en bild från GHCR kan du dra ner den med:

docker pull ghcr.io/<username>/<image-name>:<tag>
Fördelar med att använda GitHub som DockerHub
Integration: Om du redan använder GitHub för källkodshantering är det smidigt att hålla allt på ett ställe.
Åtkomstkontroll: Du kan använda GitHub-repositoriets befintliga åtkomstregler för att styra vem som får tillgång till dina images.
Kostnad: GitHub erbjuder gratis lagring och överföring inom vissa gränser.
Nackdelar
DockerHub är fortfarande mer etablerat för containerdistribution och har fler användare.
Om du använder Docker-compose eller andra verktyg kan du behöva konfigurera lite extra för att använda GHCR.
