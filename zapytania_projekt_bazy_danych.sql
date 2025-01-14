-- 1. Znajdź najpopularniejsze rodzaje wycieczek, porównaj koszta i zyski, czy są opłacalne?
-- Najpopularniejsze wycieczki bez wzgledu na to czy sie odbyły czy nie
SELECT 
    m.miasto AS wycieczka,
    COUNT(t.id_klienta) AS liczba_osob_zainteresowanych
FROM 
    Wycieczki w
JOIN 
    Miasta m ON w.id_miasta = m.id_miasta
LEFT JOIN 
    Transakcje t ON w.id_wycieczki = t.id_wycieczki
-- WHERE 
--    w.odbyla_sie = 1      warunek jakby jednak miały być tylko te co się odbyły
GROUP BY 
    m.miasto
ORDER BY 
    liczba_osob_zainteresowanych DESC;

--  koszta i zyski, czy opłacalne  i ile wycieczek sie odbyło
WITH Koszty_Wycieczki AS (
    SELECT 
        w.id_wycieczki,
        SUM(wyn.wynagrodzenie * m.dlugosc_wycieczki) AS koszt
    FROM 
        Wycieczki w
    JOIN 
        Wycieczki_pracownicy wp ON w.id_wycieczki = wp.id_wycieczki
    JOIN 
        Pracownicy p ON wp.id_pracownika = p.id_pracownika
    JOIN 
        Wynagrodzenie wyn ON p.stanowisko = wyn.stanowisko
    JOIN 
        Miasta m ON w.id_miasta = m.id_miasta
    WHERE 
        w.odbyla_sie = 1
    GROUP BY 
        w.id_wycieczki
),
Zyski_Wycieczki AS (
    SELECT 
        t.id_wycieczki,
        SUM(t.kwota) AS zysk
    FROM 
        Transakcje t
    JOIN 
        Wycieczki w ON t.id_wycieczki = w.id_wycieczki
    WHERE 
        w.odbyla_sie = 1
    GROUP BY 
        t.id_wycieczki
)
SELECT 
    m.miasto AS wycieczka,
    COUNT(w.id_wycieczki) AS liczba_wycieczek,
    COALESCE(SUM(kw.koszt), 0) AS koszt,
    COALESCE(SUM(zw.zysk), 0) AS przychód,
    COALESCE(SUM(zw.zysk) - SUM(kw.koszt), 0) AS zysk,
    CASE 
        WHEN COALESCE(SUM(zw.zysk) - SUM(kw.koszt), 0) > 0 THEN 'oplacalna'
        ELSE 'nieoplacalna'
    END AS oplacalność
FROM 
    Wycieczki w
JOIN 
    Miasta m ON w.id_miasta = m.id_miasta
LEFT JOIN 
    Koszty_Wycieczki kw ON w.id_wycieczki = kw.id_wycieczki
LEFT JOIN 
    Zyski_Wycieczki zw ON w.id_wycieczki = zw.id_wycieczki
WHERE 
    w.odbyla_sie = 1
GROUP BY 
    m.miasto
ORDER BY 
    zysk DESC;



-- liczba obsłużonych klientów w każdym miesiącu działalności firmy, czy firma rośnie, czy podupada?
SELECT 
    EXTRACT(YEAR FROM T.data_transakcji) AS Rok,
    EXTRACT(MONTH FROM T.data_transakcji) AS Miesiac,
    COUNT(DISTINCT T.id_klienta) AS Liczba_Klientow
FROM 
    Transakcje T
GROUP BY 
    EXTRACT(YEAR FROM T.data_transakcji), EXTRACT(MONTH FROM T.data_transakcji)
ORDER BY 
    Rok, Miesiac;

-- po których wycieczkach klienci wracają na kolejne, a po których mają dość i więcej ich nie widzicie. Czy są takie, które być może powinny zniknąć z oferty?
WITH Klienci_Wycieczki AS (
    SELECT 
        t.id_klienta,
        t.id_wycieczki
    FROM 
        Transakcje t
    JOIN 
        Wycieczki w ON t.id_wycieczki = w.id_wycieczki
    WHERE 
        w.odbyla_sie = 1
),
Powroty AS (
    SELECT 
        kw1.id_wycieczki AS pierwsza_wycieczka,
        COUNT(DISTINCT kw1.id_klienta) AS liczba_klientow,
        COUNT(DISTINCT CASE 
            WHEN kw2.id_wycieczki IS NOT NULL AND kw1.id_wycieczki != kw2.id_wycieczki THEN kw1.id_klienta
        END) AS liczba_powracajacych
    FROM 
        Klienci_Wycieczki kw1
    LEFT JOIN 
        Klienci_Wycieczki kw2 ON kw1.id_klienta = kw2.id_klienta
    GROUP BY 
        kw1.id_wycieczki
)
SELECT 
    m.miasto AS wycieczka,
    p.liczba_klientow,
    p.liczba_powracajacych,
    ROUND((p.liczba_powracajacych * 100.0) / p.liczba_klientow, 2) AS procent_powrotow
FROM 
    Powroty p
JOIN 
    Wycieczki w ON p.pierwsza_wycieczka = w.id_wycieczki
JOIN 
    Miasta m ON w.id_miasta = m.id_miasta
ORDER BY 
    procent_powrotow DESC;
