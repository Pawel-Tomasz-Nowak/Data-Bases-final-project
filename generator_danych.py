import pandas as pd
import pathlib as path
import numpy as np
import datetime as dt
import calendar
from string import digits

# ---------------------------------------------------------------------------------
# (1) Wczytywanie potrzebnych bibliotek.

digits:list[str] = list(digits)
today: dt.date = dt.date.today()

# Ustal, ile minimalnie, a ile maksymalnie może brać udział klientów w jednej wycieczce.
n_client_range: tuple[int] = (25, 70)

# Ustal, ile minimalnie,  a ile maksymalnie będzie wycieczek.
n_trip_range:tuple[int] = (35, 75)

# Policz, ile klientów należy wygenerować w zależności od powyższych paraemtrów.
n_clients:int = (n_trip_range[1] + n_trip_range[0])//2 * n_client_range[1]

n_female_clients: int = np.random.randint(1, n_clients+1)
n_male_clients:int = n_clients - n_female_clients

# Na ile osób przypada jeden kierownca i przewodnik.
driver_ratio: int = 50
guide_ratio: int = 25



# ---------------------------------------------------------------------------------
# (2) Odczytywanie popularnych imion i nazwisk żeńskich i męskich.

# Znajdź katalog z imionami i nazwiskami.
name_dir_path: path.Path = path.Path().cwd()/"Imiona i nazwiska"

# Znajdź  katalog, gdzie zapisujemy wszystkie tabele .csv.
csv_tables_dir_path: path.Path = path.Path().cwd()/"Tabele_csv"


def read_names(first_names_file:str, last_names_file:str, dir_path:path.Path) -> tuple[pd.Series, pd.Series]:
    """Funkcja odczytuje pliki zawierające najpopularniejsze polskie imiona i nazwiska. Wczytuje je do szeregu danych typu pandas"""
    # Odczytaj imiona oraz nazwiska.
    first_names: pd.DataFrame = pd.read_excel(dir_path/first_names_file  ,"Arkusz1",
                                                usecols = [0,2]
                                                )
    last_names: pd.DataFrame = pd.read_excel(dir_path/last_names_file, "Arkusz1",
                                                nrows = 5_000) # Wierszy w arkuszu jest bardzo dużo (ponad 380 000). 
                                                                # Odczytaj tylko pewną część wierszy.
                                                                

    # Bierzemy pod uwagę jedynie najpopularniejsze imiona i nazwiska.
    first_names = first_names.loc[first_names["LICZBA_WYSTĄPIEŃ"] > 500, "IMIĘ_PIERWSZE"]
    last_names = last_names.loc[last_names["Liczba"] > 500, "Nazwisko aktualne"] 

    # Skróc nazwy kolumn.
    first_names.columns = ['imię']
    last_names.columns = ['nazwisko']

    return first_names, last_names

# Wczytaj męskie imiona i nazwiska.
male_first_names, male_last_names = read_names("imiona_meskie.xlsx", "nazwiska_meskie.xlsx", name_dir_path)

# Wczytaj żęńskie imiona i nazwiska.
female_first_names, female_last_names = read_names("imiona_zenskie.xlsx", "nazwiska_zenskie.xlsx", name_dir_path)



# ---------------------------------------------------------------------------------
# (3) Pomocnicze funkcje generujące.

def generate_birthday() -> dt.datetime:
    # Wygeneruj wiek z rozkładu normalnego. Pamiętaj, że osoba musi być przynajmniej pełnoletnia i maksymalnie 100 letnia.
    birth_year: int =  today.year - np.random.randint(18, 100,)

    birth_month:int = np.random.randint(1, 13) # Wygeneruj miesiąc urodzenia.

    birth_day = calendar.monthrange(birth_year, birth_month)[1] # Znajdź dzień urodzenia (zgodny z liczbą dni w miesiącu)

    birthday = dt.date(birth_year, birth_month, birth_day) # Złóż wszystkie składowe urodzin w jedną date.

    return birthday



def generate_email(first_name:str, last_name:str, domains:list[str]) -> str:
    email:str = first_name.lower() + last_name.lower() + "".join(np.random.choice(digits, 3)) +"@"+ np.random.choice(domains)

    return email



def generate_phone_number() -> str:
    # Wygeneruj losowy numer telefonu nie zaczynający się od 0.
    phone_number:np.array = np.random.choice(digits, 9)

    # Jeżeli wylosowaliśmy zero, podmień cyfrę.
    if phone_number[0] == "0":
        phone_number[0] = np.random.choice(digits[1:])

    phone_number: str = "".join(phone_number)

    return phone_number


def insert_id_col(people_data:pd.DataFrame, col_name:str) -> pd.DataFrame:
    people_data.insert(loc = 0,column = col_name,
                       value = range(1, people_data.shape[0]+1))
    
    return people_data


def merge_females_and_males(female_data:pd.DataFrame, male_data:pd.DataFrame, id_col_name:str) ->pd.DataFrame:
    people_data_df : pd.DataFrame = pd.concat(objs = [female_data, male_data], axis = 0).reset_index(drop = True)

    people_data_df : pd.DataFrame = insert_id_col(people_data_df, id_col_name)

    return people_data_df


def chance_of_being_student(age:float):
    """
    Oblicza szansę na bycie studentem w zależności od wieku.

    Parametry:
        age (int): Wiek osoby.

    Zwraca:
        float: Szansa na bycie studentem (od 0.0 do 1.0).
    """
    if age < 20 or age > 35:
        return 0.0
    else:
        return 1 - (age - 20) / 15  # Liniowe zmniejszanie szansy



# ---------------------------------------------------------------------------------
# (4) Tworzenie danych osobowych klientów.

def generate_client_personal_data(first_names:pd.Series, last_names:pd.Series, n:int) -> pd.DataFrame:
    """Funkcja generuje dane osobiste klientów. Tworzone są wiersze imię, nazwisko, data urodzenia, numer telefonu i adres e-mail, status studenta.

    """
    # Przygotuj wyjściową ramkę danych.
    clients_df: pd.DataFrame = pd.DataFrame(data = {"imie":pd.Series(dtype = pd.StringDtype()),
                                                    "nazwisko": pd.Series(dtype = pd.StringDtype()), 
                                                    "data_urodzenia":pd.Series(dtype = "datetime64[ns]"),
                                                    "znizka": pd.Series(dtype = pd.Float32Dtype()),
                                                    "numer_telefonu":pd.Series(dtype = pd.StringDtype()), 
                                                    "adres_email": pd.Series(dtype = pd.StringDtype()),
                                                    "status_studenta":pd.Series(dtype = pd.Int8Dtype())}                                          
    )

    clients_df["data_urodzenia"] = clients_df['data_urodzenia'].dt.date

    # Lista domen emailowych.
    email_domains:list[str] = ['gmail.com', "wp.pl", "onet.pl"]


    for id in range(n):
        first_name_idx:int = np.random.randint(0, first_names.shape[0])
        last_name_idx:int = np.random.randint(0, last_names.shape[0])

        first_name:str = first_names[first_name_idx].capitalize() # Wylosuj imię
        last_name:str = last_names[last_name_idx].capitalize()  # Wylosuj nazwisko.

        
        # Wygeneruj losowy numer telefonu nie zaczynający się od 0.
        phone_number:str = generate_phone_number()

        # Stwórz email dla tego klienta
        email:str = generate_email(first_name, last_name, email_domains)
        
        
        # Zmyśl datę urodzenia dla tego klienta. Wszyscy muszą być pełnoletni i zakładamy, że żyją maksymalnie 100 lat.
        birthday = generate_birthday()
        
        age: int = (today-birthday).days/365

        # Czy jest studentem
        is_student: int = np.random.binomial(1, chance_of_being_student(age))
     
        # Ustal zniżkę w zależności od wieku.
        if is_student:
            discount = 0.49
        else:
            if age >= 70:
                discount = 0.5
            elif age >= 60:
                discount = 0.65
            elif age >= 50:
                discount = 0.75
            elif age >= 40:
                discount = 0.85
            elif age >= 30:
                discount = 0.9
            else:
                discount = 1
    

        clients_df.loc[id, :] = [first_name, last_name, birthday, discount,phone_number, email, is_student]

    return clients_df

        

female_clients_df : pd.DataFrame = generate_client_personal_data(female_first_names, female_last_names, n_female_clients)
male_clients_df : pd.DataFrame = generate_client_personal_data(male_first_names, male_last_names, n_male_clients)

clients_df = merge_females_and_males(female_clients_df, male_clients_df, "id_klienta")


clients_df.to_csv(path_or_buf = csv_tables_dir_path/"Klienci_db.csv",
                    sep = ";", index = False)



# ---------------------------------------------------------------------------------
# (5) Generowanie bliskich osób.

def generate_one_relative(first_names:pd.Series, last_names:pd.Series, id:int):
    """Funkcja generuje jedną osobę bliską dla ustalonego klienta"""
    first_name:str = np.random.choice(first_names)
    last_name:str = np.random.choice(last_names)

    phone_number: str = generate_phone_number()
    email = generate_email(first_name, last_name, ["gmail.com", "wp.pl", "onet.pl"])

    return (id, first_name, last_name, phone_number, email)



def generate_relatives():
    klienci:pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Klienci_db.csv",
                          sep = ";",
                          encoding = "utf-8", usecols=["id_klienta"])
    
    klienci_id:pd.Series = klienci["id_klienta"]
    
    relationship_df : pd.DataFrame = pd.DataFrame(data = {"id_klienta":pd.Series(dtype = pd.Int16Dtype()),
                                                          "id_osoby_bliskiej":pd.Series(dtype = pd.Int16Dtype())})
    
    relatives_df: pd.DataFrame = pd.DataFrame(data = {"id_osoby_bliskiej":pd.Series(dtype = pd.Int16Dtype()),
                                                        "imie":pd.Series(dtype = pd.StringDtype()),
                                                        "nazwisko": pd.Series(dtype = pd.StringDtype()), 
                                                        "numer_telefonu":pd.Series(dtype = pd.StringDtype()), 
                                                        "adres_email": pd.Series(dtype = pd.StringDtype())}) # id klienta, z którym dana osoba ma związek.


    how_many_relatives:pd.DataFrame = pd.DataFrame(data = {"id_klienta":klienci_id,
                                                        "n_relatives":np.zeros(klienci_id.shape[0])}
                                                        )


    id: int = 1 # Identyfikator osoby bliskiej.
    i: int  = 0 # Identyfikator wiersza w ramce relationship_df.


    for id_klienta in klienci_id:
        n_relatives = np.random.randint(1, 4) # Wygeneruj, ilu bliskich może mieć dana osoba.

        for _ in range(n_relatives):
            gender_draw = np.random.uniform(0, 1)

            if gender_draw > 0.5: # Jeżeli tak jest, losujemy kobietę.
                relative = generate_one_relative(female_first_names, female_last_names, id)
            else: # Jeżeli nie, losujemy mężczyzne
                relative = generate_one_relative(male_first_names, male_last_names, id)

            # Połącz relacją bliskości 'relative' oraz 'id_klienta'
            relatives_df.loc[id, :] = relative

            relationship_df.loc[i, :] = (id_klienta, id)
            
            how_many_relatives.loc[id_klienta-1, "n_relatives"] += 1

            i += 1

            # Teraz wygeneruj kilku innych klientów, z którymi ta osoba bliska będzie w relacji
        
            # Znajdź potencjalnych klientów, z którym może się zaprzyjaźnic ustalona osoba bliska.
            potential_players_id = (how_many_relatives["id_klienta"]!=id_klienta) & (how_many_relatives["n_relatives"] < 4)
            potential_players = how_many_relatives.loc[potential_players_id, :]
            
            # Ustal, z iloma osoba dana osoba będzie w relacji bliskości.
            n_clients:int = min(np.random.randint(0, 3), potential_players_id.shape[0])

            for inne_id_klienta in potential_players['id_klienta'].sample(n_clients):
                relationship_df.loc[i, :] = (inne_id_klienta, id)
                
                i += 1

            id +=1
    
    # Zapisz ramkę z krewnymi do csv.
    relatives_df.to_csv(csv_tables_dir_path/"Osoby_bliskie_db.csv",
                      sep = ';',
                      encoding = "utf-8",
                      index = False)
    
    # Zapisz ramkę z relacjiami do csv.
    relationship_df.to_csv(csv_tables_dir_path/"Relacje_bliskości_db.csv",
                      sep = ';',
                      encoding = "utf-8",
                      index = False)
    

    
generate_relatives()



# ---------------------------------------------------------------------------------
# (6) Tworzenie tabeli z wynagrodzeniami.

def create_salary_table():

    salary_df:  pd.DataFrame = pd.DataFrame(data = {"stanowisko":pd.Series(dtype =pd.StringDtype()),
                                                    "wynagrodzenie":pd.Series(dtype = pd.Float64Dtype())
                                                    })
    
    salary_df.loc[0, :] = ["przewodnik", 1200]
    salary_df.loc[1, :] = ["kierowca",800]


    salary_df.to_csv(csv_tables_dir_path/"Wynagrodzenie_db.csv",
                      sep = ';',
                      encoding = "utf-8",
                      index = False)
    

create_salary_table()



# ---------------------------------------------------------------------------------
# (7) Generowanie tabeli planowanych wycieczek, tabeli transakcji.

def generate_startday() -> dt.datetime:
    year: int =  np.random.randint(today.year -2, today.year) # Wylosuj rok odbycia się wyjazdu.

    month:int = np.random.randint(6, 10) # Wygeneruj miesiąc wyjazdu.

    day = calendar.monthrange(year, month)[1] # Znajdź dzień urodzenia (zgodny z liczbą dni w miesiącu)


    return dt.date(year, month, day)



def generate_trip_tables():
    """
    Generuje tabele związane z wycieczkami z plików CSV i przetwarza dane.

    Funkcja wykonuje następujące kroki:
    1. Wczytuje plik "Miasta_db.csv", aby uzyskać listę możliwych destynacji.
    2. Konwertuje kolumnę "dlugosc_wycieczki" w DataFrame miast na typ timedelta.
    3. Wczytuje plik "Klienci_db.csv", aby uzyskać listę klientów.
    4. Tworzy DataFrame opisujący planowane wyjazdy z kolumnami dla ID wycieczki, daty rozpoczęcia, informacji czy wycieczka się odbyła oraz ID miasta.
    5. Tworzy DataFrame do zapisywania zrealizowanych transakcji z kolumnami dla ID transakcji, kwoty, daty i innych istotnych informacji.
    Zwraca:
        None
    """
    # Wczytaj tabelę zawierającą listę możliwych destynacji.
    cities_df: pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Miasta_db.csv",
                                          sep = ";", 
                                          encoding = "utf-8",
                                          
                                          )
    
    
    # Przekształć kolumnę "dlugosc_wycieczki" na typ timedelta.
    cities_df["dlugosc_wycieczki"] = pd.to_timedelta(cities_df["dlugosc_wycieczki"])
    
    # Wczytaj tabele z klientami.
    clients_df: pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Klienci_db.csv",
                                           sep = ";",
                                           encoding = "utf-8"
                                           , parse_dates = ["data_urodzenia"]
                                           )
   

    # Stwórz tabele opisującą planowane wyjazdy.
    planned_trips_df: pd.DataFrame = pd.DataFrame(data = {"id_wycieczki":pd.Series(dtype = pd.Int32Dtype()),
                                                       "data_rozpoczecia":pd.Series(dtype = "datetime64[ns]"),
                                                       "odbyla_sie":pd.Series(dtype = pd.BooleanDtype())
                                                       ,"id_miasta":pd.Series(dtype = pd.Int32Dtype())})

    # Zbuduj tabelę zapisującą zrealizowane transakcje.
    transaction_df:pd.DataFrame =  pd.DataFrame(data = {"id_transakcji":pd.Series(dtype = pd.Int32Dtype()),
                                         "kwota":pd.Series(dtype = pd.Float64Dtype()),
                                         "data_transakcji":pd.Series(dtype = "datetime64[ns]"),
                                         "id_klienta":pd.Series(dtype = pd.Int32Dtype()),
                                         "id_wycieczki":pd.Series(dtype = pd.Int32Dtype())
                                         })


    
    # Określ, ile wycieczek ma być zaplanowanych.
    n_trips: int = np.random.randint(low = n_trip_range[0], high = n_trip_range[1])

    # Stwórz unikalny identyfikator każdej transakcji.
    transaction_id:int = 1 

    for trip_id in range(1, n_trips+1):
        # Wylosuj datę rozpoczęcia się wyjazdu.
        trip_start_date:dt.date = generate_startday()

  

        # Ustal, w jakim okresie klienti mogą opłacać bilet.
        trans_period_start : dt.date = trip_start_date - dt.timedelta(30)
        trans_period_end : dt.date = trip_start_date - dt.timedelta(7)

        # Wygeneruj zakres dat, w których klienci mogą opłacać bilety.
        trans_period: np.array[dt.date] = pd.date_range(trans_period_start, trans_period_end, freq = "1d").date
    

        # Wylosuj  (maksymalną) liczbę podróżniczych
        n_max_clients: int = np.random.randint(n_client_range[0],
                                            n_client_range[1]+1)
        
        
        # Licznik faktycznej liczby klientów.
        n_client_fact: int = 0
       
        # Wylosuj miasto, do którego idziemy.
        city_id: int = cities_df["id_miasta"].sample().values[0]
   
        # Znajdź rekord opisujący wylosowane miasto.
        city_record:pd.DataFrame = cities_df.loc[ cities_df["id_miasta"] == city_id, ["id_miasta", "cena_wyjazdu","dlugosc_wycieczki"]]

        # Długość wycieczki.
        trip_duration:pd.Timedelta = pd.to_timedelta(city_record["dlugosc_wycieczki"].values[0])

        # Znajdź datę zakończenia wycieczki.
        trip_end_date:dt.date = trip_start_date + trip_duration
    
        # Znajdź cene biletu odpowiadającą temu miastu.
        ticket_price: float = city_record["cena_wyjazdu"].values[0]

        
        # Znajdź odpowiednią liczbę róznych klientów.
        clients_ids:pd.Series = clients_df["id_klienta"].sample(n_max_clients, replace = False)


        # Dodanie każdego klienta rozważ indywidualnie.
        for client_id in clients_ids:
            # Znajdź rekord opisujący wybranego klienta.
            client_record: pd.DataFrame = clients_df.loc[clients_df["id_klienta"] == client_id, :]

           
    
            # Znajdź wszystkie transakcje związane z tym klientem.
            client_transaction:pd.DataFrame = transaction_df.loc[transaction_df["id_klienta"] == client_id, :]

            # Znajdź znizkę przysługującą temu klientowi.
            discount: float = client_record["znizka"].values[0]

            # Policz cenę biletu po zniżce.
            discounted_ticket: float = round(discount * ticket_price, 2)

            # Wylosuj datę zawarcia transakcji.
            transaction_date: dt.date = pd.to_datetime(np.random.choice(trans_period))



            # Jeżeli klient nie dokonywał jeszcze żadnych transakcji, dodaj go do tabeli od razu.
            if client_transaction.shape[0] == 0:
                transaction_df.loc[transaction_id, :] = [transaction_id, discounted_ticket,
                                                            transaction_date, client_id, trip_id]
                
                transaction_id +=1
                n_client_fact += 1

            else:
                  # W przeciwnym wypadku, znajdź wycieczki, w których brał udzial.

                # Znajdź identyfikatory wycieczek, w których brał udział klient.
                client_trip_ids: pd.DataFrame = client_transaction["id_wycieczki"]

                # Znajdź  wycieczki, w których brał udział klient.
                client_trips:pd.DataFrame = planned_trips_df.merge(right = client_trip_ids, on = "id_wycieczki")

                # Teraż znajdź wycieczki, które się odbyły.
                client_taken_trips : pd.DataFrame = client_trips.loc[client_trips["odbyla_sie"] == True, :]


                 # Jeżeli klient nie brał jeszcze udziału w żadnej wycieczce, dodaj go do tabeli od razu.
                if client_taken_trips.shape[0] == 0:
                    transaction_df.loc[transaction_id, :] = [transaction_id, discounted_ticket,
                                                            transaction_date, client_id, trip_id]
                    
                    transaction_id +=1
                    n_client_fact += 1
                
                else:
                    # Znajdź daty rozpoczęcia i zakończenia wycieczek, w których brał udział klient.
                    client_taken_trips_with_time: pd.DataFrame =client_taken_trips.merge(cities_df, on = "id_miasta")[["data_rozpoczecia", "dlugosc_wycieczki"]]

                    # Dodaj kolumnę informującą o dacie zakończenia wycieczki.
                    client_taken_trips_with_time["data_zakonczenia"] = pd.to_datetime(client_taken_trips_with_time["data_rozpoczecia"] +client_taken_trips_with_time["dlugosc_wycieczki"])
    
                    # Znajdź datę zakończenia najwczesniejszej wycieczki.
                    earliest_trip_end_date = pd.to_datetime(client_taken_trips_with_time["data_zakonczenia"].max()).date()

                    # Znajdź datę rozpoczęcia najpoźniejszej wycieczki.
                    latest_trip_start_date = pd.to_datetime(client_taken_trips_with_time["data_rozpoczecia"].min()).date()
                  
                    # Dodaj klienta, jeżeli różnica między datą rozpoczęcia tej wycieczki, a datą zakończenia wynosi co najmniej 3.
                    if (trip_start_date - earliest_trip_end_date).days >= 3 or (latest_trip_start_date - trip_end_date).days >= 3:
                            transaction_df.loc[transaction_id, :] = [transaction_id, discounted_ticket,
                                                            transaction_date, client_id, trip_id]
                            
                            transaction_id += 1
                            n_client_fact += 1
                        
                                   
        # Określ, czy wycieczka się odbyła na podstawie liczby klientów.
        if n_client_fact >= (3*n_client_range[0] + n_client_range[1])/4:
            took_place: bool = True
        else:
            took_place: bool = False

        # Przekonwertuj datę rozpoczęcia wycieczki na odpowiedni typ, aby można było ją zapisać do tabeli.
        trip_start_date = pd.to_datetime(trip_start_date)
        planned_trips_df.loc[trip_id, :] = (trip_id, trip_start_date, took_place, city_id)


    # Zapisz tabelę z planowanymi wycieczkami do pliku csv.
    planned_trips_df.to_csv(csv_tables_dir_path/"Wycieczki_db.csv",
                           sep = ";", encoding = "utf-8", 
                           index = False)
    
    # Zapisz tabelę z transakcjami do pliku csv.
    transaction_df.to_csv(csv_tables_dir_path/"Transakcje_db.csv",
                           sep = ";", encoding = "utf-8", 
                           index = False)


generate_trip_tables()



# ---------------------------------------------------------------------------------
## (8) Tworzenie danych osobowych pracowników.
def generate_worker_personal_data(first_names:pd.Series, last_names:pd.Series, trades_n:dict[str,int], email_domains:str) -> pd.DataFrame:
    """Funkcja generuje dane osobiste pracowników. Tworzone są wiersze imię, nazwisko, numer telefonu oraz adres e-mail firmowy.

    """
    # Przygotuj wyjściową ramkę danych.
    workers_df: pd.DataFrame = pd.DataFrame(data = {"imie":pd.Series(dtype = pd.StringDtype()),
                                                    "nazwisko": pd.Series(dtype = pd.StringDtype()), 
                                                    "stanowisko":pd.Series(dtype = pd.CategoricalDtype(categories = ["kierowca","przewodnik"],
                                                                                                  ordered = False
                                                                                                  )),
                                                    "numer_telefonu":pd.Series(dtype = pd.StringDtype()), 
                                                    "adres_email": pd.Series(dtype = pd.StringDtype())},                                           
    )

    id: int = 0
    for pos in trades_n:
        for _ in range(trades_n[pos]):
            first_name_idx:int = np.random.randint(0, first_names.shape[0])
            last_name_idx:int = np.random.randint(0, last_names.shape[0])

            first_name:str = first_names[first_name_idx].capitalize() # Wylosuj imię
            last_name:str = last_names[last_name_idx].capitalize()  # Wylosuj nazwisko.

            # Wygeneruj losowy numer telefonu nie zaczynający się od 0.
            phone_number:np.array = np.random.choice(digits, 9)

            # Jeżeli wylosowaliśmy zero, podmień cyfrę.
            if phone_number[0] == "0":
                phone_number[0] = np.random.choice(digits[1:], 1)[0]

            phone_number: str = "".join(phone_number)

            # Stwórz email dla tego pracownika
            random_domain = np.random.choice(email_domains)
            email:str = first_name.lower() + last_name.lower() + "".join(np.random.choice(digits, 3)) +"@" + random_domain
            

            workers_df.loc[id, :] = [first_name, last_name, pos ,phone_number, email]

            id += 1

    return workers_df


def generate_workers():
    # Policz, ilu klientów dokonało transakcji.
    n_clients:int = pd.read_csv(csv_tables_dir_path/"Transakcje_db.csv",
                            sep = ";", 
                            usecols = [0]).iloc[:, 0].unique().shape[0]
    
    

    # Dwa razy więcej przewodników niż kierowców..
    female_drivers : int = int(np.ceil(n_clients/driver_ratio))
    females_guides: int = 2*female_drivers

    male_drivers:int = int(np.ceil(n_clients/driver_ratio))
    male_guides = 2*male_drivers

    female_trades_n: dict[str, int] = {"przewodnik":females_guides, 
                                    "kierowca":female_drivers}

    male_trades_n: dict[str, int] = {"przewodnik":male_guides, 
                                    "kierowca":male_guides}


    # Wygeneruj dane osobiste dla pracowniczek
    email_domains:list[str] = ["nowowiejska.com"]

    female_workers_df : pd.DataFrame = generate_worker_personal_data(female_first_names, female_last_names, female_trades_n, email_domains)

    male_workers_df : pd.DataFrame = generate_worker_personal_data(male_first_names, male_last_names, male_trades_n, email_domains)

    # Połącz kobiecych i męskich pracowników.
    workers_data_df : pd.DataFrame = merge_females_and_males(female_workers_df, male_workers_df, "id_pracownika")


    # Zapisz dane pracowników do pliku .csv.
    workers_data_df.to_csv(path_or_buf = csv_tables_dir_path/"Pracownicy_db.csv",
                        sep = ";", index = False)


generate_workers()



# ---------------------------------------------------------------------------------
# (9) Przydzielanie pracowników.

def one_type_workers_to_trip(trips_and_workers_df:pd.DataFrame, trip_record:pd.DataFrame, trip_id:int, taken_trips_detail_df:pd.DataFrame,
                             position_df:pd.DataFrame, n_workers:int, employ_id:int):
        i: int = 0
        while i < n_workers:
            # Wylosuj jednego pracownika.
            worker_id:int = position_df.sample(1).values[0]

            # Znajdź rekordy zwiazane z jego udziałem w wycieczkach.
            worked_trips = trips_and_workers_df.loc [ trips_and_workers_df["id_pracownika"] == worker_id, :]

            # Jeżeli ta tabela jest pusta, dodaj pracownika do tabeli od razu.
            if worked_trips.shape[0] == 0:
                trips_and_workers_df.loc[employ_id, :] = (worker_id, trip_id)

                employ_id += 1
                i += 1

            else:
                # W przeciwnym razie znajdź szczegóły dotyczące wycieczek, w których ten pracownik brał udział.
                worked_trips_details: pd.DataFrame = taken_trips_detail_df.loc[worked_trips["id_wycieczki"], :]

                # Znajdź datę zakończenia ostatniej wycieczki.
                earliest_end_date:dt.date = worked_trips_details["data_zakonczenia"].max()
                
                # Znajdź datę rozpoczęcia pierwszej wycieczki.
                latest_start_date:dt.date = worked_trips_details["data_rozpoczecia"].min()

                # Znajdź datę zakończenia i rozpoczęcia aktualnie rozważanej wycieczki.
                trip_start_date:dt.date = trip_record["data_zakonczenia"]
                trip_end_date:dt.date = trip_record["data_rozpoczecia"]


                if (trip_start_date - earliest_end_date).days > 3 or (latest_start_date -trip_end_date).days > 3:
                    trips_and_workers_df.loc[employ_id, :] = (worker_id, trip_id)

                    employ_id += 1          
                    i += 1   




def assign_workers_to_trips():
    # Wczytaj tabelę z pracownikami.
    workers_df: pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Pracownicy_db.csv",
                                           sep = ";",
                                           encoding = "utf-8")


    # Wczytaj tabelę z wycieczkami.
    trips_df: pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Wycieczki_db.csv",
                                           sep = ";",
                                           encoding = "utf-8")
    # Sformatuj datę.
    trips_df['data_rozpoczecia'] = pd.to_datetime(trips_df['data_rozpoczecia'])

    # Wczytaj tabele z miastami.
    cities_df: pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Miasta_db.csv",
                                           sep = ";",
                                           encoding = "utf-8")
    
    # Przekonwertuj kolumnę na typ timedelta.
    cities_df['dlugosc_wycieczki'] = pd.to_timedelta(cities_df['dlugosc_wycieczki'])

    
    # Połącz tabelę "miasta" z tabelą "wycieczki", aby uzyskać pełne informacje i wyjeździe.
    trips_detail_df: pd.DataFrame = trips_df.merge(cities_df, on = "id_miasta")

    # Rekrutujemy pracowników jedynie do wycieczek, które się odbyły.
    taken_trips_detail_df: pd.DataFrame =   trips_detail_df.loc[trips_detail_df["odbyla_sie"] == True, 
                                                                ["id_wycieczki", "data_rozpoczecia",
                                                                 "dlugosc_wycieczki"]].set_index(keys = "id_wycieczki")
    
    taken_trips_detail_df["data_zakonczenia"] = taken_trips_detail_df['data_rozpoczecia'] + taken_trips_detail_df["dlugosc_wycieczki"]
   

    # Wczytaj tabelę z transakcjami, aby policzyć, ile osób bierze udział w każdej wycieczce.
    transactions_df: pd.DataFrame = pd.read_csv(csv_tables_dir_path/"Transakcje_db.csv",
                                           sep = ";",
                                           encoding = "utf-8")
    
    # Znajdź liczbę klientów biorących udział w każdej wycieczce.
    n_clients: pd.Series = transactions_df["id_wycieczki"].value_counts(sort = False)

    trips_and_workers_df: pd.DataFrame = pd.DataFrame(data = {"id_pracownika":pd.Series(dtype = pd.Int32Dtype()),
                                                              "id_wycieczki":pd.Series(dtype = pd.Int32Dtype())},
                                                              )

    # Tabela ze wszystkimi przewodnikami.
    guides_df:pd.Series = workers_df.loc[workers_df["stanowisko"] == "przewodnik", "id_pracownika"]
    # Tabela ze wszystkimi kierowcami.
    drivers_df:pd.Series = workers_df.loc[workers_df["stanowisko"] == "kierowca", "id_pracownika"]

 
    employ_id: int = 1 # Identyfikator wiersza w ramce "trips_and_workers_df"

    for trip_id in taken_trips_detail_df.index:
        trip_record:pd.DataFrame = taken_trips_detail_df.loc[trip_id,:]

        n_guides:int = int(np.ceil(n_clients[trip_id]/guide_ratio))
        n_drivers: int = int(np.ceil(n_clients[trip_id]/driver_ratio))

        # Umieść ramki konkretnych pozycji w liście.
        workers_dfs:list[pd.DataFrame] = [guides_df, drivers_df]
        n_workers:list[int] = [n_guides, n_drivers]

        for i in range(len(workers_dfs)):
            # Dodaj pracowników konkretnego typu.
            one_type_workers_to_trip(trips_and_workers_df, trip_record, trip_id, taken_trips_detail_df,
                                    workers_dfs[i], n_workers[i],  employ_id)
            
            employ_id += n_workers[i]


    trips_and_workers_df.to_csv(csv_tables_dir_path/"Wycieczki_pracownicy_db.csv",
                                sep = ";", index = False
                                )
    

assign_workers_to_trips()