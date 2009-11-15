.. include:: subst.inc

Installatie van de |hisparc| electronica
========================================

De HiSPARC II elektronica kan in twee configuraties toegepast worden:

* een enkele ‘Master’ unit voor het uitlezen van twee skiboxen.
* Een Master- in combinatie met een ‘Slave-unit’, geschikt voor een
  detectiestation met vier scintillatieplaten. 

Opstelling met twee skiboxen
----------------------------

De HiSPARC II Master elektronica (:ref:`Vooraanzicht master
<master-voorkant>`) integreert snelle signaalverwerking, conversie van
twee analoge signalen afkomstig van de fotoversterkerbuizen naar digitaal
formaat, en een precisie GPS, in één behuizing.  De Master verstuurt zijn
data via een USB verbinding aan de achterzijde (aansluiting aan de linker
kant in (:ref:`Achteraanzicht master <master-achterkant>`) naar de data
acquisitie (DAQ) pc.  De rechter USB aansluiting (onder de connector voor
de GPS antenne) is voor directe communicatie tussen GPS en GPS
monitorprogramma.  Deze verbinding is uitsluitend voor het verifiëren
en/of aanpassen van de instellingen van de GPS.  In tegenstelling tot de
oudere elektronica, wordt de HiSPARC II unit nu volledig bestuurd vanaf de
DAQ computer. Op deze pc draait een programma dat geschreven is in
|labview|.  Er is een uitgebreide handleiding (Data Acquisitie Gebruikers
Handleiding) beschikbaar die de gebruiker inzicht geeft in zowel het
instellen van de GPS als de diverse opties die het HiSPARC II
besturingsprogramma biedt.  Het |labview| programma is verantwoordelijk
voor het verzamelen en tevens het doorsturen van de meetgegevens naar een
locaal buffer op de harde schijf van de data acquisitie pc.  De gegevens
in deze locale buffer worden regelmatig door een tweede programma -- dat
onafhankelijk van het |labview| programma draait -- naar de centrale
(MySQL) database bij het Nikhef in Amsterdam gestuurd.  In de nabije
toekomst wordt er ook een mogelijkheid gecreëerd om de gegevens van het
station voor analyse op te slaan in een locale database.  De analyse
software kan de gegevens uit zowel de centrale als de locale database
verwerken.

.. _master-voorkant:
.. figure:: images/kastje-voorkant.jpg
   :align: center
   :width: 600

   De voorkant van de HiSPARC II Master; van links naar rechts: groene LED
   voor de voedingsspanning, de gele LED geeft aan of er signalen
   binnenkomen, signaal- en voedingsaansluiting voor fotobuis-1. Midden:
   de inlaat voor de luchtkoeling. Rechts in omgekeerde volgorde:
   voedings- en signaalaansluiting fotobuis-2 en gele signaal LED.

.. _master-achterkant:
.. figure:: images/master-achterkant.jpg
   :align: center
   :width: 600

   De achterzijde van de HiSPARC II Master; van links naar rechts: USB
   aansluiting voor het versturen van de meetgegevens naar de pc, TTL
   aansluiting voor een externe trigger (alleen voor speciale doeleinden),
   twee UTP verbindingen (niet van toepassing), uitgang luchtkoeling,
   aansluiting voedingsadapter (12 Volt DC, 1.5 A), GPS antenne
   aansluiting (rechtsboven) en USB verbinding voor het aanpassen van de
   GPS instellingen.

Opstelling met vier skiboxen
----------------------------

Om vier scintillatie detectoren uit te kunnen lezen, moet een tweede
HiSPARC II unit aangesloten worden. Echter, deze unit -- de Slave --
(:ref:`Vooraanzicht slave <slave-voorkant>`) bezit geen GPS maar is verder
identiek aan de Master.  Aan de achterzijde is dan ook geen aansluiting
voor een GPS-antenne aanwezig (:ref:`Achteraanzicht slave
<slave-achterkant>`).

.. _slave-voorkant:
.. figure:: images/kastje-voorkant.jpg
   :align: center
   :width: 600

   De voorkant van de HiSPARC II Master en Slave zijn identiek.

.. _slave-achterkant:
.. figure:: images/slave-achterkant.jpg
   :align: center
   :width: 600

   Data van de HiSPARC II Slave wordt uitgelezen via de linker USB
   verbinding.  De Slave heeft geen aansluiting voor een GPS antenne kabel
   (rechtsboven); de rechter USB aansluiting is zonder functie.

De Slave wordt via twee korte UTP kabels (kruislings, de lengte mag niet
veranderd worden!) verbonden met de Master unit (:ref:`Master-Slave
combinatie <master-slave-combi>`).  Master en Slave versturen hun data dus
over aparte USB verbindingen (voor beide units is dit de linker connector
aan de achterzijde).

.. _master-slave-combi:
.. figure:: images/master-slave-achterkant.jpg
   :align: center
   :width: 600

   Een snelle databus verzorgt de communicatie tussen HiSPARC II Master en
   Slave; de verbinding bestaat uit twee kabels die ‘LVDS data in’ en
   ‘LVDS data out’ (kruislings) met elkaar verbinden.

.. _nagios-doc:
Monitor en controle
-------------------

De nieuwe besturingssoftware biedt bovendien de optie om de status van de
detectoren en pc’s op afstand via internet te controleren (:ref:`Nagios
<nagios>`).

.. _nagios:
.. figure:: images/screenshot-nagios.jpg
   :align: center
   :width: 600

   Het Nagios menu aan de linkerzijde biedt verschillende monitor opties.

Ga naar:

http://vpn.hisparc.nl/nagios/

en selecteer vervolgens een van de opties in de linker menubalk.  De
clustercoördinatoren hebben bovendien de mogelijkheid om de instellingen
van de detector via een ‘virtual private network’ (VPN, :ref:`VPN diagram
<network-diagram>`) op afstand te wijzigen.  De toegang tot de pc’s biedt
de mogelijkheid om snel en efficiënt kritische instellingen te veranderen
en software updates door te voeren.

.. _network-diagram:
.. figure:: images/network-diagram.png
   :align: center
   :width: 600

   De software biedt monitor en controle mogelijkheden via een VPN
   verbinding.  Data van de detector wordt over een gescheiden verbinding
   verzonden.
