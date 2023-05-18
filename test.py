# Funktion zum Extrahieren von ausgerichteten Segmenten aus dem DTW-Pfad
def get_aligned_segments(path, min_segment_length=10):
    aligned_segments = []  # Liste zum Speichern der ausgerichteten Segmente
    current_segment = []  # Liste zum Speichern des aktuellen Segments

    # Iteriere durch den Pfad, beginnend mit dem zweiten Element
    for i in range(1, len(path)):
        # Wenn das aktuelle Pfadelement in beiden Dimensionen zunimmt, gehört es zu einem ausgerichteten Segment
        if path[i][0] > path[i - 1][0] and path[i][1] > path[i - 1][1]:
            current_segment.append(path[i])
        else:
            # Wenn das aktuelle Pfadelement nicht Teil eines ausgerichteten Segments ist,
            # und die Länge des aktuellen Segments größer oder gleich der Mindestlänge ist,
            # füge das aktuelle Segment der Liste der ausgerichteten Segmente hinzu
            if len(current_segment) >= min_segment_length:
                aligned_segments.append(current_segment)
            # Setze das aktuelle Segment zurück
            current_segment = []

    # Überprüfe, ob das letzte Segment die Mindestlänge erfüllt
    if len(current_segment) >= min_segment_length:
        aligned_segments.append(current_segment)

    # Gibt die Liste der ausgerichteten Segmente zurück
    return [pair for sublist in aligned_segments for pair in sublist]


# Funktion zum Berechnen der Ähnlichkeit zwischen ausgerichteten Segmenten
def aligned_segement_similarity(X_angles, Y_angles, min_segment_length=5):
    similar_num = 0
    cos_vector = np.array([])  # Leeres Numpy-Array zum Speichern von Kosinus-Ähnlichkeiten
    path, cost = dtw_path(X_angles.T, Y_angles.T)  # Berechne den DTW-Pfad und die Kosten
    path = get_aligned_segments(path, min_segment_length)  # Extrahiere ausgerichtete Segmente aus dem Pfad

    path_dict = dict()
    # Erstelle ein Wörterbuch, um die ausgerichteten Segmente zu speichern
    for f1, f2 in path:
        path_dict.setdefault(f1, []).append(f2)

    # Berechne die Kosinus-Ähnlichkeit für jedes Paar von ausgerichteten Segmenten
    for i, j in path:
        a = cosine_similarity(X_angles[i].values.reshape(1, -1), Y_angles[j].values.reshape(1, -1))
        # Füge die berechnete Ähnlichkeit zum Kosinus-Vektor hinzu, wenn sie nicht Null ist
        if a != (np.array([0])):
            cos_vector = np.append(cos_vector, a)

    # Berechne die durchschnittliche Ähnlichkeit
    similar_num = round(np.mean(cos_vector), 3)

    # Gib die durchschnittliche Ähnlichkeit und den Pfad zurück
    return similar_num, path


# Berechne die Anzahl der möglichen Paarungen von Videos (ohne doppelte Paarungen und Selbstvergleiche)
n_tot = int((len(video_names) ** 2 - len(video_names)) / 2)
i = 0

# Erstelle einen leeren DataFrame, um die Ähnlichkeiten zwischen den Videos zu speichern
similarities1 = pd.DataFrame(index=video_names, columns=video_names)

# Doppelschleife, um jedes Paar von Videos zu vergleichen
for a, video_a in enumerate(video_names):
    for b, video_b in enumerate(video_names):
        # Wenn beide Videos in den Winkeldaten vorhanden sind
        if (video_a in angle_dataframes.keys()) & (video_b in angle_dataframes.keys()):
            # Wenn die Videos unterschiedlich sind
            if (a != b):
                # Nur wenn a < b, um doppelte Berechnungen zu vermeiden
                if (a < b):
                    angles_a = angle_dataframes[video_a]
                    angles_b = angle_dataframes[video_b]
                    # Berechne die Ähnlichkeit zwischen den Videos
                    similarity, _ = overall_similarity(angles_a, angles_b)
                    # Speichere die Ähnlichkeit im DataFrame
                    similarities1.loc[video_a, video_b] = similarity
            else:
                # Wenn die Videos identisch sind, setze die Ähnlichkeit auf 1
                similarity = 1
                similarities1.loc[video_a, video_b] = similarity

            # Gib den Fortschritt der Berechnung aus
            print("{}/{} \t {} x {} => {}".format(i, n_tot, video_a, video_b, similarity))
            i += 1

# Schleife, um die Ähnlichkeiten in der unteren Dreiecksmatrix des DataFrames
# basierend auf den Ähnlichkeiten in der oberen Dreiecksmatrix zu füllen
for a, video_a in enumerate(video_names):
    for b, video_b in enumerate(video_names):
        # Wenn die Videos unterschiedlich sind und beide Videos in den Winkeldaten vorhanden sind
        if (a != b) & (video_a in angle_dataframes.keys()) & (video_b in angle_dataframes.keys()):
            # Nur wenn a > b, um die untere Dreiecksmatrix zu füllen
            if (a > b):
                # Setze die Ähnlichkeit im unteren Dreieck auf den Wert aus dem oberen Dreieck
                similarities1.loc[video_a, video_b] = similarities1.loc[video_b, video_a]

