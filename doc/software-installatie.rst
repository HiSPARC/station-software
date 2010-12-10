.. include:: subst.inc

Installatie van de |hisparc| software
=====================================

De installatie van de |hisparc| software is recent zeer vereenvoudigd
[#ooti]_.  We maken nu gebruik van één installatiepakket dat alle
benodigde software op de |hisparc| detector pc's installeert.  We raden
aan om de software te installeren op een moderne pc met een schone
installatie van Microsoft Windows XP.  Windows Vista en Windows 7 zouden
in principe ook moeten werken, maar daarop is de software niet getest.
Mocht u de software toch willen installeren op deze besturingssystemen,
dan horen we graag over uw ervaringen.  De keuze voor Windows is slechts
gemaakt omdat een aantal systeembeheerders in het voortgezet onderwijs
alleen ervaring heeft met Windows en in het verleden aangaf geen Linux
pc's toe te staan op het schoolnetwerk.  Voor het ondersteunen van meer
dan één besturingssysteem hebben we helaas niet de mankracht.

.. note:: Vóór uiteindelijk gebruik is het nodig de |hisparc| data
   acquisitie software te configureren! Zie :doc:`configuratie`.

.. note:: Op het science park en de TU/E maken we sinds kort gebruik van
   Asus EEE PC's.  Deze pc's zijn goedkoop, hebben voldoende geheugen,
   zijn energiezuinig, compact en snel genoeg voor onze doeleinden.  De
   pc's worden geleverd met Microsoft Windows XP Home en ook dat is
   voldoende.  Let wel: een monitor wordt *niet* meegeleverd; toetsenbord
   en muis weer wel.

.. note:: Op aanvraag is alle broncode beschikbaar.  Wilt u zelf met
   |labview| aan de slag, bijvoorbeeld, dan kunt u contact met ons opnemen
   en de broncode van de data acquisitie software ontvangen.  Bent u of
   zijn uw leerlingen geïnteresseerd in hoe het verwerken en uploaden van
   de |hisparc| data in zijn werk gaat, kijkt u dan na installatie in de
   ``Z:\user\hsmonitor\src`` map.  Hier vindt u de Python [#python]_
   broncode van de |hisparc| monitor.


Verwijderen van een oude software installatie
---------------------------------------------

.. note:: Installeert u de |hisparc| software voor het eerst, dan kunt u
   deze sectie overslaan.  Het volgende is alléén bedoeld voor diegenen
   die een oude versie van de |hisparc| software hebben geïnstalleerd, te
   herkennen aan de opsplitsing in meerdere installatiepakketten: *Client,
   Monitor, Buffer en LabVIEW*.

U werkte al eerder met de nieuwe electronica
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

De nieuwe |hisparc| software biedt vele verbeteringen, waaronder het
onderbrengen van alle software in één installatiepakket.  Voordat de
nieuwe software geïnstalleerd kan worden dient de oude software verwijderd
te zijn.

Ga hiervoor naar *Start -> Settings -> Control Panel -> Add or Remove
Programs*.  En verwijder, *in deze volgorde*, de volgende pakketten:

* |hisparc| Monitor
* |hisparc| Client
* |hisparc| Buffer
* HiSPARCII V3.0.2 (of een vergelijkbare versie, in sommige gevallen zelfs
  nog 2.1.1)

.. note:: Het is belangrijk om de |hisparc| user accounts van het systeem
   te verwijderen.

U heeft nu voor het eerst alle electronica vervangen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Wij raden u ten sterkste aan uw pc te vervangen of in ieder
   geval Windows XP opnieuw te installeren.  Dit omdat uw installatie
   hoogstwaarschijnlijk al jaren oud is.

Mocht u tóch besluiten om alleen de oude software te verwijderen, dan gaat
het om de volgende pakketten:

* Trimble GPS
* |hisparc| software versie 6
* PicoScope


Benodigdheden
-------------

Vóór u aan de installatie begint dient u te beschikken over:

* ``hisparcInstaller_v3.7.exe``
* een door de clustercoördinator verstrekt beveiligingscertificaat,
  bijvoorbeeld: ``sciencepark501.zip``
* een door de clustercoördinator verstrekt stationnummer
* een wachtwoord, uniek voor dit station, door de clustercoördinator
  verstrekt of door uzelf gekozen.  Dit wachtwoord wordt gebruikt als
  controle op een vergissing in stationnummers.  Denkt u er in het geval
  van een zelfgekozen wachtwoord aan dit wachtwoord aan de
  clustercoördinator te vestrekken.
* de naam van uw pc zoals gebruikt in ons monitorsysteem
  (:ref:`nagios-doc`).  Dit is niet vereist voor de installatie, maar wel
  handig om na afloop en tijdens gebruik de status van uw detector te
  controleren.

.. note:: U dient zich bij uw *systeembeheerder* te verzekeren van het
   volgende:
   
   * Een proxy-vrije verbinding vanaf de |hisparc| pc over
     *poort 443 (https)* naar *vpn.hisparc.nl* is **vereist**.  Het gaat
     hier dus alleen om de verbinding **naar buiten**.
   * Een proxy-vrije verbinding vanaf de |hisparc| pc over
     *poort 80 (http)* naar *peene.nikhef.nl* en *frome.nikhef.nl* is
     **gewenst**.

.. note:: Stel de pc in de *BIOS setup* zódanig in dat hij in het geval
   van stroomuitval automatisch weer opstart.  Bij een *EEE PC* kan dat
   door vlak na het aanzetten op *DEL* te drukken en dan in de setup het
   tabblad *Power* te kiezen, dan het menu *APM configuration* en bij de
   optie *Restore  on AC Power Loss* de optie *Last State* te kiezen.  Dit
   betekent een herstart bij stroomuitval, maar als de computer handmatig
   uit was gezet, dan blijft hij uit.

.. figure:: images/screenshot-files.png
   :align: center
   :scale: 85

   Een folder met de installer en het beveiligingscertificaat.


Installatieprocedure
--------------------

De installatieprocedure is eenvoudig te doorlopen.  Hieronder volgt een
aantal screenshots van de installer met een korte beschrijving.

Welkom
^^^^^^

Dit venster spreekt voor zich.

.. figure:: images/screenshot-welkom.png
   :align: center
   :scale: 85

   De welkomstpagina van de installer.  Dit is het eerste dat u ziet
   nadat de installer is gestart.

Stationgegevens
^^^^^^^^^^^^^^^

In dit venster dient u de stationgegevens in te vullen: stationnummer en
wachtwoord.  Het beveiligingscertificaat kan geladen worden door ofwel de
lokatie in te vullen of, handiger, op het knopje naast het veld te
klikken en het bestand te selecteren.

.. figure:: images/screenshot-stationgegevens.png
   :align: center
   :scale: 85

   De installer vraagt om het invullen van de stationgegevens.

Lokale database
^^^^^^^^^^^^^^^

Als uw school of instelling beschikt over de nodige software om |hisparc|
data te ontvangen, te verwerken en langdurig op te slaan, dan kunt u hier
het adres invullen.  Voor vrijwel alle installaties blijft dit veld leeg.

.. figure:: images/screenshot-lokaledatabase.png
   :align: center
   :scale: 85

   Het is mogelijk om een lokale database op te geven.  Normaliter blijft
   dit veld leeg.

.. note:: Op dit moment is er geen installatiepakket of handleiding
   voorhanden om zelf de benodigde serversoftware te installeren.  Op
   aanvraag is alle broncode beschikbaar.

Aangesloten detectoren
^^^^^^^^^^^^^^^^^^^^^^

In dit venster kunt u aangeven welke detectoren u heeft aangesloten.
Meestal is dit slechts een |hisparc| detector, maar in de toekomst willen
we op zoveel mogelijk lokaties ook weerstations gebruiken.  Weerstations
stellen ons in staat om de |hisparc| metingen nauwkeurig te koppelen aan
o.a. actuele luchtdruk en temperatuur waarnemingen.

.. figure:: images/screenshot-detectoren.png
   :align: center
   :scale: 85

   Hier vinkt u de aangesloten detectoren aan.  Dit station beschikt
   alleen over een |hisparc| detector.

Installatie
^^^^^^^^^^^

De installatie kan, afhankelijk van de snelheid van uw computer, wat tijd
in beslag nemen.  Vooral het uitvoeren van de zogeheten *adminUpdater*
(zie screenshot) kan even duren.

Tijdens de installatie wordt een driver geïnstalleerd voor een virtuele
netwerkkaart, de zogeheten *TAP adapter*.  Deze netwerkkaart wordt
gebruikt door *OpenVPN*.  Deze software maakt een beveiligde
netwerkverbinding met onze servers op het Nikhef door middel van een
*Virtual Private Network*.  Deze driver is niet officieel door Microsoft
gecertificeerd en daarom moet u expliciet toestemming geven voor de
installatie.

.. note:: Het is *noodzakelijk* dat u toestemming geeft voor de
   installatie van de TAP driver.  In tegenstelling tot wat de
   waarschuwing sterk suggereert zijn hieraan geen risico's verbonden.
   Voor programmeurs die hun software gratis ter beschikking stellen,
   zoals de auteurs van de TAP driver, is het niet op te brengen Microsoft
   te betalen voor hun Windows Logo test programma.  Het enige dat dit op
   zou leveren is het niet verschijnen van deze waarschuwing.

.. figure:: images/screenshot-installatie.png
   :align: center
   :scale: 85

   De installatie is in volle gang.  Dit kan enige tijd duren.

.. figure:: images/screenshot-tapdriver.png
   :align: center
   :scale: 85

   De installatie van de TAP driver (virtuele netwerkkaart voor OpenVPN)
   is niet officieel door Microsoft gecertificeerd.  Daarom moet u
   expliciet toestemming geven voor de installatie.

Herstart
^^^^^^^^

Na de installatie is het nodig de computer opnieuw op te starten.  Na de
herstart zal de pc automatisch inloggen met het nieuwe |hisparc| user
account en zal de detectorsoftware automatisch worden gestart.

.. figure:: images/screenshot-herstart.png
   :align: center
   :scale: 85

   De installer vraagt om het herstarten van de computer.  Het is mogelijk
   om dit later te doen, maar voordat de computer opnieuw is opgestart is
   de software niet volledig geïnstalleerd.


Na installatie
--------------

Nadat de computer opnieuw is opgestart zal Windows automatisch inloggen
onder het |hisparc| user account.  Windows zal dan een window
*StartHiSPARCSoftware* openen.  De volgende software zal dan
automatisch worden gestart:

* *MySQL server* voor tijdelijke data opslag
* *HiSPARC DAQ* software voor data acquisitie
* *HiSPARC Monitor* voor het versturen van data en het verzamelen van
  detectorstatistieken.  De monitor stelt ons in staat direct te weten
  wanneer een detector of detector pc niet meer goed functioneert.
* *HiSPARC Updater* voor het controleren van |hisparc| software updates.
  Dit stelt ons in staat om nieuwe detector software direct op alle
  detector pc's te installeren.

Het starten van *MySQL* zorgt voor een waarschuwing door de *Windows
Firewall*. Dit is geen enkel probleem, en we raden u aan de
waarschuwing in de toekomst te negeren (zie figuur).

.. figure:: images/screenshot-mysql-firewall.png
   :align: center
   :scale: 85

Nadat alle software is opgestart zijn verschillende vensters geopend.
Ieder venster, behalve *StartHiSPARCSoftware*, moeten blijven draaien.
Het is dus niet mogelijk vensters te sluiten.  De vensters mogen
natuurlijk wel geminimaliseerd worden.

<img>

.. note:: Voor een correcte werking van de detector is het van het
   grootste belang dat de vensters *HiSPARCDAQ, HiSPARC Monitor en HiSPARC
   Updater blijven draaien!*

.. note:: Vóór uiteindelijk gebruik is het nodig de |hisparc| data
   acquisitie software te configureren! Zie :doc:`configuratie`.


.. rubric:: Footnotes

.. [#ooti] Met dank aan een team van studenten van de Technische
   Universiteit Eindhoven.  Het OOTI team 2008 heeft in het kader van een
   8-weekse stageopdracht augustus / september 2009 onze installer,
   data-overdracht en data-opslag onderzocht en verbeterd.
.. [#python] Python is een zeer veelzijdige programmeertaal die de laatste
   jaren steeds populairder wordt.  Oorspronkelijk ontwikkeld aan het
   *Centrum voor wiskunde en informatica (CWI)* door *Guido van Rossum*
   (nu werkzaam bij *Google*) wordt de taal nu internationaal ontwikkeld
   en gebruikt.  Bekende gebruikers zijn ondermeer `Google
   <http://google.com>`_ en `Ubuntu <http://ubuntu.com>`_. Voor meer
   informatie over Python, zie de `Python website <http://python.org>`_ en
   `Python op Wikipedia
   <http://en.wikipedia.org/wiki/Python_(programming_language)>`_.
