import csv
import xml.etree.ElementTree as ET

crossings_list = []
crossing_dicts = {}
double_crossings = []
lane_list = []
before_row = '9999'


# Doppelte Kreuzungen
def double_crossing(before_row, id):
    if before_row.startswith(id):
        return before_row, id


# Dateien für Detektoren erstellen
def detector_file(crossings):
    for c in crossings.items():
        if 'Detector' in c[1] and c[1].get('Detector') is not None and len(c[1].get('Detector')) > 0:
            detector_f = open('Detector_Mapping_' + c[0] + '.txt', "w")
            i = 0
            for d in c[1].get('Detector'):
                detector_f.write(d + ';' + c[0] + '_' + str(i) + "\n")
                i = i + 1
            detector_f.close()


# Datei erstellen für Double Crossings Mapping
def double_crossing_file(double_crossings):
    double_f = open('DoubleCrossings.txt', "w")
    for c in double_crossings:
        double_f.write(c[0] + ';' + c[1] + "\n")
    double_f.close()


# Datei erstellen für TLS Mapping
def tls_file(crossings):
    tls_f = open('TLSMapping.txt', "w")
    for c in crossings.items():
        if 'ID' in c[1] and c[1].get('ID') is not None:
            if c[1].get('ID').endswith('_2'):
                tls_f.write(c[0] + ";" + c[1].get('ID')[0: 7] + "_1 \n")
            tls_f.write(str(c[0]) + ";" + str(c[1].get('ID')) + "\n")
    tls_f.close()


# Sg Mapping Datei erstellen
def sg_file(crossings):
    for c in crossings.items():
        if 'LinkIndex' in c[1] and c[1].get('LinkIndex') is not None and len(c[1].get('LinkIndex')) > 0:
            sg_f = open('Sg_Mapping_' + c[0] + '.txt', "w")
            for index in c[1].get('LinkIndex'):
                sg_f.write(index + "\n")
            if c[1].get('check_Index')[0]:
                pass
            else:
                # sg_f.write('There are missing indices: The last index should be ' + str(c[1].get('check_Index')[1]))
                print('There are missing indices: The last index should be ' + str(c[1].get('check_Index')[1]))
            sg_f.close()


# Pfadangabe anpassen
file = input('The path to the InTAS.csv file: ')
with open(file) as csvdatei:
# with open('/Users/elenaschramme/Desktop/HiWi/pythonProject/InTAS_RealFuture/InTAS.csv') as csvdatei:
    csv_reader_object = csv.reader(csvdatei, delimiter=';')
    for row in csv_reader_object:

        # Dictionary für einzelne Kreuzung
        crossing = {}
        detector = len(row)
        sumo_lane = len(row)
        distance = len(row)
        link_index = len(row)
        crossing_dicts[row[0]] = crossing

        if row[1].startswith('IN'):
            crossing['ID'] = row[1].strip()
        else:
            # Kreuzungen für die nur ein Kommentar vorliegt
            crossing['Comment'] = row[1].strip()
            continue

        # Dictionary für Kreuzung mit Merkmalen
        if 'Detector' in row:
            detector = row.index('Detector')
        if 'Sumo_Lane' in row:
            sumo_lane = row.index('Sumo_Lane')
        if 'Distance' in row:
            distance = row.index('Distance')
        if 'LinkIndex' in row:
            link_index = row.index('LinkIndex')
            crossing['check_Index'] = [False, row[link_index + 1]]

        crossing['Detector'] = [row[i].strip() for i in range(detector + 1, sumo_lane)]
        crossing['Sumo_Lane'] = [row[i].strip() for i in range(sumo_lane + 1, distance)]
        crossing['Distance'] = [row[i].strip() for i in range(distance + 1, link_index)]
        crossing['LinkIndex'] = [row[i].strip() for i in range(link_index + 2, len(row))]
        if len(crossing.get('LinkIndex')) > 0:
            crossing.update(
                {'check_Index': [int(row[link_index + 1]) == len(crossing.get('LinkIndex')) - 1, row[link_index + 1]]})

        # Doppelte Kreuzungen finden
        double_c = double_crossing(before_row, str(row[0]))
        if double_c is not None:
            double_crossings.append(double_c)
        before_row = str(row[0])

        # Prüfen, ob Anzahl Detectoren mit Spuren und Distance Liste übereinstimmt
        if len(crossing.get('Detector')) != len(crossing.get('Sumo_Lane')):
            print('Die Anzahl der Detectoren stimmt nicht mit der Anzahl der Spuren überein!')
        if len(crossing.get('Sumo_Lane')) != len(crossing.get('Distance')):
            print('Die Anzahl der Spuren stimmt nicht mit der Anzahl der Distancen überein!')

for c in crossing_dicts.items():
    print(c)
# for c in double_crossings:
#    print(c)

# Dateien erstellen
detector_file(crossing_dicts)
tls_file(crossing_dicts)
sg_file(crossing_dicts)
double_crossing_file(double_crossings)


# Längen Datei erstellenx
def length_file(crossings, lanes):
    length_f = open('Length_Mapping.add.xml', "w")

    # Kopf der Datei schreiben
    length_f.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n" +
                   '<!-- generated on 2022-07-27 16:42:42 by Eclipse SUMO netedit Version 1.14.1' + "\n" +
                   '<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                   'xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/netconvertConfiguration.xsd">' + "\n" +
                   '<input>' + "\n" +
                   '<sumo-net-file value="/home/pritesh/Intas/InTAS_RealFuture/scenario/InTAS.net.xml"/>' + "\n" +
                   '</input>' + "\n" + "\n" +
                   '<output>' + "\n" +
                   '<output-file value="/home/pritesh/Intas/InTAS_RealFuture/scenario/InTAS.net.xml"/>' + "\n" +
                   '</output>' + "\n" + "\n" +
                   '<processing>' + "\n" +
                   '<geometry.min-radius.fix.railways value="false"/>' + "\n" +
                   '<geometry.max-grade.fix value="false"/>' + "\n"
                                                               '<offset.disable-normalization value="true"/>' + "\n" +
                   '<lefthand value="false"/>' + "\n" +
                   '</processing>' + "\n" + "\n" +

                   '<junctions>' + "\n" +
                   '<no-turnarounds value="true"/>' + "\n" +
                   '<junctions.corner-detail value="5"/>' + "\n" +
                   '<junctions.limit-turn-speed value="5.5"/>' + "\n" +
                   '<rectangular-lane-cut value="false"/>' + "\n" +
                   '</junctions>' + "\n" + "\n" +

                   '<pedestrian>' + "\n" +
                   '<walkingareas value="false"/>' + "\n" +
                   '</pedestrian>' + "\n" + "\n" +

                   '<netedit>' + "\n" +
                   '<additional-files value="/home/pritesh/Intas/InTAS_RealFuture/scenario/InTAS_E1.add.xml"/>' + "\n" +
                   '</netedit>' + "\n" + "\n" +

                   '<report>' + "\n" +
                   '<aggregate-warnings value="5"/>' + "\n" +
                   '</report>' + "\n" + "\n" +

                   '</configuration>' + "\n" + '-->' + "\n")
    length_f.write('<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                   'xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">' + "\n")

    # Detektor Tags erstellen
    for c in crossings.items():
        if 'Sumo_Lane' in c[1] and c[1].get('Sumo_Lane') is not None and len(c[1].get('Sumo_Lane')) > 0:
            i = 1

            # ein Tag pro Lane erstellen
            for lane in c[1].get('Sumo_Lane'):
                dis = 0.0

                # Lane in InTAS.net Datei suchen und Länge der LAne herausfinden
                for inTAS in lanes:
                    if inTAS[0] == lane:
                        dis = float(inTAS[1])
                        continue

                # Abstand zwischen Haltelinie und Detektor
                if len(c[1].get('Distance')) <= 1:
                    dist = 0.0
                else:
                    dist = float(c[1].get('Distance')[i - 1])

                # Lane Tag schreiben
                length_f.write(
                    '<e1Detector id="' + c[0] + '_' + str(
                        i) + '" lane="' + lane + '" pos="' + '{0:.2f}'.format(dis - dist) + '" freq="900.00" name="' +
                    c[
                        0] + '" file="InTAS_Detectors_Output.xml" friendlyPos="1"/>' + "\n")
                i = i + 1

    length_f.write('</additional>' + "\n")
    length_f.close()


# Liste mit allen Lanes aus InTAS.net erstellen
xml_file = input('The path to the InTAS.net.xml file: ')
# inTASxml = ET.parse('/Users/elenaschramme/Desktop/HiWi/pythonProject/InTAS_RealFuture/scenario/InTAS.net.xml')
inTASxml = ET.parse(xml_file)
length = inTASxml.findall('edge/lane')
for item in length:
    lane_list.append((item.get('id'), item.get('length')))
# Datei erstellen
length_file(crossing_dicts, lane_list)
