# tsoha-keskusteluapp - Live demo @ https://tsoha-chatapp.herokuapp.com

KeskusteluApp on klassinen keskutelufoorumi, johon käyttäjät voivat luoda viestiketjuja keskustelualueille ja lisätä niihin uusia viestejä sekä muokata niitä. 

KeskusteluApp on toteutettu käyttäen Pythonin [Flask](https://palletsprojects.com/p/flask/) kirjastoa.

## Ominaisuudet
- Käyttäjä voi luoda uuden tunnuksen ja kirjautua sillä sisään sekä ulos.
- Käyttäjä voi antaa itselleen profiilikuvan.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

## Edistys
- [x] Kirjautuminen ja rekisteröityminen
- [x] Keskustelualueen luominen
- [x] Keskusteluketjun luominen, muokkaaminen ja poistaminen
- [x] Keskusketjuun viestin lisääminen, muokkaaminen ja poistaminen
- [x] Oikeuksien tarkastaminen
- [x] Haku
- [x] Sisällön postaminen
- [x] Profiilin muokkaaminen
- [x] CSRF
- [ ] Profiili kuvat

## Asennus
```bash
$ git clone https://github.com/PaulusParssinen/tsoha-keskusteluapp.git
$ cd tsoha-keskusteluapp

$ virtualenv env
$ source env/bin/activate

$ pip3 install -r requirements.txt

# Kopioi pohja ja aseta siinä vaaditut asetukset
$ cp .env.example .env

# Jos haluat kehittäjäympäristön käyttöön
$ export FLASK_ENV=development

$ flask run
```