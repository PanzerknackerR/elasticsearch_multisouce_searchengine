# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import random, uuid, time, json, sys
import time
# Connect to the elastic cluster
es=Elasticsearch([{'host':'elasticsearch','port':9200}])

e1={

}

def get_random_words(words_list, total=1):
    ran_words = []

    # enumerate over specified number of words
    while len(ran_words) < total:
        ran_words += [words_list[random.randint(0, len(words_list)-1)]]

    # return a string by joining the list of words
    return ' '.join(ran_words)

def create_event_json(size):
    # list to store JSON records
    records = []
    # random words to inject into records
    words = ["Hallo", "Ich", "bin", "ein", "kleiner", "Blindtext", "Und", "zwar", "schon", 
    "so", "lange", "ich", "denken", "kann", "Es", "war", "nicht", "leicht", "zu", "verstehen", 
    "was", "es", "bedeutet,", "ein", "blinder", "Text", "zu", "sein:", "Man", "ergibt", "keinen", 
    "Sinn", "Wirklich", "keinen", "Sinn", "Man", "wird", "zusammenhangslos", "eingeschoben", "und", 
    "rumgedreht", "–", "und", "oftmals", "gar", "nicht", "erst", "gelesen", "Aber", "bin", "ich", "allein", 
    "deshalb", "ein", "schlechterer", "Text", "als", "andere", "Na", "gut,", "ich", "werde", "nie", "in", "den", 
    "Bestsellerlisten", "stehen", "Aber", "andere", "Texte", "schaffen", "das", "auch", "nicht", "Und", "darum", 
    "stört", "es", "mich", "nicht", "besonders", "blind", "zu", "sein", "Und", "sollten", "Sie", "diese", "Zeilen", "noch", 
    "immer", "lesen,", "so", "habe", "ich", "als", "kleiner", "Blindtext", "etwas", "geschafft,", "wovon", "all", "die", "richtigen", 
    "und", "wichtigen", "Texte", "meist", "nur", "träumen","dieser", "text", "hat", "eigentlich", "gar", "keinen", "wirklichen", "inhalt", 
    "aber", "er", "hat", "auch", "keine", "relevanz,", "und", "deswegen", "ist", "das", "egal", "er", "dient", "lediglich", "als", "platzhalter", 
    "um", "mal", "zu", "zeigen,", "wie", "diese", "stelle", "der", "seite", "aussieht,", "wenn", "ein", "paar", "zeilen", "vorhanden", "sind", "ob", 
    "sich", "der", "text", "dabei", "gut", "fühlt,", "weiß", "ich", "nicht", "ich", "schätze,", "eher", "nicht,", "denn", "wer", "fühlt", "sich", "schon", 
    "gut", "als", "platzhalter", "aber", "irgendwer", "muss", "diesen", "job", "ja", "machen", "und", "deshalb", "kann", "ich", "es", "nicht", "ändern", "",
    "ich", "könnte", "dem", "text", "höchstens", "ein", "bisschen", "gut", "zureden,", "dass", "er", "auch", "als", "platzhalter", "eine", "wichtige", "rolle", 
    "spielt", "und", "durchaus", "gebraucht", "wird", "könnte", "mir", "vorstellen,", "dass", "ihm", "das", "gut", "tut", "denn", "das", "gefühl", "gebraucht", "zu",
    "werden", "tut", "doch", "jedem", "gut,", "oder", "klar,", "er", "ist", "austauschbar", "das", "darf", "ich", "ihm", "natürlich", "nicht", "verraten", "denn", "austauschbar", 
    "zu", "sein,", "dass", "ist", "schrecklich", "austauschbar", "zu", "sein", "bedeutet", "ja", "eigentlich,", "dass", "nicht", "man", "selbst,", "sondern", "einfach", "irgendjemand", 
    "oder", "irgendwas", "an", "der", "stelle", "gebraucht", "wird", "somit", "würde", "mein", "erstes", "argument,", "man", "braucht", "dich,", "nicht", "mehr", "ziehen,", "und", "das", 
    "zuvor", "erzeugte", "gute", "gefühl", "des", "textes", "wäre", "zunichte", "gemacht", "das", "will", "ich", "nicht", "also", "bitte", "nix", "verraten,", "ja", "aber", "vielleicht", 
    "merkt", "er", "es", "ja", "nicht", "das", "wäre", "gut,", "denn", "wer", "hat", "schon", "lust", "einen", "deprimierten", "blindtext", "auf", "seiner", "seite", "zu", "platzieren", 
    "was", "würde", "denn", "das", "für", "einen", "eindruck", "machen", "das", "will", "ja", "keiner", "lesen", "somit", "wäre", "er", "dann", "ein", "für", "alle", "mal", 
    "tatsächlich", "völlig", "nutzlos", "das", "wäre", "sein", "todesurteil", "soweit", "wollen", "wir", "es", "doch", "nicht", "kommen", "lassen,", "oder", "es", "sei", "denn", 
    "und", "das", "ist", "möglich,", "er", "würde", "wiedergeboren", "und", "käme", "als,", "naja,", "sagen", "wir", "als", "witz,", "und", "ein", "textleben", "später", "vielleicht", 
    "als", "bildzeitungsartikel", "auf", "die", "textwelt", "irgendwann", "wäre", "er", "vielleicht", "sogar", "ein", "text", "im", "lexikon", "dann", "hätten", "wir", "ihn", "ja", "sogar", 
    "weitergebracht", "in", "seiner", "entwicklung", "klingt", "gar", "nicht", "schlecht,", "oder", "trotzdem", "bin", "ich", "der", "meinung,", "man", "sollte", "ihn", "nicht", "bewusst", 
    "dort", "hin", "treiben", "er", "hat", "ein", "recht", "darauf,", "sich", "selbst", "zu", "entwickeln", "und", "zwar", "in", "genau", "dem", "tempo,", "das", "ihm", "gefällt", "und", 
    "bis", "es", "soweit", "ist,", "nehme", "ich", "ihn", "eben", "an,", "wie", "er", "ist", "als", "einfachen", "blindtext", "ohne", "wirklichen", "inhalt"]

    # iterate over the number of records being created
    for rec_id in range(size):
        # input a value for each table column
        id_col=uuid.uuid4().hex
        string_col = get_random_words( words, random.randint(1, len(words)) )
        bool_col = [True, False][random.randint(0, 1)]
        int_col = random.randint(1, 6000)
        float_col = random.uniform(1.5, 99.9)
        doc= {
            "id": id_col,
            "str_col": string_col,
            "int_col": int_col,
            "bool_col": bool_col,
            "float_col" : float_col,
        }
        res = es.index(index='event_data',id=id_col,body=doc)
        print(res)
        
        
def run():
    x=0
    while x<10:
        print(x)
        create_event_json(10)
        time.sleep(x)
        x+=0.01
        
run()